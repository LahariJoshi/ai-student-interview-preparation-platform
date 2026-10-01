import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.coding import (
    CodingQuestion,
    CodingTestCase,
    CodingSubmission,
    CodingResult,
)

pytestmark = pytest.mark.asyncio


async def register_user(async_client: AsyncClient, email: str, name: str = "Test Student") -> dict:
    """Helper to register a user and return cookies."""
    async_client.cookies.clear()
    payload = {
        "email": email,
        "password": "Password123!",
        "full_name": name,
    }
    res = await async_client.post("/api/v1/auth/register", json=payload)
    assert res.status_code == 201, f"Registration failed: {res.text}"
    return dict(res.cookies)


async def create_test_question(
    db: AsyncSession,
    title: str = "History Test Problem",
    slug: str = "history-test-problem",
    topic: str = "Dynamic Programming",
    difficulty: str = "Medium",
) -> CodingQuestion:
    """Helper to insert a question with sample and hidden test cases."""
    q = CodingQuestion(
        id=uuid.uuid4(),
        title=title,
        slug=slug,
        description="Compute the optimal solution.",
        difficulty=difficulty,
        topic=topic,
        constraints="1 <= n <= 100",
        hints=["Consider memoization."],
        starter_code={"python": "def solve(n): pass"},
    )
    db.add(q)
    await db.flush()

    tc1 = CodingTestCase(
        id=uuid.uuid4(),
        question_id=q.id,
        input_data="3",
        expected_output="6",
        is_sample=True,
        explanation="Sample case 1",
        order_index=1,
    )
    tc2 = CodingTestCase(
        id=uuid.uuid4(),
        question_id=q.id,
        input_data="5",
        expected_output="120",
        is_sample=False,
        explanation=None,
        order_index=2,
    )
    db.add_all([tc1, tc2])
    await db.commit()
    await db.refresh(q)
    return q


async def test_empty_submission_history(async_client: AsyncClient):
    """Test that a newly registered student receives an empty submission history."""
    cookies = await register_user(async_client, "new_coder_hist@example.com")

    res = await async_client.get("/api/v1/coding/submissions", cookies=cookies)
    assert res.status_code == 200
    data = res.json()
    assert data["total_count"] == 0
    assert data["submissions"] == []
    assert data["page"] == 1
    assert data["total_pages"] == 1


async def test_submission_history_with_diagnostics(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """
    Test that submitting and evaluating code produces a full submission history item
    containing question title, topic, difficulty, score, verdict, and test case counts.
    """
    q = await create_test_question(db_session, "Climbing Stairs", "climbing-stairs", "Dynamic Programming", "Easy")
    cookies = await register_user(async_client, "stairs_coder@example.com")

    # Valid Python code
    python_code = "import sys\nn = int(sys.stdin.read().strip())\nif n == 3: print(6)\nelif n == 5: print(120)\n"

    # Submit with evaluate=True
    sub_payload = {
        "question_id": str(q.id),
        "language": "python",
        "code": python_code,
    }
    submit_res = await async_client.post(
        "/api/v1/coding/submissions?evaluate=true",
        json=sub_payload,
        cookies=cookies,
    )
    assert submit_res.status_code == 201
    submission_id = submit_res.json()["id"]

    # 1. Fetch from list submissions history
    hist_res = await async_client.get("/api/v1/coding/submissions", cookies=cookies)
    assert hist_res.status_code == 200
    hist_data = hist_res.json()
    assert hist_data["total_count"] >= 1

    item = next(s for s in hist_data["submissions"] if s["id"] == submission_id)
    assert item["question_title"] == "Climbing Stairs"
    assert item["question_topic"] == "Dynamic Programming"
    assert item["question_difficulty"] == "Easy"
    assert item["language"] == "python"
    assert item["status"] == "completed"
    assert item["verdict"] == "Accepted"
    assert item["score"] == 100.0
    assert item["passed_test_cases"] == 2
    assert item["total_test_cases"] == 2

    # 2. Fetch single submission diagnostic
    detail_res = await async_client.get(f"/api/v1/coding/submissions/{submission_id}", cookies=cookies)
    assert detail_res.status_code == 200
    detail = detail_res.json()
    assert detail["id"] == submission_id
    assert detail["result"] is not None
    assert detail["result"]["verdict"] == "Accepted"
    assert detail["result"]["score"] == 100.0
    assert detail["result"]["passed_test_cases"] == 2
    assert detail["result"]["total_test_cases"] == 2


async def test_user_isolation_on_submission_history_and_results(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """
    Test that Student B cannot view Student A's submission history,
    cannot view Student A's individual submission details, and cannot view Student A's score.
    """
    q = await create_test_question(db_session, "Isolation Q", "isolation-q")
    cookies_a = await register_user(async_client, "student_a_isolation@example.com")
    cookies_b = await register_user(async_client, "student_b_isolation@example.com")

    # Student A submits code
    sub_payload = {
        "question_id": str(q.id),
        "language": "python",
        "code": "print(42)",
    }
    sub_a_res = await async_client.post(
        "/api/v1/coding/submissions?evaluate=true",
        json=sub_payload,
        cookies=cookies_a,
    )
    assert sub_a_res.status_code == 201
    sub_a_id = sub_a_res.json()["id"]

    # Student B checks their own history - must be empty
    hist_b_res = await async_client.get("/api/v1/coding/submissions", cookies=cookies_b)
    assert hist_b_res.status_code == 200
    assert hist_b_res.json()["total_count"] == 0

    # Student B attempts to access Student A's submission detail by ID -> 404 Not Found (user isolation)
    detail_b_res = await async_client.get(f"/api/v1/coding/submissions/{sub_a_id}", cookies=cookies_b)
    assert detail_b_res.status_code == 404

    # Student B attempts to access Student A's score -> 403 Forbidden (user isolation)
    score_b_res = await async_client.get(f"/api/v1/coding/submissions/{sub_a_id}/score", cookies=cookies_b)
    assert score_b_res.status_code == 403


async def test_question_specific_submissions(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test retrieving submissions filtered by specific question ID."""
    q1 = await create_test_question(db_session, "Question One", "question-one")
    q2 = await create_test_question(db_session, "Question Two", "question-two")
    cookies = await register_user(async_client, "filtered_coder@example.com")

    # Submit to Q1
    await async_client.post(
        "/api/v1/coding/submissions",
        json={"question_id": str(q1.id), "language": "python", "code": "print(1)"},
        cookies=cookies,
    )
    # Submit to Q2
    await async_client.post(
        "/api/v1/coding/submissions",
        json={"question_id": str(q2.id), "language": "python", "code": "print(2)"},
        cookies=cookies,
    )

    # Filter by Q1
    res1 = await async_client.get(f"/api/v1/coding/questions/{q1.id}/submissions", cookies=cookies)
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["total_count"] == 1
    assert data1["submissions"][0]["question_id"] == str(q1.id)

    # Filter by Q2
    res2 = await async_client.get(f"/api/v1/coding/questions/{q2.id}/submissions", cookies=cookies)
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2["total_count"] == 1
    assert data2["submissions"][0]["question_id"] == str(q2.id)


async def test_normalized_score_performance_result(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test GET /api/v1/coding/submissions/{id}/score returns normalized performance schema."""
    q = await create_test_question(db_session, "Perf Question", "perf-question", "Graphs", "Hard")
    cookies = await register_user(async_client, "graph_coder@example.com")

    # Submit and evaluate
    sub_res = await async_client.post(
        "/api/v1/coding/submissions?evaluate=true",
        json={"question_id": str(q.id), "language": "python", "code": "print('wrong')"},
        cookies=cookies,
    )
    assert sub_res.status_code == 201
    sub_id = sub_res.json()["id"]

    score_res = await async_client.get(f"/api/v1/coding/submissions/{sub_id}/score", cookies=cookies)
    assert score_res.status_code == 200
    score_data = score_res.json()

    assert score_data["submission_id"] == sub_id
    assert "score" in score_data
    assert "passed_tests" in score_data
    assert "total_tests" in score_data
    assert score_data["topic"] == "Graphs"
    assert score_data["difficulty"] == "Hard"
    assert "execution_status" in score_data
    assert "coding_metrics" in score_data
    assert "execution_time_ms" in score_data["coding_metrics"]
    assert "memory_kb" in score_data["coding_metrics"]


async def test_coding_progress_and_analytics_integration(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test full progress and analytics pipeline integration for a student."""
    q = await create_test_question(db_session, "Analytics Problem", "analytics-problem", "Sorting", "Easy")
    cookies = await register_user(async_client, "analytics_student@example.com")

    # Submit an accepted solution
    await async_client.post(
        "/api/v1/coding/submissions?evaluate=true",
        json={"question_id": str(q.id), "language": "python", "code": "import sys\nn=int(sys.stdin.read().strip())\nif n==3: print(6)\nelif n==5: print(120)\n"},
        cookies=cookies,
    )

    # 1. Overall Progress
    prog_res = await async_client.get("/api/v1/coding/progress", cookies=cookies)
    assert prog_res.status_code == 200
    prog = prog_res.json()
    assert prog["total_questions_attempted"] >= 1
    assert prog["total_questions_solved"] >= 1
    assert prog["overall_coding_score"] > 0

    # 2. Topic Performance
    topic_res = await async_client.get("/api/v1/coding/performance/topics", cookies=cookies)
    assert topic_res.status_code == 200
    topics = topic_res.json()
    assert any(t["topic"] == "Sorting" for t in topics)

    # 3. Performance History
    hist_res = await async_client.get("/api/v1/coding/performance/history", cookies=cookies)
    assert hist_res.status_code == 200
    hist = hist_res.json()
    assert len(hist) >= 1
    assert hist[0]["question_title"] == "Analytics Problem"
    assert hist[0]["verdict"] == "Accepted"
