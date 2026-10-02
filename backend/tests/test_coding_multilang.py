"""
test_coding_multilang.py - Tests for multi-language execution support (Java, C++, JS, Python).
"""

import pytest
import shutil
from app.modules.coding.services.evaluation_service import (
    execute_test_case,
    execute_java_test_case,
    execute_cpp_test_case,
)


@pytest.mark.asyncio
async def test_java_execution_success():
    """Verify that Java code compiles and executes against test cases if JDK is available."""
    if not shutil.which("javac") or not shutil.which("java"):
        pytest.skip("Java compiler/runtime not available on this host.")

    code = """
import java.util.Scanner;

public class Solution {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        if (sc.hasNextInt()) {
            int a = sc.nextInt();
            int b = sc.nextInt();
            System.out.println(a + b);
        }
    }
}
"""
    result = await execute_test_case(
        code=code,
        language="java",
        input_data="3 5",
        expected_output="8",
        is_sample=True,
    )
    assert result["passed"] is True
    assert result["verdict"] == "Passed"
    assert result["actual_output"] == "8"


@pytest.mark.asyncio
async def test_java_compilation_error():
    """Verify that invalid Java code returns Compilation Error."""
    if not shutil.which("javac") or not shutil.which("java"):
        pytest.skip("Java compiler/runtime not available on this host.")

    code = "public class Solution { this is invalid syntax }"
    result = await execute_test_case(
        code=code,
        language="java",
        input_data="1 2",
        expected_output="3",
        is_sample=True,
    )
    assert result["passed"] is False
    assert result["verdict"] == "Compilation Error"
    assert "error" in result["error_message"].lower() or "syntax" in result["error_message"].lower()


@pytest.mark.asyncio
async def test_cpp_graceful_handling():
    """Verify that C++ execution returns structured message if g++ is not installed."""
    code = "#include <iostream>\nint main() { std::cout << 42; return 0; }"
    result = await execute_test_case(
        code=code,
        language="cpp",
        input_data="",
        expected_output="42",
        is_sample=True,
    )
    if not shutil.which("g++") and not shutil.which("clang++"):
        assert result["passed"] is False
        assert result["verdict"] == "Compilation Error"
        assert "cpp" in result["error_message"].lower()
    else:
        assert result["passed"] is True
        assert result["actual_output"] == "42"


@pytest.mark.asyncio
async def test_python_solution_class_support():
    """Verify that Python Solution class methods are automatically invoked."""
    code = """
class Solution:
    def add(self, a: int, b: int) -> int:
        return a + b
"""
    result = await execute_test_case(
        code=code,
        language="python",
        input_data="10\n20",
        expected_output="30",
        is_sample=True,
    )
    assert result["passed"] is True
    assert result["verdict"] == "Passed"
    assert result["actual_output"] == "30"
