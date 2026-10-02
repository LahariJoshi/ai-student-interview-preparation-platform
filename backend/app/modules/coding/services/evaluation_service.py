import ast
import asyncio
import io
import json
import os
import re
import shutil
import subprocess
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

def main():
    input_str = sys.stdin.read()
    captured_stdout = io.StringIO()
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
    import inspect
    target_fn = None
    if "Solution" in user_globals and isinstance(user_globals["Solution"], type):
        try:
            sol_instance = user_globals["Solution"]()
            methods = [
                getattr(sol_instance, m) for m in dir(sol_instance)
                if callable(getattr(sol_instance, m)) and not m.startswith("_")
            ]
            if methods:
                target_fn = methods[0]
        except Exception:
            pass

    if target_fn is None:
        user_funcs = [
            (k, v) for k, v in user_globals.items()
            if callable(v) and not inspect.isclass(v)
            and getattr(v, "__module__", None) in ("__main__", None)
            and not k.startswith("__")
        ]
        if user_funcs:
            target_fn = user_funcs[0][1]

    if not target_fn:
        sys.stdout.write(out_val.strip())
        return

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

def run_subprocess_sync(
    cmd: List[str],
    input_str: Optional[str] = None,
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    timeout_sec: float = 2.0,
) -> Tuple[int, str, str, bool, float]:
    """
    Run a child process synchronously using subprocess.Popen.
    Returns (returncode, stdout_str, stderr_str, timed_out, elapsed_ms).
    Handles process termination/killing on timeout across Windows and Unix.
    Immune to asyncio SelectorEventLoop / ProactorEventLoop limitations.
    """
    start_time = time.perf_counter()
    timed_out = False
    stdout_bytes = b""
    stderr_bytes = b""
    returncode = -1

    input_bytes = input_str.encode("utf-8") if input_str is not None else None

    creationflags = 0
    if sys.platform == "win32":
        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)

    try:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE if input_bytes is not None else subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=cwd,
            env=env,
            creationflags=creationflags,
        )
    except Exception as e:
        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        return -1, "", str(e), False, elapsed_ms

    try:
        stdout_bytes, stderr_bytes = proc.communicate(input=input_bytes, timeout=timeout_sec)
        returncode = proc.returncode
    except subprocess.TimeoutExpired:
        timed_out = True
        try:
            proc.kill()
        except Exception:
            pass
        try:
            stdout_bytes, stderr_bytes = proc.communicate(timeout=1.0)
        except Exception:
            pass
        returncode = -1
    except Exception as e:
        try:
            proc.kill()
        except Exception:
            pass
        returncode = -1
        stderr_bytes = str(e).encode("utf-8")

    elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
    stdout_str = stdout_bytes.decode("utf-8", errors="replace")[:10000]
    stderr_str = stderr_bytes.decode("utf-8", errors="replace")[:10000]

    return returncode, stdout_str, stderr_str, timed_out, elapsed_ms


async def execute_python_test_case(
    code: str,
    input_data: str,
    expected_output: str,
    is_sample: bool,
    time_limit_sec: float,
) -> Dict[str, Any]:
    """Execute Python code against a single test case inside a sanitized sandbox directory."""
    temp_dir = tempfile.mkdtemp(prefix="coding_sandbox_")

    try:
        solution_path = os.path.join(temp_dir, "solution.py")
        runner_path = os.path.join(temp_dir, "runner.py")

        with open(solution_path, "w", encoding="utf-8") as f:
            f.write(code)

        with open(runner_path, "w", encoding="utf-8") as f:
            f.write(PYTHON_RUNNER_SCRIPT)

        # Environment scrubbing: pass minimal system variables only
        system_root = os.environ.get("SYSTEMROOT", "C:\\Windows")
        clean_env = {
            "SYSTEMROOT": system_root,
            "PATH": os.path.dirname(sys.executable) + os.pathsep + os.path.join(system_root, "System32"),
            "PYTHONUNBUFFERED": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
        }

        returncode, actual_output, stderr_text, timed_out, exec_time_ms = await asyncio.to_thread(
            run_subprocess_sync,
            cmd=[sys.executable, runner_path],
            input_str=input_data,
            cwd=temp_dir,
            env=clean_env,
            timeout_sec=time_limit_sec,
        )

        if timed_out:
            return {
                "passed": False,
                "verdict": "Time Limit Exceeded",
                "execution_time_ms": time_limit_sec * 1000,
                "actual_output": None,
                "expected_output": expected_output if is_sample else None,
                "input_data": input_data if is_sample else None,
                "error_message": f"Time limit exceeded ({time_limit_sec}s).",
            }

        if returncode != 0:
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
        shutil.rmtree(temp_dir, ignore_errors=True)


JS_RUNNER_TEMPLATE = r"""
const fs = require('fs');
const vm = require('vm');

const rawInput = fs.readFileSync(0, 'utf8').trim();
const userCode = fs.readFileSync('solution.js', 'utf8');

let stdout = '';
const customConsole = {
    log: (...args) => { stdout += args.map(a => typeof a === 'object' ? JSON.stringify(a) : String(a)).join(' ') + '\n'; },
    error: (...args) => { console.error(...args); },
    warn: (...args) => { console.warn(...args); }
};

const sandbox = {
    console: customConsole,
    require: require,
    process: process,
    Buffer: Buffer,
    setTimeout: setTimeout,
    clearTimeout: clearTimeout,
    setInterval: setInterval,
    clearInterval: clearInterval,
};

try {
    const context = vm.createContext(sandbox);
    vm.runInContext(userCode, context);

    if (stdout.trim().length > 0) {
        process.stdout.write(stdout.trim());
        process.exit(0);
    }

    let targetFn = null;
    if (context.Solution && typeof context.Solution === 'function') {
        try {
            const inst = new context.Solution();
            const methods = Object.getOwnPropertyNames(Object.getPrototypeOf(inst)).filter(m => m !== 'constructor');
            if (methods.length > 0) targetFn = inst[methods[0]].bind(inst);
        } catch(e) {}
    }

    if (!targetFn) {
        const builtins = new Set(['console', 'require', 'process', 'Buffer', 'setTimeout', 'clearTimeout', 'setInterval', 'clearInterval']);
        for (const key of Object.keys(context)) {
            if (!builtins.has(key) && !key.startsWith('_') && typeof context[key] === 'function') {
                targetFn = context[key];
                break;
            }
        }
    }

    if (!targetFn) {
        process.stdout.write(stdout.trim());
        process.exit(0);
    }

    function parseArg(s) {
        s = s.trim();
        try { return JSON.parse(s); } catch(e) {}
        try { return eval('(' + s + ')'); } catch(e) {}
        return s;
    }

    const lines = rawInput.split(/\r?\n/).filter(l => l.trim().length > 0);
    let parsedArgs = lines.map(parseArg);

    let res;
    if (parsedArgs.length === targetFn.length) {
        res = targetFn(...parsedArgs);
    } else if (parsedArgs.length === 1 && targetFn.length > 1 && Array.isArray(parsedArgs[0])) {
        res = targetFn(...parsedArgs[0]);
    } else {
        res = targetFn(...parsedArgs);
    }

    if (res !== undefined) {
        if (typeof res === 'object') {
            process.stdout.write(JSON.stringify(res));
        } else {
            process.stdout.write(String(res));
        }
    }
} catch (e) {
    console.error(e.stack || e.message);
    process.exit(1);
}
"""


JAVA_RUNNER_TEMPLATE = r"""import java.io.*;
import java.lang.reflect.*;
import java.util.*;
import java.util.regex.*;

public class Runner {
    public static void main(String[] args) {
        try {
            BufferedReader reader = new BufferedReader(new InputStreamReader(System.in));
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                sb.append(line).append("\n");
            }
            String rawInput = sb.toString().trim();

            Class<?> solClass;
            try {
                solClass = Class.forName("Solution");
            } catch (ClassNotFoundException e) {
                System.err.println("Class Solution not found.");
                System.exit(1);
                return;
            }

            Method targetMethod = null;
            for (Method m : solClass.getDeclaredMethods()) {
                if (Modifier.isPublic(m.getModifiers()) && !m.getName().equals("main") && !m.isSynthetic()) {
                    targetMethod = m;
                    break;
                }
            }
            if (targetMethod == null) {
                for (Method m : solClass.getDeclaredMethods()) {
                    if (!m.getName().equals("main") && !m.isSynthetic()) {
                        targetMethod = m;
                        break;
                    }
                }
            }
            if (targetMethod == null) {
                for (Method m : solClass.getDeclaredMethods()) {
                    if (m.getName().equals("main")) { targetMethod = m; break; }
                }
                if (targetMethod != null) {
                    targetMethod.invoke(null, (Object) new String[0]);
                    return;
                }
                System.err.println("No executable method found in Solution class.");
                System.exit(1);
                return;
            }

            targetMethod.setAccessible(true);
            Object solInstance = null;
            if (!Modifier.isStatic(targetMethod.getModifiers())) {
                Constructor<?> ctor = solClass.getDeclaredConstructor();
                ctor.setAccessible(true);
                solInstance = ctor.newInstance();
            }

            Class<?>[] paramTypes = targetMethod.getParameterTypes();
            Object[] parsedArgs = parseArgs(rawInput, paramTypes);
            Object result = targetMethod.invoke(solInstance, parsedArgs);

            if (targetMethod.getReturnType().equals(Void.TYPE)) {
                if (parsedArgs.length > 0) printFormatted(parsedArgs[0]);
            } else {
                printFormatted(result);
            }
        } catch (InvocationTargetException ite) {
            Throwable cause = ite.getCause() != null ? ite.getCause() : ite;
            System.err.println(cause.getClass().getSimpleName() + ": " + cause.getMessage());
            cause.printStackTrace(System.err);
            System.exit(1);
        } catch (Exception e) {
            System.err.println(e.getClass().getSimpleName() + ": " + e.getMessage());
            e.printStackTrace(System.err);
            System.exit(1);
        }
    }

    private static Object[] parseArgs(String input, Class<?>[] types) {
        List<String> rawTokens = splitArguments(input, types.length);
        Object[] args = new Object[types.length];
        for (int i = 0; i < types.length; i++) {
            String token = i < rawTokens.size() ? rawTokens.get(i).trim() : "";
            args[i] = parseSingleArg(token, types[i]);
        }
        return args;
    }

    private static List<String> splitArguments(String input, int count) {
        List<String> result = new ArrayList<>();
        if (count <= 1) {
            result.add(input);
            return result;
        }
        String[] lines = input.split("\r?\n");
        List<String> nonBlank = new ArrayList<>();
        for (String l : lines) if (!l.trim().isEmpty()) nonBlank.add(l.trim());
        if (nonBlank.size() == count) {
            return nonBlank;
        }

        int depth = 0;
        StringBuilder current = new StringBuilder();
        for (int i = 0; i < input.length(); i++) {
            char c = input.charAt(i);
            if (c == '[' || c == '{' || c == '(') depth++;
            else if (c == ']' || c == '}' || c == ')') depth--;
            else if (c == ',' && depth == 0 && result.size() < count - 1) {
                result.add(current.toString().trim());
                current = new StringBuilder();
                continue;
            }
            current.append(c);
        }
        if (current.length() > 0) result.add(current.toString().trim());
        return result;
    }

    private static Object parseSingleArg(String s, Class<?> type) {
        s = s.trim();
        if (type == int.class || type == Integer.class) return Integer.parseInt(s);
        if (type == long.class || type == Long.class) return Long.parseLong(s);
        if (type == double.class || type == Double.class) return Double.parseDouble(s);
        if (type == boolean.class || type == Boolean.class) return Boolean.parseBoolean(s.toLowerCase());
        if (type == String.class) {
            if (s.startsWith("\"") && s.endsWith("\"") && s.length() >= 2) {
                return s.substring(1, s.length() - 1);
            }
            return s;
        }
        if (type == char.class || type == Character.class) {
            if (s.startsWith("'") && s.endsWith("'") && s.length() >= 2) return s.charAt(1);
            return s.length() > 0 ? s.charAt(0) : ' ';
        }
        if (type == int[].class) {
            return parseIntArray(s);
        }
        if (type == int[][].class) {
            return parseInt2DArray(s);
        }
        if (type == String[].class) {
            return parseStringArray(s);
        }
        if (type == char[].class) {
            return parseCharArray(s);
        }
        if (List.class.isAssignableFrom(type)) {
            return parseList(s);
        }
        return s;
    }

    private static int[] parseIntArray(String s) {
        s = s.trim();
        if (s.startsWith("[") && s.endsWith("]")) s = s.substring(1, s.length() - 1);
        if (s.trim().isEmpty()) return new int[0];
        String[] parts = s.split(",");
        int[] res = new int[parts.length];
        for (int i = 0; i < parts.length; i++) res[i] = Integer.parseInt(parts[i].trim());
        return res;
    }

    private static int[][] parseInt2DArray(String s) {
        s = s.trim();
        if (s.startsWith("[") && s.endsWith("]")) s = s.substring(1, s.length() - 1).trim();
        List<int[]> list = new ArrayList<>();
        Matcher m = Pattern.compile("\\[([^\\]]*)\\]").matcher(s);
        while (m.find()) {
            list.add(parseIntArray("[" + m.group(1) + "]"));
        }
        return list.toArray(new int[list.size()][]);
    }

    private static String[] parseStringArray(String s) {
        s = s.trim();
        if (s.startsWith("[") && s.endsWith("]")) s = s.substring(1, s.length() - 1);
        if (s.trim().isEmpty()) return new String[0];
        String[] parts = s.split(",");
        String[] res = new String[parts.length];
        for (int i = 0; i < parts.length; i++) {
            String p = parts[i].trim();
            if (p.startsWith("\"") && p.endsWith("\"") && p.length() >= 2) p = p.substring(1, p.length() - 1);
            res[i] = p;
        }
        return res;
    }

    private static char[] parseCharArray(String s) {
        s = s.trim();
        if (s.startsWith("[") && s.endsWith("]")) s = s.substring(1, s.length() - 1);
        if (s.trim().isEmpty()) return new char[0];
        String[] parts = s.split(",");
        char[] res = new char[parts.length];
        for (int i = 0; i < parts.length; i++) {
            String p = parts[i].trim();
            if (p.startsWith("'") && p.endsWith("'") && p.length() >= 2) p = p.substring(1, p.length() - 1);
            res[i] = p.length() > 0 ? p.charAt(0) : ' ';
        }
        return res;
    }

    private static List<Object> parseList(String s) {
        s = s.trim();
        if (s.startsWith("[") && s.endsWith("]")) s = s.substring(1, s.length() - 1);
        List<Object> list = new ArrayList<>();
        if (s.trim().isEmpty()) return list;
        String[] parts = s.split(",");
        for (String p : parts) {
            p = p.trim();
            try { list.add(Integer.parseInt(p)); }
            catch (Exception e) { list.add(p); }
        }
        return list;
    }

    private static void printFormatted(Object obj) {
        if (obj == null) {
            System.out.println("null");
        } else if (obj instanceof boolean[]) {
            System.out.println(Arrays.toString((boolean[]) obj));
        } else if (obj instanceof int[]) {
            System.out.println(Arrays.toString((int[]) obj));
        } else if (obj instanceof long[]) {
            System.out.println(Arrays.toString((long[]) obj));
        } else if (obj instanceof double[]) {
            System.out.println(Arrays.toString((double[]) obj));
        } else if (obj instanceof Object[]) {
            System.out.println(Arrays.deepToString((Object[]) obj));
        } else if (obj instanceof Boolean) {
            System.out.println(((Boolean) obj) ? "true" : "false");
        } else {
            System.out.println(obj.toString());
        }
    }
}
"""


async def execute_javascript_test_case(
    code: str,
    input_data: str,
    expected_output: str,
    is_sample: bool,
    time_limit_sec: float,
) -> Dict[str, Any]:
    """Execute JavaScript code using Node.js in an isolated directory with runner harness."""
    node_path = shutil.which("node")
    if not node_path:
        return {
            "passed": False,
            "verdict": "Compilation Error",
            "execution_time_ms": 0.0,
            "actual_output": None,
            "expected_output": expected_output if is_sample else None,
            "input_data": input_data if is_sample else None,
            "error_message": "Node.js runtime is not installed on server.",
        }

    temp_dir = tempfile.mkdtemp(prefix="coding_js_sandbox_")
    start_time = time.perf_counter()

    try:
        solution_path = os.path.join(temp_dir, "solution.js")
        runner_path = os.path.join(temp_dir, "runner.js")
        with open(solution_path, "w", encoding="utf-8") as f:
            f.write(code)
        with open(runner_path, "w", encoding="utf-8") as f:
            f.write(JS_RUNNER_TEMPLATE)

        clean_env = {
            "SYSTEMROOT": os.environ.get("SYSTEMROOT", "C:\\Windows"),
            "PATH": os.environ.get("PATH", ""),
        }

        # If code explicitly handles process.stdin, execute solution directly; otherwise use runner harness
        has_stdin_handling = any(k in code for k in ("process.stdin", "readline", "readFileSync(0"))
        exec_script = solution_path if has_stdin_handling else runner_path

        returncode, actual_output, stderr_text, timed_out, exec_time_ms = await asyncio.to_thread(
            run_subprocess_sync,
            cmd=[node_path, exec_script],
            input_str=input_data,
            cwd=temp_dir,
            env=clean_env,
            timeout_sec=time_limit_sec,
        )

        if timed_out:
            return {
                "passed": False,
                "verdict": "Time Limit Exceeded",
                "execution_time_ms": time_limit_sec * 1000,
                "actual_output": None,
                "expected_output": expected_output if is_sample else None,
                "input_data": input_data if is_sample else None,
                "error_message": f"Time limit exceeded ({time_limit_sec}s).",
            }

        if returncode != 0:
            verdict = "Compilation Error" if "SyntaxError" in stderr_text else "Runtime Error"
            return {
                "passed": False,
                "verdict": verdict,
                "execution_time_ms": exec_time_ms,
                "actual_output": None,
                "expected_output": expected_output if is_sample else None,
                "input_data": input_data if is_sample else None,
                "error_message": stderr_text.strip() or "JavaScript execution error.",
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
        shutil.rmtree(temp_dir, ignore_errors=True)


async def execute_java_test_case(
    code: str,
    input_data: str,
    expected_output: str,
    is_sample: bool,
    time_limit_sec: float,
) -> Dict[str, Any]:
    """Execute Java code with javac compilation and Runner.java reflection harness."""
    javac_path = shutil.which("javac")
    java_path = shutil.which("java")
    if not javac_path or not java_path:
        return {
            "passed": False,
            "verdict": "Compilation Error",
            "execution_time_ms": 0.0,
            "actual_output": None,
            "expected_output": expected_output if is_sample else None,
            "input_data": input_data if is_sample else None,
            "error_message": "Java compiler (javac) or runtime (java) is not installed on server.",
        }

    temp_dir = tempfile.mkdtemp(prefix="coding_java_sandbox_")
    start_time = time.perf_counter()

    try:
        # Determine class name
        class_match = re.search(r"(?:public\s+)?class\s+([A-Za-z0-9_]+)", code)
        class_name = class_match.group(1) if class_match else "Solution"

        # Check if code has a main method
        has_main = bool(re.search(r"public\s+static\s+void\s+main\s*\(", code))

        # Ensure class is not package-declared
        prepared_code = re.sub(r"package\s+[^;]+;", "", code)
        if not class_match:
            prepared_code = f"import java.util.*;\npublic class Solution {{\n{prepared_code}\n}}"
            class_name = "Solution"

        java_file_path = os.path.join(temp_dir, f"{class_name}.java")
        with open(java_file_path, "w", encoding="utf-8") as f:
            f.write(prepared_code)

        runner_file_path = os.path.join(temp_dir, "Runner.java")
        with open(runner_file_path, "w", encoding="utf-8") as f:
            f.write(JAVA_RUNNER_TEMPLATE)

        clean_env = {
            "SYSTEMROOT": os.environ.get("SYSTEMROOT", "C:\\Windows"),
            "PATH": os.environ.get("PATH", ""),
        }

        # Step 1: Compile
        compile_targets = [f"{class_name}.java"]
        if not has_main:
            compile_targets.append("Runner.java")

        c_rc, c_stdout, c_stderr, c_timed_out, _ = await asyncio.to_thread(
            run_subprocess_sync,
            cmd=[javac_path] + compile_targets,
            cwd=temp_dir,
            env=clean_env,
            timeout_sec=8.0,
        )

        if c_timed_out:
            return {
                "passed": False,
                "verdict": "Compilation Error",
                "execution_time_ms": 8000.0,
                "actual_output": None,
                "expected_output": expected_output if is_sample else None,
                "input_data": input_data if is_sample else None,
                "error_message": "Compilation timed out.",
            }

        if c_rc != 0:
            err_msg = c_stderr.strip()[:2000]
            return {
                "passed": False,
                "verdict": "Compilation Error",
                "execution_time_ms": 0.0,
                "actual_output": None,
                "expected_output": expected_output if is_sample else None,
                "input_data": input_data if is_sample else None,
                "error_message": err_msg or "Java compilation failed.",
            }

        # Step 2: Execute
        exec_class = class_name if has_main else "Runner"
        r_rc, actual_output, stderr_text, r_timed_out, exec_time_ms = await asyncio.to_thread(
            run_subprocess_sync,
            cmd=[java_path, exec_class],
            input_str=input_data,
            cwd=temp_dir,
            env=clean_env,
            timeout_sec=time_limit_sec,
        )

        if r_timed_out:
            return {
                "passed": False,
                "verdict": "Time Limit Exceeded",
                "execution_time_ms": time_limit_sec * 1000,
                "actual_output": None,
                "expected_output": expected_output if is_sample else None,
                "input_data": input_data if is_sample else None,
                "error_message": f"Time limit exceeded ({time_limit_sec}s).",
            }

        if r_rc != 0:
            return {
                "passed": False,
                "verdict": "Runtime Error",
                "execution_time_ms": exec_time_ms,
                "actual_output": None,
                "expected_output": expected_output if is_sample else None,
                "input_data": input_data if is_sample else None,
                "error_message": stderr_text.strip() or "Java runtime error.",
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
        shutil.rmtree(temp_dir, ignore_errors=True)


async def execute_cpp_test_case(
    code: str,
    input_data: str,
    expected_output: str,
    is_sample: bool,
    time_limit_sec: float,
) -> Dict[str, Any]:
    """Execute C++ code with g++/clang++ if installed, else return informative notice."""
    compiler_path = shutil.which("g++") or shutil.which("clang++")
    if not compiler_path:
        return {
            "passed": False,
            "verdict": "Compilation Error",
            "execution_time_ms": 0.0,
            "actual_output": None,
            "expected_output": expected_output if is_sample else None,
            "input_data": input_data if is_sample else None,
            "error_message": "Execution environment for language 'cpp' is not configured on this host. Compiler (g++/clang++) not found.",
        }

    temp_dir = tempfile.mkdtemp(prefix="coding_cpp_sandbox_")
    start_time = time.perf_counter()

    try:
        cpp_file_path = os.path.join(temp_dir, "solution.cpp")
        exe_file_path = os.path.join(temp_dir, "solution.exe")
        with open(cpp_file_path, "w", encoding="utf-8") as f:
            f.write(code)

        clean_env = {
            "SYSTEMROOT": os.environ.get("SYSTEMROOT", "C:\\Windows"),
            "PATH": os.environ.get("PATH", ""),
        }

        # Step 1: Compile
        c_rc, c_stdout, c_stderr, c_timed_out, _ = await asyncio.to_thread(
            run_subprocess_sync,
            cmd=[compiler_path, "-O2", "solution.cpp", "-o", "solution.exe"],
            cwd=temp_dir,
            env=clean_env,
            timeout_sec=8.0,
        )

        if c_timed_out:
            return {
                "passed": False,
                "verdict": "Compilation Error",
                "execution_time_ms": 8000.0,
                "actual_output": None,
                "expected_output": expected_output if is_sample else None,
                "input_data": input_data if is_sample else None,
                "error_message": "C++ compilation timed out.",
            }

        if c_rc != 0:
            err_msg = c_stderr.strip()[:2000]
            return {
                "passed": False,
                "verdict": "Compilation Error",
                "execution_time_ms": 0.0,
                "actual_output": None,
                "expected_output": expected_output if is_sample else None,
                "input_data": input_data if is_sample else None,
                "error_message": err_msg or "C++ compilation failed.",
            }

        # Step 2: Execute
        r_rc, actual_output, stderr_text, r_timed_out, exec_time_ms = await asyncio.to_thread(
            run_subprocess_sync,
            cmd=[exe_file_path],
            input_str=input_data,
            cwd=temp_dir,
            env=clean_env,
            timeout_sec=time_limit_sec,
        )

        if r_timed_out:
            return {
                "passed": False,
                "verdict": "Time Limit Exceeded",
                "execution_time_ms": time_limit_sec * 1000,
                "actual_output": None,
                "expected_output": expected_output if is_sample else None,
                "input_data": input_data if is_sample else None,
                "error_message": f"Time limit exceeded ({time_limit_sec}s).",
            }

        if r_rc != 0:
            return {
                "passed": False,
                "verdict": "Runtime Error",
                "execution_time_ms": exec_time_ms,
                "actual_output": None,
                "expected_output": expected_output if is_sample else None,
                "input_data": input_data if is_sample else None,
                "error_message": stderr_text.strip() or "C++ runtime error.",
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
    elif lang in ("javascript", "typescript"):
        return await execute_javascript_test_case(
            code=code,
            input_data=input_data,
            expected_output=expected_output,
            is_sample=is_sample,
            time_limit_sec=time_limit_sec,
        )
    elif lang == "java":
        return await execute_java_test_case(
            code=code,
            input_data=input_data,
            expected_output=expected_output,
            is_sample=is_sample,
            time_limit_sec=time_limit_sec,
        )
    elif lang in ("cpp", "c++"):
        return await execute_cpp_test_case(
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

                # Priority: Compilation Error > Runtime Error > Time Limit Exceeded > Wrong Answer
                if run_res["verdict"] == "Compilation Error":
                    overall_verdict = "Compilation Error"
                elif run_res["verdict"] == "Runtime Error" and overall_verdict != "Compilation Error":
                    overall_verdict = "Runtime Error"
                elif run_res["verdict"] == "Time Limit Exceeded" and overall_verdict not in ("Compilation Error", "Runtime Error"):
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
    question_id: Any,
    language: str,
    code: str,
    time_limit_sec: float = 2.0,
) -> Dict[str, Any]:
    """
    Interactive 'Run Code' endpoint:
    Executes code against ONLY sample test cases without persisting a submission record.
    """
    if isinstance(question_id, str):
        try:
            q_uuid = uuid.UUID(question_id)
            cond = (CodingQuestion.id == q_uuid)
        except ValueError:
            cond = (CodingQuestion.slug == question_id)
    else:
        cond = (CodingQuestion.id == question_id)

    q_stmt = (
        select(CodingQuestion)
        .options(selectinload(CodingQuestion.test_cases))
        .where(cond)
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
            elif run_res["verdict"] == "Runtime Error" and overall_verdict != "Compilation Error":
                overall_verdict = "Runtime Error"
            elif run_res["verdict"] == "Time Limit Exceeded" and overall_verdict not in ("Compilation Error", "Runtime Error"):
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
