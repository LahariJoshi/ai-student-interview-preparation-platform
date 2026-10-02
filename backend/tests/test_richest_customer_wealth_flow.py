"""
test_richest_customer_wealth_flow.py - Full end-to-end flow test for Member-2 Richest Customer Wealth problem.
Verifies:
1. Starter code returned without solution.
2. Reference solution and hidden test cases are not exposed.
3. Java Run Code with correct solution -> 2/2 passed.
4. Java Run Code with wrong solution -> Wrong Answer.
5. Java Run Code with syntax error -> Compilation Error.
6. Java Submit with correct solution -> Accepted (100%), saved in DB.
7. Java Submit with wrong solution -> Wrong Answer, saved in DB.
8. Submissions list returns the submission.
9. Submission details and score endpoint return verified metrics.
10. Student coding progress reflects the accepted submission.
"""

import uuid
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.coding import CodingQuestion, CodingSubmission, CodingResult
from seed_coding_questions import seed_questions_to_session

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture(autouse=True)
async def seed_db(db_session: AsyncSession):
    await seed_questions_to_session(db_session)


async def get_auth_cookies(async_client: AsyncClient, email: str = "wealth_student@example.com") -> dict:
    reg_payload = {
        "email": email,
        "password": "password123",
        "full_name": "Wealth Student",
    }
    res = await async_client.post("/api/v1/auth/register", json=reg_payload)
    assert res.status_code == 201
    return dict(res.cookies)


CORRECT_JAVA = """public class Solution {
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
}"""

WRONG_JAVA = """public class Solution {
    public int maximumWealth(int[][] accounts) {
        return 0;
    }
}"""

COMPILATION_ERROR_JAVA = """public class Solution {
    public int maximumWealth(int[][] accounts) {
        return ;
    }
}"""


async def test_richest_customer_wealth_question_security(async_client: AsyncClient):
    """Verify problem page exposes clean starter code and no reference solution or hidden tests."""
    res = await async_client.get("/api/v1/coding/questions/richest-customer-wealth")
    assert res.status_code == 200
    q = res.json()
    assert q["title"] == "Richest Customer Wealth"
    assert q["difficulty"] == "Easy"
    assert q["topic"] == "Matrix"

    starter = q["starter_code"]
    assert "java" in starter
    java_starter = starter["java"]
    # Must NOT contain solution logic
    assert "for (int[] row" not in java_starter
    assert "Math.max" not in java_starter
    assert "// Write your solution here" in java_starter

    py_starter = starter["python"]
    assert "max(sum(" not in py_starter
    assert "# Write your solution here" in py_starter

    # Test cases: only sample cases returned
    for tc in q["sample_test_cases"]:
        assert tc["is_sample"] is True

    # No hidden cases exposed
    assert "all_test_cases" not in q


async def test_java_run_code_scenarios(async_client: AsyncClient):
    """Verify Run Code for correct, wrong, and compilation error solutions."""
    cookies = await get_auth_cookies(async_client, "runner_test@example.com")

    # 1. Correct Java solution
    res_correct = await async_client.post(
        "/api/v1/coding/run",
        json={"question_id": "richest-customer-wealth", "language": "java", "code": CORRECT_JAVA},
        cookies=cookies,
    )
    assert res_correct.status_code == 200
    data_correct = res_correct.json()
    assert data_correct["verdict"] in ("Accepted", "Passed")
    assert data_correct["passed_test_cases"] == 2
    assert data_correct["total_test_cases"] == 2
    assert len(data_correct["test_cases"]) == 2
    for tc in data_correct["test_cases"]:
        assert tc["passed"] is True
        assert tc["verdict"] == "Passed"

    # 2. Wrong Java solution
    res_wrong = await async_client.post(
        "/api/v1/coding/run",
        json={"question_id": "richest-customer-wealth", "language": "java", "code": WRONG_JAVA},
        cookies=cookies,
    )
    assert res_wrong.status_code == 200
    data_wrong = res_wrong.json()
    assert data_wrong["verdict"] == "Wrong Answer"
    assert data_wrong["passed_test_cases"] == 0

    # 3. Compilation Error Java solution
    res_err = await async_client.post(
        "/api/v1/coding/run",
        json={"question_id": "richest-customer-wealth", "language": "java", "code": COMPILATION_ERROR_JAVA},
        cookies=cookies,
    )
    assert res_err.status_code == 200
    data_err = res_err.json()
    assert data_err["verdict"] == "Compilation Error"
    assert "error" in data_err["error_message"].lower()


async def test_java_submit_solution_lifecycle(async_client: AsyncClient, db_session: AsyncSession):
    """Verify complete submit, persistence, history, scoring, and progress flow."""
    cookies = await get_auth_cookies(async_client, "submitter@example.com")

    # 1. Submit Correct Solution
    sub_res = await async_client.post(
        "/api/v1/coding/submissions?evaluate=true",
        json={"question_id": "richest-customer-wealth", "language": "java", "code": CORRECT_JAVA},
        cookies=cookies,
    )
    assert sub_res.status_code in (200, 201)
    sub_data = sub_res.json()
    assert sub_data["status"] == "completed"
    assert sub_data["result"] is not None
    assert sub_data["result"]["verdict"] == "Accepted"
    assert sub_data["result"]["score"] == 100.0
    assert sub_data["result"]["passed_test_cases"] == sub_data["result"]["total_test_cases"]

    submission_id = sub_data["id"]

    # 2. Verify submission is persisted in database
    db_res = await db_session.execute(select(CodingSubmission).where(CodingSubmission.id == uuid.UUID(submission_id)))
    persisted_sub = db_res.scalar_one_or_none()
    assert persisted_sub is not None
    assert persisted_sub.status == "completed"

    # 3. Verify question submissions endpoint
    q_subs_res = await async_client.get(
        "/api/v1/coding/questions/richest-customer-wealth/submissions",
        cookies=cookies,
    )
    assert q_subs_res.status_code == 200
    q_subs = q_subs_res.json()
    assert q_subs["total_count"] >= 1
    assert q_subs["submissions"][0]["id"] == submission_id
    assert q_subs["submissions"][0]["verdict"] == "Accepted"

    # 4. Verify submission details by ID
    detail_res = await async_client.get(
        f"/api/v1/coding/submissions/{submission_id}",
        cookies=cookies,
    )
    assert detail_res.status_code == 200
    assert detail_res.json()["id"] == submission_id

    # 5. Verify score endpoint
    score_res = await async_client.get(
        f"/api/v1/coding/submissions/{submission_id}/score",
        cookies=cookies,
    )
    assert score_res.status_code == 200
    score_data = score_res.json()
    assert score_data["score"] == 100.0
    assert score_data["execution_status"] == "Accepted"
    assert score_data["topic"] == "Matrix"
    assert score_data["difficulty"] == "Easy"

    # 6. Verify student coding progress reflects the solve
    prog_res = await async_client.get(
        "/api/v1/coding/progress",
        cookies=cookies,
    )
    assert prog_res.status_code == 200
    prog_data = prog_res.json()
    assert prog_data["total_questions_solved"] >= 1
    assert prog_data["easy_solved"] >= 1

    # 7. Submit Wrong Solution
    wrong_sub_res = await async_client.post(
        "/api/v1/coding/submissions?evaluate=true",
        json={"question_id": "richest-customer-wealth", "language": "java", "code": WRONG_JAVA},
        cookies=cookies,
    )
    assert wrong_sub_res.status_code in (200, 201)
    wrong_sub_data = wrong_sub_res.json()
    assert wrong_sub_data["result"]["verdict"] == "Wrong Answer"
    assert wrong_sub_data["result"]["score"] == 0.0

    # 8. Check question submissions now has 2 submissions
    q_subs_res2 = await async_client.get(
        "/api/v1/coding/questions/richest-customer-wealth/submissions",
        cookies=cookies,
    )
    assert q_subs_res2.status_code == 200
    assert q_subs_res2.json()["total_count"] == 2


async def test_python_run_and_submit_scenarios(async_client: AsyncClient, db_session: AsyncSession):
    """Verify complete Python run, submit, and error scenarios."""
    cookies = await get_auth_cookies(async_client, "py_student@example.com")

    correct_py = "def maximumWealth(accounts: list[list[int]]) -> int:\n    return max(sum(row) for row in accounts)"
    wrong_py = "def maximumWealth(accounts: list[list[int]]) -> int:\n    return 0"
    runtime_err_py = "def maximumWealth(accounts: list[list[int]]) -> int:\n    return 1 / 0"
    syntax_err_py = "def maximumWealth(accounts: list[list[int]]) -> int:\n    return def"

    # 1. Python Run Code - Correct
    res_correct = await async_client.post(
        "/api/v1/coding/run",
        json={"question_id": "richest-customer-wealth", "language": "python", "code": correct_py},
        cookies=cookies,
    )
    assert res_correct.status_code == 200
    d_correct = res_correct.json()
    assert d_correct["verdict"] in ("Accepted", "Passed")
    assert d_correct["passed_test_cases"] == 2
    assert d_correct["total_test_cases"] == 2
    assert d_correct["execution_time_ms"] > 0

    # 2. Python Run Code - Wrong
    res_wrong = await async_client.post(
        "/api/v1/coding/run",
        json={"question_id": "richest-customer-wealth", "language": "python", "code": wrong_py},
        cookies=cookies,
    )
    assert res_wrong.status_code == 200
    assert res_wrong.json()["verdict"] == "Wrong Answer"
    assert res_wrong.json()["passed_test_cases"] == 0

    # 3. Python Run Code - Runtime Error
    res_rt = await async_client.post(
        "/api/v1/coding/run",
        json={"question_id": "richest-customer-wealth", "language": "python", "code": runtime_err_py},
        cookies=cookies,
    )
    assert res_rt.status_code == 200
    d_rt = res_rt.json()
    assert d_rt["verdict"] == "Runtime Error"
    assert "ZeroDivisionError" in d_rt["error_message"]

    # 4. Python Run Code - Syntax/Compilation Error
    res_syn = await async_client.post(
        "/api/v1/coding/run",
        json={"question_id": "richest-customer-wealth", "language": "python", "code": syntax_err_py},
        cookies=cookies,
    )
    assert res_syn.status_code == 200
    assert res_syn.json()["verdict"] == "Compilation Error"

    # 5. Python Submit - Correct Solution
    sub_res = await async_client.post(
        "/api/v1/coding/submissions?evaluate=true",
        json={"question_id": "richest-customer-wealth", "language": "python", "code": correct_py},
        cookies=cookies,
    )
    assert sub_res.status_code in (200, 201)
    sub_d = sub_res.json()
    assert sub_d["status"] == "completed"
    assert sub_d["result"]["verdict"] == "Accepted"
    assert sub_d["result"]["score"] == 100.0
    assert sub_d["result"]["passed_test_cases"] == sub_d["result"]["total_test_cases"]
    assert sub_d["result"]["total_test_cases"] >= 2

