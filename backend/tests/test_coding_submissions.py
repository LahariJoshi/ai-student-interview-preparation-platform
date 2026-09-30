import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.coding import (
    CodingQuestion,
    CodingTestCase,
    CodingSubmission,
)
import app.modules.coding.services.submission_service as sub_service
from app.modules.coding.schemas import SubmissionCreate

pytestmark = pytest.mark.asyncio


async def register_student(async_client: AsyncClient, email: str = "submitter@example.com") -> dict:
    """Helper to register a student and return session cookies."""
    async_client.cookies.clear()
    payload = {
        "email": email,
        "password": "password123",
        "full_name": "Submitter Student",
    }
    res = await async_client.post("/api/v1/auth/register", json=payload)
    assert res.status_code == 201
    return dict(res.cookies)


async def create_sample_question(db: AsyncSession, title: str = "Two Sum", slug: str = "two-sum") -> CodingQuestion:
    """Helper to create a sample question in the database."""
    q = CodingQuestion(
        id=uuid.uuid4(),
        title=title,
        slug=slug,
        description="Find indices of two numbers that add up to target.",
        difficulty="Easy",
        topic="Arrays",
        constraints="2 <= nums.length <= 10^4",
        hints=["Use a dictionary to store seen values."],
        starter_code={"python": "def twoSum(nums, target): pass"},
    )
    db.add(q)
    await db.commit()
    await db.refresh(q)
    return q


async def test_create_submission_success(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test successful submission creation for an authenticated student."""
    question = await create_sample_question(db_session)
    cookies = await register_student(async_client, "successful_coder@example.com")

    # Get student info
    me_res = await async_client.get("/api/v1/auth/me", cookies=cookies)
    assert me_res.status_code == 200
    student_id = me_res.json()["id"]

    sub_payload = {
        "question_id": str(question.id),
        "language": "python",
        "code": "def twoSum(nums, target):\n    seen = {}\n    for i, n in enumerate(nums):\n        diff = target - n\n        if diff in seen:\n            return [seen[diff], i]\n        seen[n] = i\n    return []",
    }

    res = await async_client.post(
        "/api/v1/coding/submissions",
        json=sub_payload,
        cookies=cookies,
    )
    assert res.status_code == 201
    data = res.json()

    assert "id" in data
    assert data["user_id"] == student_id
    assert data["question_id"] == str(question.id)
    assert data["language"] == "python"
    assert data["status"] == "pending"
    assert data["code"] == sub_payload["code"]
    assert data["question_title"] == "Two Sum"
    assert data["question_slug"] == "two-sum"
    assert data["question_difficulty"] == "Easy"
    assert data["question_topic"] == "Arrays"
    assert data["result"] is None
    assert "created_at" in data


async def test_create_submission_unauthenticated(async_client: AsyncClient, db_session: AsyncSession):
    """Test that submitting code without authentication returns 401."""
    question = await create_sample_question(db_session, "Unauth Question", "unauth-q")
    async_client.cookies.clear()

    sub_payload = {
        "question_id": str(question.id),
        "language": "python",
        "code": "print('hello')",
    }

    res = await async_client.post(
        "/api/v1/coding/submissions",
        json=sub_payload,
    )
    assert res.status_code == 401


async def test_create_submission_invalid_question(async_client: AsyncClient):
    """Test submitting code for a non-existent question returns 404."""
    cookies = await register_student(async_client, "invalid_q@example.com")

    fake_id = str(uuid.uuid4())
    sub_payload = {
        "question_id": fake_id,
        "language": "python",
        "code": "print('hello')",
    }

    res = await async_client.post(
        "/api/v1/coding/submissions",
        json=sub_payload,
        cookies=cookies,
    )
    assert res.status_code == 404
    assert "Coding question not found" in res.json()["detail"]


async def test_create_submission_invalid_language(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test submitting code with an unsupported language returns 422."""
    question = await create_sample_question(db_session, "Lang Question", "lang-q")
    cookies = await register_student(async_client, "bad_lang@example.com")

    sub_payload = {
        "question_id": str(question.id),
        "language": "ruby",
        "code": "puts 'hello'",
    }

    res = await async_client.post(
        "/api/v1/coding/submissions",
        json=sub_payload,
        cookies=cookies,
    )
    assert res.status_code == 422
    assert "Language 'ruby' is not supported" in str(res.json())


async def test_create_submission_empty_code(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test submitting empty or whitespace-only code returns 422."""
    question = await create_sample_question(db_session, "Empty Code Q", "empty-code-q")
    cookies = await register_student(async_client, "empty_code@example.com")

    # Pure whitespace code
    sub_payload = {
        "question_id": str(question.id),
        "language": "python",
        "code": "   \n\t  ",
    }

    res = await async_client.post(
        "/api/v1/coding/submissions",
        json=sub_payload,
        cookies=cookies,
    )
    assert res.status_code == 422
    assert "Submitted code cannot be empty" in str(res.json())


async def test_get_submission_by_id_and_user_isolation(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test individual submission retrieval and strict user isolation."""
    question = await create_sample_question(db_session, "Isolation Q", "isolation-q")

    # User A creates a submission
    cookies_a = await register_student(async_client, "student_a@example.com")
    sub_payload = {
        "question_id": str(question.id),
        "language": "javascript",
        "code": "function solve() { return true; }",
    }
    create_res = await async_client.post(
        "/api/v1/coding/submissions",
        json=sub_payload,
        cookies=cookies_a,
    )
    assert create_res.status_code == 201
    sub_id = create_res.json()["id"]

    # 1. User A retrieves their own submission
    get_res_a = await async_client.get(
        f"/api/v1/coding/submissions/{sub_id}",
        cookies=cookies_a,
    )
    assert get_res_a.status_code == 200
    assert get_res_a.json()["id"] == sub_id
    assert get_res_a.json()["language"] == "javascript"

    # 2. User B attempts to access User A's submission -> 404 (user isolation)
    cookies_b = await register_student(async_client, "student_b@example.com")
    get_res_b = await async_client.get(
        f"/api/v1/coding/submissions/{sub_id}",
        cookies=cookies_b,
    )
    assert get_res_b.status_code == 404

    # 3. Non-existent submission ID -> 404
    fake_sub_id = str(uuid.uuid4())
    get_fake = await async_client.get(
        f"/api/v1/coding/submissions/{fake_sub_id}",
        cookies=cookies_a,
    )
    assert get_fake.status_code == 404


async def test_list_user_submissions_and_pagination(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test listing user submissions, filtering by question/status, and pagination."""
    q1 = await create_sample_question(db_session, "Question 1", "q-1")
    q2 = await create_sample_question(db_session, "Question 2", "q-2")

    cookies = await register_student(async_client, "multi_submit@example.com")

    # Create 3 submissions: 2 for q1, 1 for q2
    await async_client.post(
        "/api/v1/coding/submissions",
        json={"question_id": str(q1.id), "language": "python", "code": "pass"},
        cookies=cookies,
    )
    await async_client.post(
        "/api/v1/coding/submissions",
        json={"question_id": str(q1.id), "language": "cpp", "code": "int main() {}"},
        cookies=cookies,
    )
    await async_client.post(
        "/api/v1/coding/submissions",
        json={"question_id": str(q2.id), "language": "java", "code": "class Solution {}"},
        cookies=cookies,
    )

    # 1. List all submissions for current user
    res_all = await async_client.get("/api/v1/coding/submissions", cookies=cookies)
    assert res_all.status_code == 200
    d_all = res_all.json()
    assert d_all["total_count"] == 3
    assert len(d_all["submissions"]) == 3

    # 2. Filter by question_id
    res_q1 = await async_client.get(f"/api/v1/coding/submissions?question_id={q1.id}", cookies=cookies)
    assert res_q1.status_code == 200
    d_q1 = res_q1.json()
    assert d_q1["total_count"] == 2
    assert len(d_q1["submissions"]) == 2
    for s in d_q1["submissions"]:
        assert s["question_id"] == str(q1.id)

    # 3. Filter by status
    res_status = await async_client.get("/api/v1/coding/submissions?status=pending", cookies=cookies)
    assert res_status.status_code == 200
    assert res_status.json()["total_count"] == 3

    # Invalid status filter -> 400
    res_bad_status = await async_client.get("/api/v1/coding/submissions?status=bogus", cookies=cookies)
    assert res_bad_status.status_code == 400

    # 4. Pagination
    res_p1 = await async_client.get("/api/v1/coding/submissions?page=1&limit=2", cookies=cookies)
    assert res_p1.status_code == 200
    d_p1 = res_p1.json()
    assert d_p1["total_count"] == 3
    assert d_p1["page"] == 1
    assert d_p1["limit"] == 2
    assert d_p1["total_pages"] == 2
    assert len(d_p1["submissions"]) == 2

    res_p2 = await async_client.get("/api/v1/coding/submissions?page=2&limit=2", cookies=cookies)
    assert res_p2.status_code == 200
    d_p2 = res_p2.json()
    assert d_p2["page"] == 2
    assert len(d_p2["submissions"]) == 1


async def test_question_specific_submissions_endpoint(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """Test GET /questions/{question_id}/submissions endpoint."""
    q = await create_sample_question(db_session, "History Q", "history-q")
    cookies = await register_student(async_client, "history_coder@example.com")

    # Initially empty
    res_empty = await async_client.get(
        f"/api/v1/coding/questions/{q.id}/submissions",
        cookies=cookies,
    )
    assert res_empty.status_code == 200
    assert res_empty.json()["total_count"] == 0

    # Submit 1 solution
    await async_client.post(
        "/api/v1/coding/submissions",
        json={"question_id": str(q.id), "language": "python", "code": "def solve(): return 42"},
        cookies=cookies,
    )

    res_sub = await async_client.get(
        f"/api/v1/coding/questions/{q.id}/submissions",
        cookies=cookies,
    )
    assert res_sub.status_code == 200
    assert res_sub.json()["total_count"] == 1
    assert res_sub.json()["submissions"][0]["question_slug"] == "history-q"


async def test_submission_lifecycle_status_service(db_session: AsyncSession):
    """Test submission status lifecycle transitions in service layer."""
    q = await create_sample_question(db_session, "Lifecycle Q", "lifecycle-q")
    fake_user_id = uuid.uuid4()

    # Create submission directly through service
    data = SubmissionCreate(
        question_id=q.id,
        language="python",
        code="def solve(): pass",
    )
    sub_dict = await sub_service.create_submission(db_session, fake_user_id, data)
    assert sub_dict["status"] == "pending"
    sub_id = sub_dict["id"]

    # Transition to running
    running_sub = await sub_service.update_submission_status(db_session, sub_id, "running")
    assert running_sub.status == "running"

    # Transition to completed
    completed_sub = await sub_service.update_submission_status(db_session, sub_id, "completed")
    assert completed_sub.status == "completed"

    # Transition to failed
    failed_sub = await sub_service.update_submission_status(db_session, sub_id, "failed")
    assert failed_sub.status == "failed"

    # Invalid status transition raises 400
    with pytest.raises(Exception) as exc_info:
        await sub_service.update_submission_status(db_session, sub_id, "unknown_status")
    assert "Invalid submission status" in str(exc_info.value)
