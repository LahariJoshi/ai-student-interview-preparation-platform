import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.user import User

pytestmark = pytest.mark.asyncio


async def get_student_cookies(async_client: AsyncClient, email: str = "tc_student@example.com") -> dict:
    """Helper to register and obtain auth session cookie for a student."""
    reg_payload = {
        "email": email,
        "password": "password123",
        "full_name": "Test Student",
    }
    response = await async_client.post("/api/v1/auth/register", json=reg_payload)
    assert response.status_code == 201
    return dict(response.cookies)


async def get_admin_cookies(async_client: AsyncClient, db_session: AsyncSession, email: str = "tc_admin@example.com") -> dict:
    """Helper to create an authenticated administrator user with role='admin'."""
    cookies = await get_student_cookies(async_client, email)
    res = await db_session.execute(select(User).where(User.email == email.lower()))
    user = res.scalar_one()
    user.role = "admin"
    await db_session.commit()
    return cookies


async def create_dummy_question(async_client: AsyncClient, admin_cookies: dict, title: str = "Two Sum") -> str:
    """Helper to create a question using admin credentials and return its ID."""
    payload = {
        "title": title,
        "description": "Find two indices that sum to target.",
        "difficulty": "Easy",
        "topic": "Arrays",
        "starter_code": {"python": "def two_sum(): pass"},
    }
    res = await async_client.post("/api/v1/coding/questions", json=payload, cookies=admin_cookies)
    assert res.status_code == 201
    return res.json()["id"]


async def test_test_case_full_lifecycle(async_client: AsyncClient, db_session: AsyncSession):
    """Test test case CRUD, batching, reordering, and verify hidden test cases are protected from students."""
    admin_cookies = await get_admin_cookies(async_client, db_session, "tc_admin_lifecycle@example.com")
    student_cookies = await get_student_cookies(async_client, "tc_student_lifecycle@example.com")
    question_id = await create_dummy_question(async_client, admin_cookies, "Test Case Lifecycle Problem")

    # 1. Admin adds single sample test case
    tc_single_payload = {
        "input_data": "[1, 2, 3]\r\n4",
        "expected_output": "[0, 2]\r\n",
        "is_sample": True,
        "explanation": "1 + 3 = 4",
        "order_index": 1,
    }
    single_res = await async_client.post(
        f"/api/v1/coding/questions/{question_id}/test-cases",
        json=tc_single_payload,
        cookies=admin_cookies,
    )
    assert single_res.status_code == 201
    single_data = single_res.json()
    assert single_data["input_data"] == "[1, 2, 3]\n4"  # Verifies CRLF normalization
    assert single_data["expected_output"] == "[0, 2]"   # Verifies trailing newline strip
    assert single_data["is_sample"] is True
    first_tc_id = single_data["id"]

    # 2. Admin adds batch test cases (mix of sample and hidden)
    batch_payload = {
        "test_cases": [
            {
                "input_data": "[3, 2, 4]\n6",
                "expected_output": "[1, 2]",
                "is_sample": True,
                "explanation": "2 + 4 = 6",
                "order_index": 2,
            },
            {
                "input_data": "[3, 3]\n6",
                "expected_output": "[0, 1]",
                "is_sample": False,
                "order_index": 3,
            },
            {
                "input_data": "[-1, -2, -3, -4, -5]\n-8",
                "expected_output": "[2, 4]",
                "is_sample": False,
                "order_index": 4,
            },
        ]
    }
    batch_res = await async_client.post(
        f"/api/v1/coding/questions/{question_id}/test-cases/batch",
        json=batch_payload,
        cookies=admin_cookies,
    )
    assert batch_res.status_code == 201
    batch_data = batch_res.json()
    assert len(batch_data) == 3
    hidden_tc_id = batch_data[0]["id"] if not batch_data[0]["is_sample"] else batch_data[1]["id"]

    # 3. Student tries to list all test cases -> 403 Forbidden (hidden test cases protected)
    student_all_res = await async_client.get(
        f"/api/v1/coding/questions/{question_id}/test-cases",
        cookies=student_cookies,
    )
    assert student_all_res.status_code == 403
    assert "Administrator access required" in student_all_res.json()["detail"]

    # 4. Student tries to fetch hidden test case directly -> 403 Forbidden
    student_tc_res = await async_client.get(
        f"/api/v1/coding/test-cases/{hidden_tc_id}",
        cookies=student_cookies,
    )
    assert student_tc_res.status_code == 403
    assert "Administrator access required" in student_tc_res.json()["detail"]

    # 5. Public / Student lists sample test cases -> 200 OK (only samples visible)
    samples_res = await async_client.get(
        f"/api/v1/coding/questions/{question_id}/test-cases/samples"
    )
    assert samples_res.status_code == 200
    samples_data = samples_res.json()
    assert len(samples_data) == 2
    assert all(c["is_sample"] is True for c in samples_data)

    # 6. Admin lists all test cases (both sample and hidden) -> 200 OK
    all_res = await async_client.get(
        f"/api/v1/coding/questions/{question_id}/test-cases",
        cookies=admin_cookies,
    )
    assert all_res.status_code == 200
    all_data = all_res.json()
    assert all_data["total_count"] == 4
    assert all_data["sample_count"] == 2
    # 7. Admin gets individual test case
    get_res = await async_client.get(
        f"/api/v1/coding/test-cases/{first_tc_id}",
        cookies=admin_cookies,
    )
    assert get_res.status_code == 200
    assert get_res.json()["id"] == first_tc_id

    # 8. Student cannot update test case -> 403 Forbidden
    student_update_res = await async_client.put(
        f"/api/v1/coding/test-cases/{first_tc_id}",
        json={"expected_output": "hacked"},
        cookies=student_cookies,
    )
    assert student_update_res.status_code == 403
    assert "Administrator access required" in student_update_res.json()["detail"]

    # 9. Admin updates test case -> 200 OK
    update_payload = {
        "expected_output": "[0, 2] updated",
        "explanation": "Updated explanation",
    }
    update_res = await async_client.put(
        f"/api/v1/coding/test-cases/{first_tc_id}",
        json=update_payload,
        cookies=admin_cookies,
    )
    assert update_res.status_code == 200
    assert update_res.json()["expected_output"] == "[0, 2] updated"
    assert update_res.json()["explanation"] == "Updated explanation"

    # 10. Student cannot reorder test cases -> 403 Forbidden
    reorder_payload = {
        "items": [
            {"id": first_tc_id, "order_index": 10},
            {"id": batch_data[0]["id"], "order_index": 1},
        ]
    }
    student_reorder_res = await async_client.put(
        f"/api/v1/coding/questions/{question_id}/test-cases/reorder",
        json=reorder_payload,
        cookies=student_cookies,
    )
    assert student_reorder_res.status_code == 403
    assert "Administrator access required" in student_reorder_res.json()["detail"]

    # 11. Admin reorders test cases -> 200 OK
    reorder_res = await async_client.put(
        f"/api/v1/coding/questions/{question_id}/test-cases/reorder",
        json=reorder_payload,
        cookies=admin_cookies,
    )
    assert reorder_res.status_code == 200
    reordered_cases = reorder_res.json()
    case_order_map = {c["id"]: c["order_index"] for c in reordered_cases}
    assert case_order_map[first_tc_id] == 10
    assert case_order_map[batch_data[0]["id"]] == 1

    # 12. Student cannot delete test case -> 403 Forbidden
    student_del_res = await async_client.delete(
        f"/api/v1/coding/test-cases/{first_tc_id}",
        cookies=student_cookies,
    )
    assert student_del_res.status_code == 403
    assert "Administrator access required" in student_del_res.json()["detail"]

    # 13. Admin deletes test case -> 200 OK
    del_res = await async_client.delete(
        f"/api/v1/coding/test-cases/{first_tc_id}",
        cookies=admin_cookies,
    )
    assert del_res.status_code == 200
    assert "deleted successfully" in del_res.json()["message"]

    # Verify deleted test case returns 404
    check_del = await async_client.get(
        f"/api/v1/coding/test-cases/{first_tc_id}",
        cookies=admin_cookies,
    )
    assert check_del.status_code == 404


async def test_test_case_error_handling(async_client: AsyncClient, db_session: AsyncSession):
    """Test unauthorized access, student forbidden checks, and nonexistent entity handling."""
    fake_uuid = uuid.uuid4()
    student_cookies = await get_student_cookies(async_client, "tc_err_student@example.com")
    admin_cookies = await get_admin_cookies(async_client, db_session, "tc_err_admin@example.com")

    # 1. Unauthorized access check (unauthenticated -> 401)
    async_client.cookies.clear()
    unauth_res = await async_client.post(
        f"/api/v1/coding/questions/{fake_uuid}/test-cases",
        json={"input_data": "1", "expected_output": "2"},
    )
    assert unauth_res.status_code == 401

    # 2. Student cannot add test cases -> 403 Forbidden
    student_post = await async_client.post(
        f"/api/v1/coding/questions/{fake_uuid}/test-cases",
        json={"input_data": "1", "expected_output": "2"},
        cookies=student_cookies,
    )
    assert student_post.status_code == 403
    assert "Administrator access required" in student_post.json()["detail"]

    # 3. Admin adds test case to nonexistent question -> 404 Not Found
    bad_q_res = await async_client.post(
        f"/api/v1/coding/questions/{fake_uuid}/test-cases",
        json={"input_data": "1", "expected_output": "2"},
        cookies=admin_cookies,
    )
    assert bad_q_res.status_code == 404
    assert "question not found" in bad_q_res.json()["detail"].lower()

    # 4. Admin gets nonexistent test case -> 404 Not Found
    bad_tc_res = await async_client.get(
        f"/api/v1/coding/test-cases/{fake_uuid}",
        cookies=admin_cookies,
    )
    assert bad_tc_res.status_code == 404
