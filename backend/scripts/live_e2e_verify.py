import requests
import json
import sys

BASE_URL = "http://127.0.0.1:8000/api/v1"

def run_live_verification():
    session = requests.Session()

    print("1. Registering live test user...")
    email = f"live_verify_user_{hash(BASE_URL)}@example.com"
    reg_res = session.post(f"{BASE_URL}/auth/register", json={
        "email": email,
        "password": "password123",
        "full_name": "Live Verify User"
    })
    if reg_res.status_code not in (200, 201):
        print(f"Register response: {reg_res.status_code}, trying login...")
        login_res = session.post(f"{BASE_URL}/auth/login", json={
            "email": email,
            "password": "password123"
        })
        assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    print("User authenticated successfully.")

    print("\n2. Fetching Richest Customer Wealth question...")
    q_res = session.get(f"{BASE_URL}/coding/questions/richest-customer-wealth")
    assert q_res.status_code == 200, f"Get question failed: {q_res.text}"
    q_data = q_res.json()
    print(f"Title: {q_data['title']}, Difficulty: {q_data['difficulty']}")
    assert "java" in q_data["starter_code"]
    assert "python" in q_data["starter_code"]
    assert "for (int[] row" not in q_data["starter_code"]["java"]
    assert "reference_solution" not in q_data
    print("Clean starter code verified. No reference solution leaked.")

    print("\n3. Testing Python Run Code (Correct)...")
    py_correct = "def maximumWealth(accounts: list[list[int]]) -> int:\n    return max(sum(row) for row in accounts)"
    run_py = session.post(f"{BASE_URL}/coding/run", json={
        "question_id": "richest-customer-wealth",
        "language": "python",
        "code": py_correct
    })
    assert run_py.status_code == 200, f"Run Python failed: {run_py.text}"
    run_py_data = run_py.json()
    print("Python Run Result:", json.dumps(run_py_data, indent=2))
    assert run_py_data["verdict"] in ("Accepted", "Passed")
    assert run_py_data["passed_test_cases"] == 2
    assert run_py_data["total_test_cases"] == 2
    assert run_py_data["execution_time_ms"] > 0
    print("Python Run Code PASSED 2/2!")

    print("\n4. Testing Python Run Code (Wrong)...")
    run_wrong = session.post(f"{BASE_URL}/coding/run", json={
        "question_id": "richest-customer-wealth",
        "language": "python",
        "code": "def maximumWealth(accounts: list[list[int]]) -> int:\n    return 0"
    })
    assert run_wrong.status_code == 200
    assert run_wrong.json()["verdict"] == "Wrong Answer"
    assert run_wrong.json()["passed_test_cases"] == 0
    print("Python Wrong Answer PASSED!")

    print("\n5. Testing Python Run Code (Compilation Error)...")
    run_syntax = session.post(f"{BASE_URL}/coding/run", json={
        "question_id": "richest-customer-wealth",
        "language": "python",
        "code": "def maximumWealth(accounts: list[list[int]]) -> int:\n    return def"
    })
    assert run_syntax.status_code == 200
    assert run_syntax.json()["verdict"] == "Compilation Error"
    print("Python Compilation Error PASSED!")

    print("\n6. Testing Java Run Code (Correct)...")
    java_correct = """public class Solution {
    public int maximumWealth(int[][] accounts) {
        int max = 0;
        for (int[] row : accounts) {
            int sum = 0;
            for (int x : row) sum += x;
            max = Math.max(max, sum);
        }
        return max;
    }
}"""
    run_java = session.post(f"{BASE_URL}/coding/run", json={
        "question_id": "richest-customer-wealth",
        "language": "java",
        "code": java_correct
    })
    assert run_java.status_code == 200, f"Run Java failed: {run_java.text}"
    run_java_data = run_java.json()
    print("Java Run Result:", json.dumps(run_java_data, indent=2))
    assert run_java_data["verdict"] in ("Accepted", "Passed")
    assert run_java_data["passed_test_cases"] == 2
    print("Java Run Code PASSED 2/2!")

    print("\n7. Submitting Java Solution...")
    sub_res = session.post(f"{BASE_URL}/coding/submissions?evaluate=true", json={
        "question_id": "richest-customer-wealth",
        "language": "java",
        "code": java_correct
    })
    assert sub_res.status_code in (200, 201), f"Submit failed: {sub_res.text}"
    sub_data = sub_res.json()
    print("Submission Result:", json.dumps(sub_data["result"], indent=2))
    assert sub_data["status"] == "completed"
    assert sub_data["result"]["verdict"] == "Accepted"
    assert sub_data["result"]["score"] == 100.0
    submission_id = sub_data["id"]
    print(f"Java submission accepted with 100% score! ID: {submission_id}")

    print("\n8. Checking Question Submissions Tab...")
    subs_list_res = session.get(f"{BASE_URL}/coding/questions/richest-customer-wealth/submissions")
    assert subs_list_res.status_code == 200
    subs_list = subs_list_res.json()
    print(f"Total question submissions: {subs_list['total_count']}")
    assert subs_list["total_count"] >= 1
    assert any(s["id"] == submission_id for s in subs_list["submissions"])
    print("Question submissions list verified!")

    print("\n9. Checking Student Progress / Analytics...")
    prog_res = session.get(f"{BASE_URL}/coding/progress")
    assert prog_res.status_code == 200
    prog = prog_res.json()
    print("Student Progress:", json.dumps(prog, indent=2))
    assert prog["total_questions_solved"] >= 1
    assert prog["easy_solved"] >= 1
    print("Progress analytics verified!")

    print("\n=======================================================")
    print("ALL LIVE END-TO-END FLOW CHECKS PASSED WITH FLYING COLORS!")
    print("=======================================================")

if __name__ == "__main__":
    run_live_verification()
