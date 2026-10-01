import ast
import asyncio
import io
import json
import os
import re
import shutil
import signal
import sys
import tempfile
import time
import uuid
from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status as http_status

from app.db.models.coding import (
    CodingQuestion,
    CodingTestCase,
    CodingSubmission,
    CodingResult,
)
from app.modules.coding.schemas import (
    ALLOWED_LANGUAGES,
)
from app.modules.coding.services.test_case_service import normalize_io_text
from app.modules.coding.services.submission_service import format_submission_dict
from app.modules.coding.services.performance_service import compute_submission_score


# ============================================================================
# SECURITY NOTICE & DEFENSE-IN-DEPTH ARCHITECTURE
# ============================================================================
# IMPORTANT SECURITY CONSTRAINTS:
# 1. Untrusted Code Execution: Static AST validation (Python) and regular expression
#    filters (JavaScript) provide early defense-in-depth pre-checks for obvious
#    malicious constructs. However, static checks and Python restricted builtins DO NOT
#    constitute a complete security sandboxing boundary on their own. Untrusted Python
#    and JavaScript code can bypass lexical or AST filters via dynamic attribute
#    resolution, reflection, or indirect invocations.
# 2. Host Isolation Absence: In bare host environments (e.g. standard Windows/Linux
#    developer setups), OS-level container isolation (such as Docker, gVisor microVMs,
#    Linux cgroups/namespaces, or Windows Job Objects) is NOT active. Production
#    deployments MUST execute untrusted user submissions inside isolated microVMs
#    or unprivileged disposable containers with strict memory and CPU quotas.
# 3. Mitigations Implemented:
#    - Subprocess process-tree termination on timeout/abort (cross-platform: taskkill /F /T
#      on Windows, killpg on POSIX).
#    - Bounded streaming I/O with maximum buffer limits (MAX_OUTPUT_BYTES = 64KB)
#      to prevent memory exhaustion Denial-of-Service attacks ("Output Limit Exceeded").
#    - Scrubbed execution environment variables (PATH, SYSTEMROOT).
#    - Guaranteed temporary directory and file cleanup with handle-release retry.
# ============================================================================

MAX_OUTPUT_BYTES = 64 * 1024  # 64 KB maximum buffer limit per test case run


# ============================================================================
# SECURITY POLICIES & FORBIDDEN CONSTRUCTS
# ============================================================================

DANGEROUS_PYTHON_MODULES = {
    "os", "subprocess", "shutil", "socket", "http", "urllib", "urllib3",
    "requests", "aiohttp", "ftplib", "smtplib", "telnetlib", "pickle", "shelve",
    "ctypes", "winreg", "psutil", "signal", "multiprocessing", "threading",
    "pty", "commands", "importlib", "platform", "webbrowser", "posix", "nt",
}

DANGEROUS_PYTHON_ATTRIBUTES = {
    "__subclasses__", "__bases__", "__base__", "__mro__", "__globals__",
    "__code__", "__builtins__",
}

DANGEROUS_PYTHON_CALLS = {
    "open", "compile", "eval", "exec", "__import__", "breakpoint",
}

DANGEROUS_JS_PATTERNS = [
    r"require\s*\(\s*['\"](?:fs|child_process|net|http|https|cluster|dgram|dns|tls)['\"]\s*\)",
    r"process\s*\.\s*(?:env|exit|kill|abort)",
    r"eval\s*\(",
    r"Function\s*\(",
]


def validate_python_code_security(code: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Perform static AST analysis to detect syntax errors and unsafe operations.
    Returns (verdict, error_message) if an issue is found, else (None, None).
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return "Compilation Error", f"SyntaxError at line {e.lineno}: {e.msg}"

    for node in ast.walk(tree):
        # 1. Check direct imports (import os, etc.)
        if isinstance(node, ast.Import):
            for alias in node.names:
                root_module = alias.name.split(".")[0].lower()
                if root_module in DANGEROUS_PYTHON_MODULES:
                    return (
                        "Compilation Error",
                        f"Security policy violation: Module '{root_module}' is not permitted.",
                    )
        # 2. Check from imports (from os import path, etc.)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                root_module = node.module.split(".")[0].lower()
                if root_module in DANGEROUS_PYTHON_MODULES:
                    return (
                        "Compilation Error",
                        f"Security policy violation: Module '{root_module}' is not permitted.",
                    )
        # 3. Check dangerous attribute access (__subclasses__, __globals__, etc.)
        elif isinstance(node, ast.Attribute):
            if node.attr in DANGEROUS_PYTHON_ATTRIBUTES:
                return (
                    "Compilation Error",
                    f"Security policy violation: Attribute '{node.attr}' is not permitted.",
                )
        # 4. Check dangerous built-in function calls (open, eval, exec, etc.)
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in DANGEROUS_PYTHON_CALLS:
                    return (
                        "Compilation Error",
                        f"Security policy violation: Function '{node.func.id}' is not permitted.",
                    )

    return None, None


def validate_javascript_code_security(code: str) -> Tuple[Optional[str], Optional[str]]:
    """Check JavaScript code for dangerous module requires or process inspection."""
    for pattern in DANGEROUS_JS_PATTERNS:
        match = re.search(pattern, code, re.IGNORECASE)
        if match:
            return (
                "Compilation Error",
                f"Security policy violation: Restricted operation detected: '{match.group(0)}'.",
            )
    return None, None


def sanitize_traceback(tb_str: str) -> str:
    """Scrub host-specific filesystem paths and usernames from tracebacks."""
    if not tb_str:
        return ""
    # Strip local Windows and Unix drive/folder paths
    scrubbed = re.sub(r'[A-Za-z]:\\[^\n]*\\([^\\]+\.py)', r'\1', tb_str)
    scrubbed = re.sub(r'/[^\n]*/([^/]+\.py)', r'\1', scrubbed)
    # Remove references to Python library internals
    scrubbed = re.sub(r'File "[^"]+", line (\d+)', r'line \1', scrubbed)
    return scrubbed.strip()


def outputs_match(actual: str, expected: str) -> bool:
    """
    Compare actual output against expected output with normalization for whitespace,
    CRLF vs LF, booleans, and JSON structures.
    """
    norm_actual = normalize_io_text(actual)
    norm_expected = normalize_io_text(expected)

    if norm_actual == norm_expected:
        return True

    # Case-insensitive comparison for boolean values
    if norm_actual.lower() == norm_expected.lower():
        return True

    # Attempt JSON-parsed equivalence (handles [0, 1] vs [0,1] or dict key orders)
    try:
        return json.loads(norm_actual) == json.loads(norm_expected)
    except Exception:
        pass

    return False


# ============================================================================
# PYTHON EXECUTION HARNESS
# ============================================================================

PYTHON_RUNNER_SCRIPT = r"""
import sys
import io
import json
import ast

def safe_parse_arg(val_str):
    val_str = val_str.strip()
    try:
        return json.loads(val_str)
    except Exception:
        try:
            return ast.literal_eval(val_str)
        except Exception:
            return val_str

def format_output(obj):
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, (list, dict, tuple)):
        return json.dumps(obj)
    return str(obj)

class BoundedStringIO(io.StringIO):
    def __init__(self, max_bytes=65536):
        super().__init__()
        self.max_bytes = max_bytes
        self.total_bytes = 0

    def write(self, s):
        if not s:
            return 0
        self.total_bytes += len(s.encode("utf-8", errors="replace"))
        if self.total_bytes > self.max_bytes:
            raise RuntimeError("Output Limit Exceeded: Standard output exceeded maximum size limit of 64KB.")
        return super().write(s)

def main():
    input_str = sys.stdin.read()
    captured_stdout = BoundedStringIO(max_bytes=65536)
    real_stdout = sys.stdout
    real_stdin = sys.stdin
    sys.stdout = captured_stdout
    sys.stdin = io.StringIO(input_str)

    user_globals = {
        "__name__": "__main__",
        "__doc__": None,
        "__package__": None,
    }

    import builtins
    import math, collections, heapq, itertools, bisect, re, functools, copy, random, string

    real_import = builtins.__import__
    SAFE_MODULES = {
        "math", "collections", "heapq", "itertools", "bisect", "re",
        "functools", "copy", "random", "string", "typing", "json", "sys", "time", "dataclasses",
    }
    def safe_import(name, *args, **kwargs):
        root_pkg = name.split(".")[0]
        if root_pkg not in SAFE_MODULES:
            raise ImportError(f"Import of module '{name}' is not permitted in sandbox.")
        return real_import(name, *args, **kwargs)

    b_dict = {k: getattr(builtins, k) for k in dir(builtins)}
    safe_builtins = {
        k: v for k, v in b_dict.items()
        if k not in {"open", "eval", "exec", "compile", "breakpoint", "help"}
    }
    safe_builtins["__import__"] = safe_import

    lines = input_str.splitlines()
    line_idx = [0]
    def safe_input(prompt=None):
        if line_idx[0] < len(lines):
            val = lines[line_idx[0]]
            line_idx[0] += 1
            return val
        raise EOFError("EOF when reading a line")

    safe_builtins["input"] = safe_input
    user_globals["__builtins__"] = safe_builtins
    user_globals["math"] = math
    user_globals["collections"] = collections
    user_globals["heapq"] = heapq
    user_globals["itertools"] = itertools
    user_globals["bisect"] = bisect
    user_globals["re"] = re
    user_globals["functools"] = functools

    try:
        with open("solution.py", "r", encoding="utf-8") as f:
            user_code = f.read()
        compiled = compile(user_code, "solution.py", "exec")
        exec(compiled, user_globals)
    except Exception as e:
        sys.stdout = real_stdout
        sys.stdin = real_stdin
        exc_type = type(e).__name__
        sys.stderr.write(f"{exc_type}: {e}\n")
        sys.exit(1)

    out_val = captured_stdout.getvalue()
    sys.stdout = real_stdout
    sys.stdin = real_stdin

    # If code already produced stdout or consumed input()
    if out_val.strip() or line_idx[0] > 0:
        sys.stdout.write(out_val.strip())
        return

    # If code defined a function without explicit calling, invoke it with parsed input
    user_funcs = [
        (k, v) for k, v in user_globals.items()
        if callable(v) and getattr(v, "__module__", None) in ("__main__", None)
        and not k.startswith("__")
    ]

    if not user_funcs:
        sys.stdout.write(out_val.strip())
        return

    target_fn = user_funcs[0][1]
    arg_lines = [l for l in input_str.strip().splitlines() if l.strip()]
    parsed_args = [safe_parse_arg(l) for l in arg_lines]

    try:
        import inspect
        sig = inspect.signature(target_fn)
        param_count = len(sig.parameters)
        if len(parsed_args) == param_count:
            res = target_fn(*parsed_args)
        elif len(parsed_args) == 1 and param_count > 1 and isinstance(parsed_args[0], (list, tuple)):
            res = target_fn(*parsed_args[0])
        else:
            res = target_fn(*parsed_args)

        if res is not None:
            sys.stdout.write(format_output(res))
    except Exception as e:
        exc_type = type(e).__name__
        sys.stderr.write(f"{exc_type}: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()
"""


# ============================================================================
# SUBPROCESS EXECUTION ENGINE
# ============================================================================

async def terminate_process_tree(proc: asyncio.subprocess.Process) -> None:
    """
    Forcefully terminate a subprocess and its entire descendant process tree.
    Cross-platform: uses Windows `taskkill /F /T /PID` on Windows,
    and process group kill via `os.killpg(os.getpgid(pid), signal.SIGKILL)` on POSIX.
    """
    if proc.returncode is not None:
        return
    pid = proc.pid
    if sys.platform == "win32":
        try:
            kill_proc = await asyncio.create_subprocess_exec(
                "taskkill", "/F", "/T", "/PID", str(pid),
                stdout=asyncio.subprocess.DEVNULL,
                stderr=asyncio.subprocess.DEVNULL,
            )
            await kill_proc.wait()
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass
    else:
        try:
            pgid = os.getpgid(pid)
            os.killpg(pgid, signal.SIGKILL)
        except Exception:
            try:
                proc.kill()
            except Exception:
                pass
    try:
        await asyncio.wait_for(proc.wait(), timeout=1.0)
    except Exception:
        pass


async def communicate_bounded(
    proc: asyncio.subprocess.Process,
    input_bytes: bytes = b"",
    max_bytes: int = MAX_OUTPUT_BYTES,
) -> Tuple[bytes, bytes, bool]:
    """
    Safely stream stdin and read stdout/stderr up to a strict maximum byte limit.
    If the accumulated output exceeds max_bytes, terminates the process tree immediately
    to prevent memory exhaustion Denial-of-Service attacks.
    Returns (stdout_bytes, stderr_bytes, limit_exceeded).
    """
    stdout_chunks: List[bytes] = []
    stderr_chunks: List[bytes] = []
    total_bytes = 0
    limit_exceeded = False

    async def _feed():
        if input_bytes and proc.stdin:
            try:
                proc.stdin.write(input_bytes)
                await proc.stdin.drain()
            except (BrokenPipeError, ConnectionResetError):
                pass
            finally:
                try:
                    proc.stdin.close()
                    await proc.stdin.wait_closed()
                except Exception:
                    pass
        elif proc.stdin:
            try:
                proc.stdin.close()
                await proc.stdin.wait_closed()
            except Exception:
                pass

    async def _read_stream(reader: Optional[asyncio.StreamReader], chunks: List[bytes]):
        nonlocal total_bytes, limit_exceeded
        if not reader:
            return
        while True:
            try:
                chunk = await reader.read(4096)
            except Exception:
                break
            if not chunk:
                break
            chunks.append(chunk)
            total_bytes += len(chunk)
            if total_bytes > max_bytes:
                limit_exceeded = True
                await terminate_process_tree(proc)
                break

    try:
        feed_task = asyncio.create_task(_feed())
        stdout_task = asyncio.create_task(_read_stream(proc.stdout, stdout_chunks))
        stderr_task = asyncio.create_task(_read_stream(proc.stderr, stderr_chunks))

        await asyncio.gather(feed_task, stdout_task, stderr_task, return_exceptions=True)
        await proc.wait()
    finally:
        if getattr(proc, "_transport", None):
            for fd in (0, 1, 2):
                try:
                    tp = proc._transport.get_pipe_transport(fd)
                    if tp and not tp.is_closing():
                        tp.close()
                except Exception:
                    pass

    return b"".join(stdout_chunks), b"".join(stderr_chunks), limit_exceeded


async def execute_python_test_case(
    code: str,
    input_data: str,
    expected_output: str,
    is_sample: bool,
    time_limit_sec: float,
) -> Dict[str, Any]:
    """Execute Python code against a single test case inside a sanitized sandbox directory."""
    temp_dir = tempfile.mkdtemp(prefix="coding_sandbox_")
    start_time = time.perf_counter()
    proc = None

    try:
        solution_path = os.path.join(temp_dir, "solution.py")
        runner_path = os.path.join(temp_dir, "runner.py")

        with open(solution_path, "w", encoding="utf-8") as f:
            f.write(code)

        with open(runner_path, "w", encoding="utf-8") as f:
            f.write(PYTHON_RUNNER_SCRIPT)

        # Environment scrubbing: pass minimal system variables only
        clean_env = {
            "SYSTEMROOT": os.environ.get("SYSTEMROOT", "C:\\Windows"),
            "PATH": os.path.dirname(sys.executable),
            "PYTHONUNBUFFERED": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
        }

        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            runner_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=temp_dir,
            env=clean_env,
            start_new_session=True,
        )

        try:
            stdout_bytes, stderr_bytes, limit_exceeded = await asyncio.wait_for(
                communicate_bounded(proc, input_bytes=input_data.encode("utf-8"), max_bytes=MAX_OUTPUT_BYTES),
                timeout=time_limit_sec,
            )
            exec_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
        except asyncio.TimeoutError:
            if proc:
                await terminate_process_tree(proc)
            return {
                "passed": False,
                "verdict": "Time Limit Exceeded",
                "execution_time_ms": time_limit_sec * 1000,
                "actual_output": None,
                "expected_output": expected_output if is_sample else None,
                "input_data": input_data if is_sample else None,
                "error_message": f"Time limit exceeded ({time_limit_sec}s).",
            }

        actual_output = stdout_bytes.decode("utf-8", errors="replace")[:10000]
        stderr_text = stderr_bytes.decode("utf-8", errors="replace")[:10000]

        if limit_exceeded or "Output Limit Exceeded" in stderr_text:
            return {
                "passed": False,
                "verdict": "Output Limit Exceeded",
                "execution_time_ms": exec_time_ms,
                "actual_output": None,
                "expected_output": expected_output if is_sample else None,
                "input_data": input_data if is_sample else None,
                "error_message": f"Output limit exceeded (maximum {MAX_OUTPUT_BYTES // 1024} KB).",
            }

        if proc.returncode != 0:
            clean_err = sanitize_traceback(stderr_text)
            return {
                "passed": False,
                "verdict": "Runtime Error",
                "execution_time_ms": exec_time_ms,
                "actual_output": None,
                "expected_output": expected_output if is_sample else None,
                "input_data": input_data if is_sample else None,
                "error_message": clean_err or "Runtime error occurred during execution.",
            }

        passed = outputs_match(actual_output, expected_output)
        return {
            "passed": passed,
            "verdict": "Passed" if passed else "Wrong Answer",
            "execution_time_ms": exec_time_ms,
            "actual_output": actual_output.strip() if is_sample else None,
            "expected_output": expected_output if is_sample else None,
            "input_data": input_data if is_sample else None,
            "error_message": None if passed else "Output does not match expected output.",
        }

    finally:
        if proc and proc.returncode is None:
            try:
                await terminate_process_tree(proc)
            except Exception:
                pass
        for attempt in range(3):
            try:
                shutil.rmtree(temp_dir, ignore_errors=False)
                break
            except Exception:
                if attempt < 2:
                    await asyncio.sleep(0.05)
                else:
                    shutil.rmtree(temp_dir, ignore_errors=True)


async def execute_javascript_test_case(
    code: str,
    input_data: str,
    expected_output: str,
    is_sample: bool,
    time_limit_sec: float,
) -> Dict[str, Any]:
    """Execute JavaScript code using Node.js in an isolated directory."""
    temp_dir = tempfile.mkdtemp(prefix="coding_js_sandbox_")
    start_time = time.perf_counter()
    proc = None

    try:
        solution_path = os.path.join(temp_dir, "solution.js")
        with open(solution_path, "w", encoding="utf-8") as f:
            f.write(code)

        node_bin = shutil.which("node") or "node"
        node_dir = os.path.dirname(shutil.which("node")) if shutil.which("node") else ""
        system_root = os.environ.get("SYSTEMROOT", "C:\\Windows")
        system_32 = os.path.join(system_root, "System32")
        sanitized_path = os.pathsep.join(filter(None, [node_dir, system_32]))

        clean_env = {
            "SYSTEMROOT": system_root,
            "PATH": sanitized_path,
        }

        proc = await asyncio.create_subprocess_exec(
            node_bin,
            solution_path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=temp_dir,
            env=clean_env,
            start_new_session=True,
        )

        try:
            stdout_bytes, stderr_bytes, limit_exceeded = await asyncio.wait_for(
                communicate_bounded(proc, input_bytes=input_data.encode("utf-8"), max_bytes=MAX_OUTPUT_BYTES),
                timeout=time_limit_sec,
            )
            exec_time_ms = round((time.perf_counter() - start_time) * 1000, 2)
        except asyncio.TimeoutError:
            if proc:
                await terminate_process_tree(proc)
            return {
                "passed": False,
                "verdict": "Time Limit Exceeded",
                "execution_time_ms": time_limit_sec * 1000,
                "actual_output": None,
                "expected_output": expected_output if is_sample else None,
                "input_data": input_data if is_sample else None,
                "error_message": f"Time limit exceeded ({time_limit_sec}s).",
            }

        actual_output = stdout_bytes.decode("utf-8", errors="replace")[:10000]
        stderr_text = stderr_bytes.decode("utf-8", errors="replace")[:10000]

        if limit_exceeded or "Output Limit Exceeded" in stderr_text:
            return {
                "passed": False,
                "verdict": "Output Limit Exceeded",
                "execution_time_ms": exec_time_ms,
                "actual_output": None,
                "expected_output": expected_output if is_sample else None,
                "input_data": input_data if is_sample else None,
                "error_message": f"Output limit exceeded (maximum {MAX_OUTPUT_BYTES // 1024} KB).",
            }

        if proc.returncode != 0:
            return {
                "passed": False,
                "verdict": "Runtime Error",
                "execution_time_ms": exec_time_ms,
                "actual_output": None,
                "expected_output": expected_output if is_sample else None,
                "input_data": input_data if is_sample else None,
                "error_message": stderr_text.strip() or "Runtime error.",
            }

        passed = outputs_match(actual_output, expected_output)
        return {
            "passed": passed,
            "verdict": "Passed" if passed else "Wrong Answer",
            "execution_time_ms": exec_time_ms,
            "actual_output": actual_output.strip() if is_sample else None,
            "expected_output": expected_output if is_sample else None,
            "input_data": input_data if is_sample else None,
            "error_message": None if passed else "Output does not match expected output.",
        }

    finally:
        if proc and proc.returncode is None:
            try:
                await terminate_process_tree(proc)
            except Exception:
                pass
        for attempt in range(3):
            try:
                shutil.rmtree(temp_dir, ignore_errors=False)
                break
            except Exception:
                if attempt < 2:
                    await asyncio.sleep(0.05)
                else:
                    shutil.rmtree(temp_dir, ignore_errors=True)


async def execute_test_case(
    code: str,
    language: str,
    input_data: str,
    expected_output: str,
    is_sample: bool,
    time_limit_sec: float = 2.0,
) -> Dict[str, Any]:
    """Route test case execution to the appropriate language sandbox."""
    lang = language.strip().lower()

    if lang == "python":
        return await execute_python_test_case(
            code=code,
            input_data=input_data,
            expected_output=expected_output,
            is_sample=is_sample,
            time_limit_sec=time_limit_sec,
        )
    elif lang == "javascript":
        return await execute_javascript_test_case(
            code=code,
            input_data=input_data,
            expected_output=expected_output,
            is_sample=is_sample,
            time_limit_sec=time_limit_sec,
        )
    else:
        # Graceful notice if runtime is not configured on this host
        return {
            "passed": False,
            "verdict": "Compilation Error",
            "execution_time_ms": 0.0,
            "actual_output": None,
            "expected_output": expected_output if is_sample else None,
            "input_data": input_data if is_sample else None,
            "error_message": f"Execution environment for language '{language}' is not configured on this host.",
        }


# ============================================================================
# SUBMISSION EVALUATION PIPELINE
# ============================================================================

async def evaluate_submission(
    db: AsyncSession,
    submission_id: uuid.UUID,
    user_id: Optional[uuid.UUID] = None,
    time_limit_sec: float = 2.0,
) -> Dict[str, Any]:
    """
    Main evaluation pipeline:
    1. Loads submission, question, and test cases.
    2. Verifies user ownership if user_id is provided.
    3. Enforces security pre-checks (AST).
    4. Runs code in an isolated subprocess against all test cases.
    5. Evaluates verdicts and records outcome in coding_results.
    6. Updates submission status to 'completed'.
    """
    stmt = (
        select(CodingSubmission)
        .options(
            selectinload(CodingSubmission.question).selectinload(CodingQuestion.test_cases),
            selectinload(CodingSubmission.result),
        )
        .where(CodingSubmission.id == submission_id)
    )
    res = await db.execute(stmt)
    submission = res.scalar_one_or_none()

    if not submission:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Coding submission not found.",
        )

    if user_id is not None and submission.user_id != user_id:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You can only evaluate your own submissions.",
        )

    question = submission.question
    test_cases = question.test_cases if question else []
    test_cases = sorted(test_cases, key=lambda tc: tc.order_index)

    # Transition submission status to running
    submission.status = "running"
    await db.commit()

    # Pre-execution security check
    lang = submission.language.strip().lower()
    security_verdict = None
    security_error = None

    if lang == "python":
        security_verdict, security_error = validate_python_code_security(submission.code)
    elif lang == "javascript":
        security_verdict, security_error = validate_javascript_code_security(submission.code)

    test_case_results = []
    overall_verdict = "Accepted"
    first_error_message = None

    if security_verdict:
        overall_verdict = security_verdict
        first_error_message = security_error
        # Generate error results for all test cases
        for tc in test_cases:
            test_case_results.append(
                {
                    "test_case_id": str(tc.id),
                    "order_index": tc.order_index,
                    "is_sample": tc.is_sample,
                    "passed": False,
                    "verdict": security_verdict,
                    "execution_time_ms": 0.0,
                    "actual_output": None,
                    "expected_output": tc.expected_output if tc.is_sample else None,
                    "input_data": tc.input_data if tc.is_sample else None,
                    "error_message": security_error,
                }
            )
    elif not test_cases:
        overall_verdict = "No Test Cases"
        first_error_message = "No test cases found for this question."
    else:
        # Run test cases
        for tc in test_cases:
            run_res = await execute_test_case(
                code=submission.code,
                language=submission.language,
                input_data=tc.input_data,
                expected_output=tc.expected_output,
                is_sample=tc.is_sample,
                time_limit_sec=time_limit_sec,
            )

            tc_result = {
                "test_case_id": str(tc.id),
                "order_index": tc.order_index,
                "is_sample": tc.is_sample,
                "passed": run_res["passed"],
                "verdict": run_res["verdict"],
                "execution_time_ms": run_res["execution_time_ms"],
                "actual_output": run_res["actual_output"],
                "expected_output": run_res["expected_output"],
                "input_data": run_res["input_data"],
                "error_message": run_res["error_message"],
            }
            test_case_results.append(tc_result)

            if not run_res["passed"]:
                if not first_error_message:
                    first_error_message = run_res["error_message"] or f"Failed on test case {tc.order_index}"

                # Priority: Compilation Error > Output Limit Exceeded > Runtime Error > Time Limit Exceeded > Wrong Answer
                if run_res["verdict"] == "Compilation Error":
                    overall_verdict = "Compilation Error"
                elif run_res["verdict"] == "Output Limit Exceeded" and overall_verdict != "Compilation Error":
                    overall_verdict = "Output Limit Exceeded"
                elif run_res["verdict"] == "Runtime Error" and overall_verdict not in ("Compilation Error", "Output Limit Exceeded"):
                    overall_verdict = "Runtime Error"
                elif run_res["verdict"] == "Time Limit Exceeded" and overall_verdict not in ("Compilation Error", "Output Limit Exceeded", "Runtime Error"):
                    overall_verdict = "Time Limit Exceeded"
                elif overall_verdict == "Accepted":
                    overall_verdict = "Wrong Answer"

    # Compute aggregate metrics
    total_test_cases = len(test_cases)
    passed_test_cases = sum(1 for r in test_case_results if r["passed"])
    score = compute_submission_score(passed_test_cases, total_test_cases, overall_verdict)
    max_exec_time = max((r.get("execution_time_ms", 0.0) for r in test_case_results), default=0.0)

    # Persist in coding_results
    if submission.result:
        submission.result.verdict = overall_verdict
        submission.result.score = score
        submission.result.passed_test_cases = passed_test_cases
        submission.result.total_test_cases = total_test_cases
        submission.result.execution_time_ms = max_exec_time
        submission.result.error_message = first_error_message
        submission.result.test_case_results_json = test_case_results
    else:
        new_result = CodingResult(
            id=uuid.uuid4(),
            submission_id=submission.id,
            verdict=overall_verdict,
            score=score,
            passed_test_cases=passed_test_cases,
            total_test_cases=total_test_cases,
            execution_time_ms=max_exec_time,
            memory_kb=12400.0,  # Baseline process footprint
            error_message=first_error_message,
            test_case_results_json=test_case_results,
        )
        new_result.submission = submission
        submission.result = new_result
        db.add(new_result)

    submission.status = "completed"
    await db.commit()
    await db.refresh(submission, ["question", "result"])

    return format_submission_dict(submission)


async def run_sample_code(
    db: AsyncSession,
    question_id: uuid.UUID,
    language: str,
    code: str,
    time_limit_sec: float = 2.0,
) -> Dict[str, Any]:
    """
    Interactive 'Run Code' endpoint:
    Executes code against ONLY sample test cases without persisting a submission record.
    """
    q_stmt = (
        select(CodingQuestion)
        .options(selectinload(CodingQuestion.test_cases))
        .where(CodingQuestion.id == question_id)
    )
    q_res = await db.execute(q_stmt)
    question = q_res.scalar_one_or_none()

    if not question:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Coding question not found.",
        )

    sample_cases = [tc for tc in question.test_cases if tc.is_sample]
    sample_cases = sorted(sample_cases, key=lambda tc: tc.order_index)

    if not sample_cases:
        return {
            "verdict": "No Sample Cases",
            "passed_test_cases": 0,
            "total_test_cases": 0,
            "execution_time_ms": 0.0,
            "error_message": "No sample test cases are available for this question.",
            "test_cases": [],
        }

    lang = language.strip().lower()
    security_verdict = None
    security_error = None

    if lang == "python":
        security_verdict, security_error = validate_python_code_security(code)
    elif lang == "javascript":
        security_verdict, security_error = validate_javascript_code_security(code)

    if security_verdict:
        return {
            "verdict": security_verdict,
            "passed_test_cases": 0,
            "total_test_cases": len(sample_cases),
            "execution_time_ms": 0.0,
            "error_message": security_error,
            "test_cases": [
                {
                    "test_case_id": tc.id,
                    "order_index": tc.order_index,
                    "is_sample": True,
                    "passed": False,
                    "verdict": security_verdict,
                    "execution_time_ms": 0.0,
                    "actual_output": None,
                    "expected_output": tc.expected_output,
                    "input_data": tc.input_data,
                    "error_message": security_error,
                }
                for tc in sample_cases
            ],
        }

    overall_verdict = "Accepted"
    first_error = None
    results = []

    for tc in sample_cases:
        run_res = await execute_test_case(
            code=code,
            language=language,
            input_data=tc.input_data,
            expected_output=tc.expected_output,
            is_sample=True,
            time_limit_sec=time_limit_sec,
        )

        tc_item = {
            "test_case_id": tc.id,
            "order_index": tc.order_index,
            "is_sample": True,
            "passed": run_res["passed"],
            "verdict": run_res["verdict"],
            "execution_time_ms": run_res["execution_time_ms"],
            "actual_output": run_res["actual_output"],
            "expected_output": run_res["expected_output"],
            "input_data": run_res["input_data"],
            "error_message": run_res["error_message"],
        }
        results.append(tc_item)

        if not run_res["passed"]:
            if not first_error:
                first_error = run_res["error_message"]
            if run_res["verdict"] == "Compilation Error":
                overall_verdict = "Compilation Error"
            elif run_res["verdict"] == "Output Limit Exceeded" and overall_verdict != "Compilation Error":
                overall_verdict = "Output Limit Exceeded"
            elif run_res["verdict"] == "Runtime Error" and overall_verdict not in ("Compilation Error", "Output Limit Exceeded"):
                overall_verdict = "Runtime Error"
            elif run_res["verdict"] == "Time Limit Exceeded" and overall_verdict not in ("Compilation Error", "Output Limit Exceeded", "Runtime Error"):
                overall_verdict = "Time Limit Exceeded"
            elif overall_verdict == "Accepted":
                overall_verdict = "Wrong Answer"

    passed_count = sum(1 for r in results if r["passed"])
    max_time = max((r["execution_time_ms"] for r in results), default=0.0)

    return {
        "verdict": overall_verdict,
        "passed_test_cases": passed_count,
        "total_test_cases": len(sample_cases),
        "execution_time_ms": max_time,
        "error_message": first_error,
        "test_cases": results,
    }
