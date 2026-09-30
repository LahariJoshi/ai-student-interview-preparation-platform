import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.coding import (
    CodingQuestion,
    CodingTestCase,
    CodingSubmission,
    CodingResult,
)
from app.modules.coding.services.performance_service import (
    compute_submission_score,
    get_proficiency_label,
)

pytestmark = pytest.mark.asyncio


async def register_student(async_client: AsyncClient, email: str = "perf_student@example.com") -> dict:
    """Helper to register a student and return session cookies."""
    async_client.cookies.clear()
    payload = {
        "email": email,
        "password": "password123",
        "full_name": "Performance Student",
    }
    res = await async_client.post("/api/v1/auth/register", json=payload)
    assert res.status_code == 201
    return dict(res.cookies)


async def seed_questions(db: AsyncSession) -> dict:
    """Seed questions across different topics and difficulties."""
    q_easy_array = CodingQuestion(
        id=uuid.uuid4(),
        title="Two Sum",
        slug="two-sum",
        description="Find indices summing to target",
        difficulty="Easy",
        topic="Arrays",
    )
    q_med_array = CodingQuestion(
        id=uuid.uuid4(),
        title="3Sum",
        slug="3sum",
        description="Find triplets summing to zero",
        difficulty="Medium",
        topic="Arrays",
    )
    q_easy_string = CodingQuestion(
        id=uuid.uuid4(),
        title="Valid Palindrome",
        slug="valid-palindrome",
        description="Check if string is palindrome",
        difficulty="Easy",
        topic="Strings",
    )
    q_hard_dp = CodingQuestion(
        id=uuid.uuid4(),
        title="Edit Distance",
        slug="edit-distance",
        description="Minimum operations to convert string",
        difficulty="Hard",
        topic="Dynamic Programming",
    )
    db.add_all([q_easy_array, q_med_array, q_easy_string, q_hard_dp])
    await db.commit()
    for q in [q_easy_array, q_med_array, q_easy_string, q_hard_dp]:
        await db.refresh(q)

    return {
        "easy_array": q_easy_array,
        "med_array": q_med_array,
        "easy_string": q_easy_string,
        "hard_dp": q_hard_dp,
    }


# ============================================================================
# UNIT TESTS: SCORING ENGINE
# ============================================================================

async def test_compute_submission_score_cases():
    """Test unit scoring calculation across full, partial, zero, and boundary cases."""
    # 1. Full score (10/10)
    assert compute_submission_score(10, 10) == 100.0

    # 2. Partial score (3/4 = 75.0)
    assert compute_submission_score(3, 4) == 75.0

    # 3. Partial score (1/3 = 33.3)
    assert compute_submission_score(1, 3) == 33.3

    # 4. Zero passed (0/5)
    assert compute_submission_score(0, 5) == 0.0

    # 5. Zero total test cases edge case -> 0.0 without division by zero
    assert compute_submission_score(0, 0) == 0.0
    assert compute_submission_score(5, 0) == 0.0

    # 6. Negative or out of bounds clamped safely
    assert compute_submission_score(-2, 10) == 0.0
    assert compute_submission_score(15, 10) == 100.0


async def test_proficiency_label_classification():
    """Test proficiency level labeling logic."""
    assert get_proficiency_label(solved=0, attempted=0, avg_score=0.0) == "Not Started"
    assert get_proficiency_label(solved=0, attempted=3, avg_score=35.0) == "Needs Practice"
    assert get_proficiency_label(solved=1, attempted=3, avg_score=55.0) == "Developing"
    assert get_proficiency_label(solved=3, attempted=3, avg_score=85.0) == "Proficient"
    assert get_proficiency_label(solved=5, attempted=5, avg_score=95.0) == "Mastered"


# ============================================================================
# INTEGRATION TESTS: SUBMISSION SCORE ENDPOINT
# ============================================================================

async def test_get_submission_score_endpoint(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test GET /submissions/{id}/score returns normalized performance result."""
    questions = await seed_questions(db_session)
    q = questions["easy_array"]
    cookies = await register_student(async_client, "score_student@example.com")

    # Add test cases to question
    tc1 = CodingTestCase(
        id=uuid.uuid4(),
        question_id=q.id,
        input_data="[2, 7, 11, 15]\n9",
        expected_output="[0, 1]",
        is_sample=True,
        order_index=0,
    )
    tc2 = CodingTestCase(
        id=uuid.uuid4(),
        question_id=q.id,
        input_data="[3, 2, 4]\n6",
        expected_output="[1, 2]",
        is_sample=False,
        order_index=1,
    )
    db_session.add_all([tc1, tc2])
    await db_session.commit()

    # Submit solution and evaluate
    sub_res = await async_client.post(
        "/api/v1/coding/submissions?evaluate=true",
        json={
            "question_id": str(q.id),
            "language": "python",
            "code": "def twoSum(nums, target):\n    lookup = {}\n    for i, n in enumerate(nums):\n        if target - n in lookup:\n            return [lookup[target - n], i]\n        lookup[n] = i\n    return []",
        },
        cookies=cookies,
    )
    assert sub_res.status_code == 201
    sub_id = sub_res.json()["id"]

    # Retrieve normalized score performance
    score_res = await async_client.get(
        f"/api/v1/coding/submissions/{sub_id}/score",
        cookies=cookies,
    )
    assert score_res.status_code == 200
    perf = score_res.json()

    assert perf["submission_id"] == sub_id
    assert perf["score"] == 100.0
    assert perf["passed_tests"] == 2
    assert perf["total_tests"] == 2
    assert perf["topic"] == "Arrays"
    assert perf["difficulty"] == "Easy"
    assert perf["execution_status"] == "Accepted"
    assert "coding_metrics" in perf
    assert perf["coding_metrics"]["execution_time_ms"] >= 0.0
    assert perf["coding_metrics"]["memory_kb"] > 0


async def test_submission_score_user_isolation(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test that student B cannot view student A's submission score."""
    questions = await seed_questions(db_session)
    q = questions["easy_array"]

    # Student A submits
    cookies_a = await register_student(async_client, "student_a_perf@example.com")
    sub_res = await async_client.post(
        "/api/v1/coding/submissions",
        json={"question_id": str(q.id), "language": "python", "code": "pass"},
        cookies=cookies_a,
    )
    sub_id = sub_res.json()["id"]

    # Student B attempts to access Student A's score -> 403 Forbidden
    cookies_b = await register_student(async_client, "student_b_perf@example.com")
    res = await async_client.get(
        f"/api/v1/coding/submissions/{sub_id}/score",
        cookies=cookies_b,
    )
    assert res.status_code == 403
    assert "You can only view your own submission performance" in res.json()["detail"]


# ============================================================================
# INTEGRATION TESTS: PROGRESS & PERFORMANCE ANALYTICS
# ============================================================================

async def test_empty_student_performance_analytics(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test analytics endpoints return zeroed/neutral structures for student with no submissions."""
    await seed_questions(db_session)
    cookies = await register_student(async_client, "new_student@example.com")

    # 1. Progress
    res_prog = await async_client.get("/api/v1/coding/progress", cookies=cookies)
    assert res_prog.status_code == 200
    prog = res_prog.json()
    assert prog["total_questions_in_bank"] >= 4
    assert prog["total_questions_attempted"] == 0
    assert prog["total_questions_solved"] == 0
    assert prog["solve_rate_percentage"] == 0.0
    assert prog["overall_coding_score"] == 0.0
    assert prog["weak_topics"] == []

    # 2. Topic performance
    res_topics = await async_client.get("/api/v1/coding/performance/topics", cookies=cookies)
    assert res_topics.status_code == 200
    topics = res_topics.json()
    assert len(topics) >= 3
    for t in topics:
        assert t["questions_attempted"] == 0
        assert t["questions_solved"] == 0
        assert t["proficiency_level"] == "Not Started"

    # 3. Difficulties
    res_diff = await async_client.get("/api/v1/coding/performance/difficulties", cookies=cookies)
    assert res_diff.status_code == 200
    diffs = res_diff.json()
    assert len(diffs) == 3
    for d in diffs:
        assert d["questions_attempted"] == 0
        assert d["questions_solved"] == 0

    # 4. Weak topics (empty when 0 attempts)
    res_weak = await async_client.get("/api/v1/coding/performance/weak-topics", cookies=cookies)
    assert res_weak.status_code == 200
    assert res_weak.json() == []

    # 5. History (empty)
    res_hist = await async_client.get("/api/v1/coding/performance/history", cookies=cookies)
    assert res_hist.status_code == 200
    assert res_hist.json() == []

    # 6. Recommendation context
    res_rec = await async_client.get("/api/v1/coding/performance/recommendation-context", cookies=cookies)
    assert res_rec.status_code == 200
    rec = res_rec.json()
    assert rec["coding_score"] == 0.0
    assert rec["weak_topics"] == []
    assert rec["proficiency_level"] == "Beginner"


async def test_full_student_performance_flow(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """
    Test complete performance analytics with multiple questions:
    - 1 Easy Array question: Solved (score 100)
    - 1 Easy String question: Attempted & Failed (score 0) -> Weak Topic
    - 1 Medium Array question: Partial Score (score 50)
    Verify topic, difficulty, weak topics, progress, history, and recommendation bundle.
    """
    q_map = await seed_questions(db_session)
    q_arr_easy = q_map["easy_array"]
    q_str_easy = q_map["easy_string"]
    q_arr_med = q_map["med_array"]

    cookies = await register_student(async_client, "active_coder@example.com")

    # Get student UUID
    me_res = await async_client.get("/api/v1/auth/me", cookies=cookies)
    user_id = uuid.UUID(me_res.json()["id"])

    # Create manual submission & result records to verify analytics calculation directly
    # 1. Easy Array: Passed (score 100)
    sub1 = CodingSubmission(
        id=uuid.uuid4(),
        user_id=user_id,
        question_id=q_arr_easy.id,
        language="python",
        code="def solve(): return True",
        status="completed",
    )
    res1 = CodingResult(
        id=uuid.uuid4(),
        submission_id=sub1.id,
        verdict="Accepted",
        score=100.0,
        passed_test_cases=4,
        total_test_cases=4,
        execution_time_ms=12.5,
        memory_kb=12400.0,
    )
    sub1.result = res1

    # 2. Easy String: Failed (score 0.0) -> Wrong Answer
    sub2 = CodingSubmission(
        id=uuid.uuid4(),
        user_id=user_id,
        question_id=q_str_easy.id,
        language="python",
        code="def solve(): return False",
        status="completed",
    )
    res2 = CodingResult(
        id=uuid.uuid4(),
        submission_id=sub2.id,
        verdict="Wrong Answer",
        score=0.0,
        passed_test_cases=0,
        total_test_cases=3,
        execution_time_ms=15.0,
        memory_kb=12400.0,
    )
    sub2.result = res2

    # 3. Medium Array: Partial (score 50.0) -> Wrong Answer
    sub3 = CodingSubmission(
        id=uuid.uuid4(),
        user_id=user_id,
        question_id=q_arr_med.id,
        language="python",
        code="def solve(): return [1]",
        status="completed",
    )
    res3 = CodingResult(
        id=uuid.uuid4(),
        submission_id=sub3.id,
        verdict="Wrong Answer",
        score=50.0,
        passed_test_cases=2,
        total_test_cases=4,
        execution_time_ms=20.0,
        memory_kb=12400.0,
    )
    sub3.result = res3

    db_session.add_all([sub1, res1, sub2, res2, sub3, res3])
    await db_session.commit()

    # -------------------------------------------------------------
    # 1. Verify Topic-Wise Performance API
    # -------------------------------------------------------------
    res_topics = await async_client.get("/api/v1/coding/performance/topics", cookies=cookies)
    assert res_topics.status_code == 200
    topics_list = res_topics.json()
    topics_dict = {t["topic"]: t for t in topics_list}

    # Arrays: 2 attempted (q_arr_easy, q_arr_med), 1 solved (q_arr_easy), 2 submissions, avg_score = (100+50)/2 = 75.0
    assert "Arrays" in topics_dict
    arr_perf = topics_dict["Arrays"]
    assert arr_perf["questions_attempted"] == 2
    assert arr_perf["questions_solved"] == 1
    assert arr_perf["total_submissions"] == 2
    assert arr_perf["average_score"] == 75.0
    assert arr_perf["proficiency_level"] == "Proficient"

    # Strings: 1 attempted, 0 solved, 1 submission, avg_score = 0.0 -> Needs Practice
    assert "Strings" in topics_dict
    str_perf = topics_dict["Strings"]
    assert str_perf["questions_attempted"] == 1
    assert str_perf["questions_solved"] == 0
    assert str_perf["average_score"] == 0.0
    assert str_perf["proficiency_level"] == "Needs Practice"

    # -------------------------------------------------------------
    # 2. Verify Difficulty-Wise Performance API
    # -------------------------------------------------------------
    res_diff = await async_client.get("/api/v1/coding/performance/difficulties", cookies=cookies)
    assert res_diff.status_code == 200
    diff_list = res_diff.json()
    diff_dict = {d["difficulty"]: d for d in diff_list}

    # Easy: 2 attempted (q_arr_easy, q_str_easy), 1 solved (q_arr_easy) -> solve_rate = 50.0%
    assert "Easy" in diff_dict
    easy_perf = diff_dict["Easy"]
    assert easy_perf["questions_attempted"] == 2
    assert easy_perf["questions_solved"] == 1
    assert easy_perf["solve_rate_percentage"] == 50.0
    assert easy_perf["average_score"] == 50.0  # (100 + 0) / 2

    # Medium: 1 attempted (q_arr_med), 0 solved -> solve_rate = 0.0%
    assert "Medium" in diff_dict
    med_perf = diff_dict["Medium"]
    assert med_perf["questions_attempted"] == 1
    assert med_perf["questions_solved"] == 0
    assert med_perf["average_score"] == 50.0

    # Hard: 0 attempted
    assert "Hard" in diff_dict
    assert diff_dict["Hard"]["questions_attempted"] == 0
    assert diff_dict["Hard"]["questions_solved"] == 0

    # -------------------------------------------------------------
    # 3. Verify Weak-Topic Identification API
    # -------------------------------------------------------------
    res_weak = await async_client.get("/api/v1/coding/performance/weak-topics", cookies=cookies)
    assert res_weak.status_code == 200
    weak_list = res_weak.json()

    # Strings should be ranked weakest (avg score 0.0)
    assert len(weak_list) >= 1
    weak_topic_names = [w["topic"] for w in weak_list]
    assert "Strings" in weak_topic_names
    str_weak = [w for w in weak_list if w["topic"] == "Strings"][0]
    assert str_weak["questions_solved"] == 0
    assert "Priority practice required in Strings" in str_weak["recommended_focus"]

    # -------------------------------------------------------------
    # 4. Verify Overall Coding Progress API
    # -------------------------------------------------------------
    res_prog = await async_client.get("/api/v1/coding/performance/progress", cookies=cookies)
    assert res_prog.status_code == 200
    prog = res_prog.json()

    assert prog["total_questions_attempted"] == 3
    assert prog["total_questions_solved"] == 1
    assert prog["total_submissions"] == 3
    # Overall score = (100 + 0 + 50) / 3 = 50.0
    assert prog["overall_coding_score"] == 50.0
    assert prog["easy_solved"] == 1
    assert prog["medium_solved"] == 0
    assert prog["hard_solved"] == 0
    assert "Strings" in prog["weak_topics"]

    # -------------------------------------------------------------
    # 5. Verify Coding History API
    # -------------------------------------------------------------
    res_hist = await async_client.get("/api/v1/coding/performance/history?limit=10", cookies=cookies)
    assert res_hist.status_code == 200
    hist = res_hist.json()
    assert len(hist) == 3
    # Verify fields in each history item
    for item in hist:
        assert "submission_id" in item
        assert "question_title" in item
        assert "difficulty" in item
        assert "topic" in item
        assert "verdict" in item
        assert "score" in item
        assert "created_at" in item

    # -------------------------------------------------------------
    # 6. Verify Recommendation Engine Context API
    # -------------------------------------------------------------
    res_rec = await async_client.get("/api/v1/coding/performance/recommendation-context", cookies=cookies)
    assert res_rec.status_code == 200
    rec = res_rec.json()

    assert rec["coding_score"] == 50.0
    assert "Strings" in rec["weak_topics"]
    assert "difficulty_performance" in rec
    assert "Easy" in rec["difficulty_performance"]
    assert "Medium" in rec["difficulty_performance"]
    assert "Hard" in rec["difficulty_performance"]
    assert rec["total_solved"] == 1
    assert rec["total_attempted"] == 3
    assert rec["proficiency_level"] == "Beginner"


async def test_get_submission_score_not_found(async_client: AsyncClient):
    """Test retrieving score for non-existent submission returns 404."""
    cookies = await register_student(async_client, "not_found_tester@example.com")
    fake_id = uuid.uuid4()
    res = await async_client.get(
        f"/api/v1/coding/submissions/{fake_id}/score",
        cookies=cookies,
    )
    assert res.status_code == 404
    assert "Coding submission not found" in res.json()["detail"]


async def test_weak_topics_threshold_parameter(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test that weak-topics threshold filtering adjusts flagged topics."""
    q_map = await seed_questions(db_session)
    q_arr = q_map["med_array"]

    cookies = await register_student(async_client, "threshold_tester@example.com")
    me_res = await async_client.get("/api/v1/auth/me", cookies=cookies)
    user_id = uuid.UUID(me_res.json()["id"])

    # Create submission with score 60.0
    sub = CodingSubmission(
        id=uuid.uuid4(),
        user_id=user_id,
        question_id=q_arr.id,
        language="python",
        code="def solve(): pass",
        status="completed",
    )
    res = CodingResult(
        id=uuid.uuid4(),
        submission_id=sub.id,
        verdict="Wrong Answer",
        score=60.0,
        passed_test_cases=3,
        total_test_cases=5,
        execution_time_ms=10.0,
        memory_kb=12400.0,
    )
    sub.result = res
    db_session.add_all([sub, res])
    await db_session.commit()

    # 1. Threshold 50.0 -> score 60.0 is above threshold -> NOT weak
    res_low = await async_client.get("/api/v1/coding/performance/weak-topics?threshold=50.0", cookies=cookies)
    assert res_low.status_code == 200
    assert len(res_low.json()) == 0

    # 2. Threshold 70.0 -> score 60.0 is below threshold -> FLAGGED as weak
    res_high = await async_client.get("/api/v1/coding/performance/weak-topics?threshold=70.0", cookies=cookies)
    assert res_high.status_code == 200
    assert len(res_high.json()) == 1
    assert res_high.json()[0]["topic"] == "Arrays"


async def test_history_limit_parameter(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test that history limit parameter caps returned results."""
    q_map = await seed_questions(db_session)
    q = q_map["easy_array"]

    cookies = await register_student(async_client, "history_limiter@example.com")
    me_res = await async_client.get("/api/v1/auth/me", cookies=cookies)
    user_id = uuid.UUID(me_res.json()["id"])

    # Create 5 submissions
    subs = []
    for i in range(5):
        s = CodingSubmission(
            id=uuid.uuid4(),
            user_id=user_id,
            question_id=q.id,
            language="python",
            code=f"# submission {i}",
            status="completed",
        )
        r = CodingResult(
            id=uuid.uuid4(),
            submission_id=s.id,
            verdict="Accepted",
            score=100.0,
            passed_test_cases=2,
            total_test_cases=2,
        )
        s.result = r
        subs.extend([s, r])
    db_session.add_all(subs)
    await db_session.commit()

    # Request limit=2
    res_lim2 = await async_client.get("/api/v1/coding/performance/history?limit=2", cookies=cookies)
    assert res_lim2.status_code == 200
    assert len(res_lim2.json()) == 2

    # Request limit=4
    res_lim4 = await async_client.get("/api/v1/coding/performance/history?limit=4", cookies=cookies)
    assert res_lim4.status_code == 200
    assert len(res_lim4.json()) == 4

