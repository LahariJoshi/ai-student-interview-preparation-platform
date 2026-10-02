import asyncio
import os
import sys

sys.path.insert(0, os.path.abspath("backend"))

from app.modules.coding.services.evaluation_service import execute_test_case

async def run_language_checks():
    print("=== Testing Python Execution ===")
    py_code = """
def maximumWealth(accounts: list[list[int]]) -> int:
    return max(sum(row) for row in accounts)
"""
    res_py1 = await execute_test_case(
        code=py_code,
        language="python",
        input_data="[[1,2,3],[3,2,1]]",
        expected_output="6",
        is_sample=True,
    )
    print("Python Case 1:", res_py1)
    assert res_py1["passed"] is True
    assert res_py1["verdict"] == "Passed"
    assert res_py1["actual_output"] == "6"

    res_py2 = await execute_test_case(
        code=py_code,
        language="python",
        input_data="[[1,5],[7,3],[3,5]]",
        expected_output="10",
        is_sample=True,
    )
    print("Python Case 2:", res_py2)
    assert res_py2["passed"] is True
    assert res_py2["actual_output"] == "10"
    print("PYTHON PASSED 2/2!")

    print("\n=== Testing Java Execution ===")
    java_code = """
public class Solution {
    public int maximumWealth(int[][] accounts) {
        int max = 0;
        for (int[] row : accounts) {
            int sum = 0;
            for (int x : row) {
                sum += x;
            }
            max = Math.max(max, sum);
        }
        return max;
    }
}
"""
    res_java1 = await execute_test_case(
        code=java_code,
        language="java",
        input_data="[[1,2,3],[3,2,1]]",
        expected_output="6",
        is_sample=True,
    )
    print("Java Case 1:", res_java1)
    assert res_java1["passed"] is True
    assert res_java1["actual_output"] == "6"

    res_java2 = await execute_test_case(
        code=java_code,
        language="java",
        input_data="[[1,5],[7,3],[3,5]]",
        expected_output="10",
        is_sample=True,
    )
    print("Java Case 2:", res_java2)
    assert res_java2["passed"] is True
    assert res_java2["actual_output"] == "10"
    print("JAVA PASSED 2/2!")

    print("\n=== Testing JavaScript Execution ===")
    js_code = """
function maximumWealth(accounts) {
    return Math.max(...accounts.map(row => row.reduce((a, b) => a + b, 0)));
}
"""
    res_js = await execute_test_case(
        code=js_code,
        language="javascript",
        input_data="[[1,2,3],[3,2,1]]",
        expected_output="6",
        is_sample=True,
    )
    print("JavaScript Case 1:", res_js)
    assert res_js["passed"] is True
    assert res_js["actual_output"] == "6"
    print("JAVASCRIPT PASSED!")

    print("\n=== Testing C++ Error Handling ===")
    res_cpp = await execute_test_case(
        code="int main() { return 0; }",
        language="cpp",
        input_data="[[1,2,3],[3,2,1]]",
        expected_output="6",
        is_sample=True,
    )
    print("C++ Notice:", res_cpp)
    assert res_cpp["verdict"] == "Compilation Error"
    assert "not configured on this host" in res_cpp["error_message"]
    print("C++ GRACEFUL NOTICE PASSED!")

if __name__ == "__main__":
    asyncio.run(run_language_checks())
