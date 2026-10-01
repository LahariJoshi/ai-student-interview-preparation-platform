import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.user import User

pytestmark = pytest.mark.asyncio


async def get_student_cookies(async_client: AsyncClient, email: str = "coder@example.com") -> dict:
    """Helper to register and obtain auth session cookie for a student."""
    reg_payload = {
        "email": email,
        "password": "password123",
        "full_name": "Coding Student",
    }
    response = await async_client.post("/api/v1/auth/register", json=reg_payload)
    assert response.status_code == 201
    return dict(response.cookies)


async def get_admin_cookies(async_client: AsyncClient, db_session: AsyncSession, email: str = "admin@example.com") -> dict:
    """Helper to create an authenticated administrator user with role='admin'."""
    cookies = await get_student_cookies(async_client, email)
    res = await db_session.execute(select(User).where(User.email == email.lower()))
    user = res.scalar_one()
    user.role = "admin"
    await db_session.commit()
    return cookies


async def test_question_topics_and_difficulties(async_client: AsyncClient):
    """Test standard public endpoints for difficulties and topics."""
    diff_res = await async_client.get("/api/v1/coding/questions/difficulties")
    assert diff_res.status_code == 200
    assert diff_res.json() == ["Easy", "Medium", "Hard"]

    topics_res = await async_client.get("/api/v1/coding/questions/topics")
    assert topics_res.status_code == 200
    assert isinstance(topics_res.json(), list)


async def test_create_question_full_lifecycle(async_client: AsyncClient, db_session: AsyncSession):
    """Test administrator question CRUD and verify hidden test cases are never leaked to students."""
    admin_cookies = await get_admin_cookies(async_client, db_session, "admin_lifecycle@example.com")
    student_cookies = await get_student_cookies(async_client, "student_lifecycle@example.com")

    # 1. Admin creates Question with Sample and Hidden test cases
    create_payload = {
        "title": "Valid Palindrome",
        "slug": "valid-palindrome",
        "description": "A phrase is a palindrome if it reads the same forward and backward.",
        "difficulty": "Easy",
        "topic": "Strings",
        "constraints": "1 <= s.length <= 2 * 10^5",
        "hints": ["Consider using two pointers from both ends."],
        "starter_code": {
            "python": "def isPalindrome(s: str) -> bool:\n    pass"
        },
        "test_cases": [
            {
                "input_data": '"A man, a plan, a canal: Panama"',
                "expected_output": "true",
                "is_sample": True,
                "explanation": '"amanaplanacanalpanama" is a palindrome.',
                "order_index": 1,
            },
            {
                "input_data": '"race a car"',
                "expected_output": "false",
                "is_sample": True,
                "explanation": '"raceacar" is not a palindrome.',
                "order_index": 2,
            },
            {
                "input_data": '"secret_hidden_input"',
                "expected_output": "true",
                "is_sample": False,
                "order_index": 3,
            },
        ],
    }

    create_res = await async_client.post(
        "/api/v1/coding/questions",
        json=create_payload,
        cookies=admin_cookies,
    )
    assert create_res.status_code == 201
    q_data = create_res.json()
    assert q_data["title"] == "Valid Palindrome"
    assert q_data["slug"] == "valid-palindrome"
    assert q_data["difficulty"] == "Easy"
    assert q_data["topic"] == "Strings"
    assert len(q_data["sample_test_cases"]) == 2  # Only sample test cases returned in public view
    question_id = q_data["id"]

    # 2. Duplicate slug error test
    dup_res = await async_client.post(
        "/api/v1/coding/questions",
        json=create_payload,
        cookies=admin_cookies,
    )
    assert dup_res.status_code == 400
    assert "already exists" in dup_res.json()["detail"]

    # 3. Retrieve by slug as student - verify hidden test cases are NOT leaked
    get_slug_res = await async_client.get(
        "/api/v1/coding/questions/valid-palindrome",
        cookies=student_cookies,
    )
    assert get_slug_res.status_code == 200
    assert get_slug_res.json()["id"] == question_id
    assert len(get_slug_res.json()["sample_test_cases"]) == 2
    assert not any("secret_hidden_input" in tc.get("input_data", "") for tc in get_slug_res.json()["sample_test_cases"])

    # 4. Retrieve by ID as student
    get_id_res = await async_client.get(
        f"/api/v1/coding/questions/{question_id}",
        cookies=student_cookies,
    )
    assert get_id_res.status_code == 200
    assert get_id_res.json()["slug"] == "valid-palindrome"

    # 5. List questions with filtering (public / student)
    list_res = await async_client.get(
        "/api/v1/coding/questions?topic=Strings&difficulty=Easy"
    )
    assert list_res.status_code == 200
    list_data = list_res.json()
    assert list_data["total_count"] >= 1
    matched = [q for q in list_data["questions"] if q["id"] == question_id]
    assert len(matched) == 1
    assert matched[0]["sample_test_case_count"] == 2

    # Search filter
    search_res = await async_client.get(
        "/api/v1/coding/questions?search=palindrome"
    )
    assert search_res.status_code == 200
    assert search_res.json()["total_count"] >= 1

    # 6. Admin updates question
    update_payload = {
        "difficulty": "Medium",
        "description": "Updated palindrome description.",
    }
    update_res = await async_client.put(
        f"/api/v1/coding/questions/{question_id}",
        json=update_payload,
        cookies=admin_cookies,
    )
    assert update_res.status_code == 200
    assert update_res.json()["difficulty"] == "Medium"
    assert update_res.json()["description"] == "Updated palindrome description."

    # 7. Admin adds additional test case
    add_tc_payload = {
        "input_data": '"0P"',
        "expected_output": "false",
        "is_sample": True,
        "explanation": '"0p" is not a palindrome.',
        "order_index": 4,
    }
    tc_res = await async_client.post(
        f"/api/v1/coding/questions/{question_id}/test-cases",
        json=add_tc_payload,
        cookies=admin_cookies,
    )
    assert tc_res.status_code == 201
    new_tc_id = tc_res.json()["id"]

    # Verify updated sample count
    get_after_tc = await async_client.get(f"/api/v1/coding/questions/{question_id}")
    assert len(get_after_tc.json()["sample_test_cases"]) == 3

    # 8. Admin deletes test case
    del_tc_res = await async_client.delete(
        f"/api/v1/coding/test-cases/{new_tc_id}",
        cookies=admin_cookies,
    )
    assert del_tc_res.status_code == 200
    assert "deleted successfully" in del_tc_res.json()["message"]

    # 9. Admin deletes question
    del_q_res = await async_client.delete(
        f"/api/v1/coding/questions/{question_id}",
        cookies=admin_cookies,
    )
    assert del_q_res.status_code == 200

    # Verify 404 after deletion
    check_404 = await async_client.get(f"/api/v1/coding/questions/{question_id}")
    assert check_404.status_code == 404


async def test_question_unauthorized_access(async_client: AsyncClient, db_session: AsyncSession):
    """Mutating question bank requires administrator privileges; student access is forbidden."""
    student_cookies = await get_student_cookies(async_client, "unauth_q_student@example.com")
    fake_id = uuid.uuid4()

    # Read public
    get_res = await async_client.get("/api/v1/coding/questions")
    assert get_res.status_code == 200

    # 2. Unauthenticated user POST -> 401
    async_client.cookies.clear()
    post_unauth = await async_client.post(
        "/api/v1/coding/questions",
        json={"title": "Test", "description": "Desc", "difficulty": "Easy", "topic": "Arrays"},
    )
    assert post_unauth.status_code == 401

    # Student cannot create questions -> 403 Forbidden
    post_student = await async_client.post(
        "/api/v1/coding/questions",
        json={"title": "Student Question", "description": "Desc", "difficulty": "Easy", "topic": "Arrays"},
        cookies=student_cookies,
    )
    assert post_student.status_code == 403
    assert "Administrator access required" in post_student.json()["detail"]

    # Student cannot update questions -> 403 Forbidden
    put_student = await async_client.put(
        f"/api/v1/coding/questions/{fake_id}",
        json={"title": "Updated Title"},
        cookies=student_cookies,
    )
    assert put_student.status_code == 403
    assert "Administrator access required" in put_student.json()["detail"]

    # Student cannot delete questions -> 403 Forbidden
    del_student = await async_client.delete(
        f"/api/v1/coding/questions/{fake_id}",
        cookies=student_cookies,
    )
    assert del_student.status_code == 403
    assert "Administrator access required" in del_student.json()["detail"]


async def test_question_validation_errors(async_client: AsyncClient, db_session: AsyncSession):
    """Test validation errors for invalid difficulty or empty fields using admin credentials."""
    admin_cookies = await get_admin_cookies(async_client, db_session, "val_errors_admin@example.com")

    # Invalid difficulty
    invalid_diff = {
        "title": "Invalid Diff Question",
        "description": "Desc",
        "difficulty": "SuperHard",
        "topic": "Arrays",
    }
    res = await async_client.post(
        "/api/v1/coding/questions",
        json=invalid_diff,
        cookies=admin_cookies,
    )
    assert res.status_code == 422
