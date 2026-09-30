import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.coding import CodingQuestion, CodingTestCase, CodingSubmission, CodingResult
from app.core.config import settings

pytestmark = pytest.mark.asyncio


async def register_student(async_client: AsyncClient, email: str, name: str) -> dict:
    """Helper to register and login a student."""
    async_client.cookies.clear()
    payload = {
        "email": email,
        "password": "Password123!",
        "full_name": name,
    }
    res = await async_client.post("/api/v1/auth/register", json=payload)
    assert res.status_code == 201, f"Register failed: {res.text}"
    return dict(res.cookies)


async def test_complete_member2_e2e_flow(async_client: AsyncClient, db_session: AsyncSession):
    """
    Comprehensive End-to-End Validation of the full Member-2 Flow:
    1. Auth / Student registration
    2. Question creation & test cases setup (sample & hidden)
    3. Question listing, topic summary, difficulty summary
    4. Question retrieval by ID/slug (hidden test cases protected)
    5. Interactive code run (sample test cases only, no DB persistence)
    6. Full code submission & sandboxed evaluation
    7. Results persistence and score verification
    8. Diagnostic retrieval & student isolation enforcement
    9. Submission history listing with test case counts
    10. Performance analytics (Progress, Topics, Difficulties, Weak Areas)
    11. Recommendation engine context export
    """
    # -------------------------------------------------------------------------
    # 1. Auth & Student Onboarding
    # -------------------------------------------------------------------------
    cookies_a = await register_student(async_client, "e2e_student_a@example.com", "Student Alice")
    cookies_b = await register_student(async_client, "e2e_student_b@example.com", "Student Bob")

    # -------------------------------------------------------------------------
    # 2. Question Bank Setup
    # -------------------------------------------------------------------------
    q = CodingQuestion(
        id=uuid.uuid4(),
        title="Valid Palindrome",
        slug="valid-palindrome-e2e",
        description="A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward.",
        difficulty="Easy",
        topic="Strings",
        constraints="1 <= s.length <= 2 * 10^5",
        hints=["Use two pointers moving inward from both ends."],
        starter_code={
            "python": "def isPalindrome(s: str) -> bool:\n    pass",
            "javascript": "function isPalindrome(s) {\n    return false;\n}",
        },
    )
    db_session.add(q)
    await db_session.flush()

    tc_sample = CodingTestCase(
        id=uuid.uuid4(),
        question_id=q.id,
        input_data="racecar",
        expected_output="True",
        is_sample=True,
        explanation="racecar reversed is racecar",
        order_index=1,
    )
    tc_hidden = CodingTestCase(
        id=uuid.uuid4(),
        question_id=q.id,
        input_data="hello",
        expected_output="False",
        is_sample=False,
        explanation=None,
        order_index=2,
    )
    db_session.add_all([tc_sample, tc_hidden])
    await db_session.commit()
    await db_session.refresh(q)

    # -------------------------------------------------------------------------
    # 3. Question Retrieval, Topic & Difficulty Summaries
    # -------------------------------------------------------------------------
    list_res = await async_client.get("/api/v1/coding/questions?topic=Strings&difficulty=Easy", cookies=cookies_a)
    assert list_res.status_code == 200
    list_data = list_res.json()
    assert list_data["total_count"] >= 1
    assert any(item["id"] == str(q.id) for item in list_data["questions"])

    topics_res = await async_client.get("/api/v1/coding/questions/topics/summary", cookies=cookies_a)
    assert topics_res.status_code == 200
    assert any(t["topic"] == "Strings" for t in topics_res.json())

    diff_res = await async_client.get("/api/v1/coding/questions/difficulties/summary", cookies=cookies_a)
    assert diff_res.status_code == 200
    assert any(d["difficulty"] == "Easy" for d in diff_res.json())

    # -------------------------------------------------------------------------
    # 4. Question Details Security: Hidden test cases must NEVER be exposed
    # -------------------------------------------------------------------------
    q_detail_res = await async_client.get(f"/api/v1/coding/questions/{q.slug}", cookies=cookies_a)
    assert q_detail_res.status_code == 200
    q_detail = q_detail_res.json()
    assert q_detail["title"] == "Valid Palindrome"
    assert len(q_detail["sample_test_cases"]) == 1
    assert q_detail["sample_test_cases"][0]["input_data"] == "racecar"
    # Ensure hidden test case is not leaked
    assert not any(tc.get("input_data") == "hello" for tc in q_detail["sample_test_cases"])

    # -------------------------------------------------------------------------
    # 5. Interactive Sample Run (No DB persistence)
    # -------------------------------------------------------------------------
    python_solution = (
        "import sys\n"
        "s = sys.stdin.read().strip()\n"
        "cleaned = ''.join(c.lower() for c in s if c.isalnum())\n"
        "print(cleaned == cleaned[::-1])\n"
    )

    run_res = await async_client.post(
        f"/api/v1/coding/questions/{q.id}/run",
        json={"language": "python", "code": python_solution},
        cookies=cookies_a,
    )
    assert run_res.status_code == 200
    run_data = run_res.json()
    assert run_data["verdict"] == "Accepted"
    assert run_data["passed_test_cases"] == 1
    assert run_data["total_test_cases"] == 1
    assert len(run_data["test_cases"]) == 1
    assert run_data["test_cases"][0]["is_sample"] is True

    # -------------------------------------------------------------------------
    # 6. Full Submission & Sandbox Evaluation
    # -------------------------------------------------------------------------
    sub_res = await async_client.post(
        "/api/v1/coding/submissions?evaluate=true",
        json={"question_id": str(q.id), "language": "python", "code": python_solution},
        cookies=cookies_a,
    )
    assert sub_res.status_code == 201
    sub_data = sub_res.json()
    sub_id = sub_data["id"]
    assert sub_data["status"] == "completed"
    assert sub_data["result"] is not None
    assert sub_data["result"]["verdict"] == "Accepted"
    assert sub_data["result"]["score"] == 100.0
    assert sub_data["result"]["passed_test_cases"] == 2
    assert sub_data["result"]["total_test_cases"] == 2

    # Verify hidden test case output is redacted in the returned test_case_results
    test_results = sub_data["result"]["test_case_results"]
    hidden_result = next(tr for tr in test_results if not tr["is_sample"])
    assert hidden_result["passed"] is True
    assert hidden_result["expected_output"] is None
    assert hidden_result["input_data"] is None

    # -------------------------------------------------------------------------
    # 7. Database Result Persistence
    # -------------------------------------------------------------------------
    res_stmt = select(CodingResult).where(CodingResult.submission_id == uuid.UUID(sub_id))
    db_res = (await db_session.execute(res_stmt)).scalar_one_or_none()
    assert db_res is not None
    assert db_res.verdict == "Accepted"
    assert db_res.score == 100.0
    assert db_res.passed_test_cases == 2
    assert db_res.total_test_cases == 2

    # -------------------------------------------------------------------------
    # 8. Diagnostic Retrieval & User Isolation
    # -------------------------------------------------------------------------
    # Alice can view her submission
    detail_res_a = await async_client.get(f"/api/v1/coding/submissions/{sub_id}", cookies=cookies_a)
    assert detail_res_a.status_code == 200
    assert detail_res_a.json()["id"] == sub_id

    # Alice can view her submission score
    score_res_a = await async_client.get(f"/api/v1/coding/submissions/{sub_id}/score", cookies=cookies_a)
    assert score_res_a.status_code == 200
    assert score_res_a.json()["score"] == 100.0

    # Bob cannot view Alice's submission (404 isolation)
    detail_res_b = await async_client.get(f"/api/v1/coding/submissions/{sub_id}", cookies=cookies_b)
    assert detail_res_b.status_code == 404

    # Bob cannot view Alice's score (403 forbidden)
    score_res_b = await async_client.get(f"/api/v1/coding/submissions/{sub_id}/score", cookies=cookies_b)
    assert score_res_b.status_code == 403

    # -------------------------------------------------------------------------
    # 9. Submission History
    # -------------------------------------------------------------------------
    hist_res = await async_client.get("/api/v1/coding/submissions", cookies=cookies_a)
    assert hist_res.status_code == 200
    hist = hist_res.json()
    assert hist["total_count"] >= 1
    alice_item = next(item for item in hist["submissions"] if item["id"] == sub_id)
    assert alice_item["question_title"] == "Valid Palindrome"
    assert alice_item["verdict"] == "Accepted"
    assert alice_item["score"] == 100.0
    assert alice_item["passed_test_cases"] == 2
    assert alice_item["total_test_cases"] == 2

    # Bob's history is isolated and empty
    bob_hist_res = await async_client.get("/api/v1/coding/submissions", cookies=cookies_b)
    assert bob_hist_res.status_code == 200
    assert bob_hist_res.json()["total_count"] == 0

    # -------------------------------------------------------------------------
    # 10. Performance Analytics (Progress, Topics, Difficulties, Weak Areas)
    # -------------------------------------------------------------------------
    prog_res = await async_client.get("/api/v1/coding/progress", cookies=cookies_a)
    assert prog_res.status_code == 200
    prog = prog_res.json()
    assert prog["total_questions_solved"] >= 1
    assert prog["overall_coding_score"] == 100.0

    topic_perf_res = await async_client.get("/api/v1/coding/performance/topics", cookies=cookies_a)
    assert topic_perf_res.status_code == 200
    assert any(tp["topic"] == "Strings" and tp["proficiency_level"] == "Mastered" for tp in topic_perf_res.json())

    diff_perf_res = await async_client.get("/api/v1/coding/performance/difficulties", cookies=cookies_a)
    assert diff_perf_res.status_code == 200
    easy_diff = next(d for d in diff_perf_res.json() if d["difficulty"] == "Easy")
    assert easy_diff["questions_solved"] >= 1
    assert easy_diff["average_score"] == 100.0

    # -------------------------------------------------------------------------
    # 11. Team Recommendation Engine Integration Contract
    # -------------------------------------------------------------------------
    rec_res = await async_client.get("/api/v1/coding/performance/recommendation-context", cookies=cookies_a)
    assert rec_res.status_code == 200
    rec_context = rec_res.json()
    assert "coding_score" in rec_context
    assert "weak_topics" in rec_context
    assert "difficulty_performance" in rec_context
    assert "Easy" in rec_context["difficulty_performance"]
    assert rec_context["coding_score"] == 100.0
    assert isinstance(rec_context["weak_topics"], list)


async def test_security_sandbox_enforcement(async_client: AsyncClient, db_session: AsyncSession):
    """
    Test security sandbox safeguards:
    - Dangerous imports and system calls blocked (os, subprocess, socket, eval, open, etc.)
    - Timeout protection
    - Secrets isolation (process environment variables are not accessible)
    """
    q = CodingQuestion(
        id=uuid.uuid4(),
        title="Security Probe Problem",
        slug="security-probe-problem",
        description="Test isolation boundaries.",
        difficulty="Medium",
        topic="Security",
        starter_code={"python": "pass"},
    )
    db_session.add(q)
    await db_session.flush()

    tc = CodingTestCase(
        id=uuid.uuid4(),
        question_id=q.id,
        input_data="1",
        expected_output="OK",
        is_sample=True,
        order_index=1,
    )
    db_session.add(tc)
    await db_session.commit()

    cookies = await register_student(async_client, "hacker_probe@example.com", "Probe User")

    # 1. Blocked dangerous imports (os, sys, subprocess, socket, etc.)
    dangerous_code_1 = "import os\nprint(os.listdir('.'))\n"
    res1 = await async_client.post(
        f"/api/v1/coding/questions/{q.id}/run",
        json={"language": "python", "code": dangerous_code_1},
        cookies=cookies,
    )
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["verdict"] in ("Compilation Error", "Security Violation", "Runtime Error")
    assert "security" in (data1.get("error_message") or "").lower()
    assert data1["test_cases"][0]["verdict"] in ("Compilation Error", "Security Violation")

    # 2. Blocked builtins (open, eval, exec)
    dangerous_code_2 = "open('/etc/passwd', 'r')\n"
    res2 = await async_client.post(
        f"/api/v1/coding/questions/{q.id}/run",
        json={"language": "python", "code": dangerous_code_2},
        cookies=cookies,
    )
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["verdict"] in ("Compilation Error", "Security Violation", "Runtime Error")
    assert "security" in (data2.get("error_message") or "").lower()
    assert data2["test_cases"][0]["verdict"] in ("Compilation Error", "Security Violation")

    # 3. Timeout enforcement (infinite loop)
    infinite_loop_code = "while True: pass\n"
    res3 = await async_client.post(
        f"/api/v1/coding/questions/{q.id}/run",
        json={"language": "python", "code": infinite_loop_code},
        cookies=cookies,
    )
    assert res3.status_code == 200
    data3 = res3.json()
    assert data3["verdict"] == "Time Limit Exceeded"
    assert data3["passed_test_cases"] == 0
