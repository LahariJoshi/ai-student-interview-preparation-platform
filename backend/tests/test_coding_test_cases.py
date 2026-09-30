import uuid
import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def get_auth_cookies(async_client: AsyncClient, email: str = "tc_admin@example.com") -> dict:
    """Helper to register and obtain auth session cookie."""
    reg_payload = {
        "email": email,
        "password": "password123",
        "full_name": "Test Case Manager",
    }
    response = await async_client.post("/api/v1/auth/register", json=reg_payload)
    assert response.status_code == 201
    return dict(response.cookies)


async def create_dummy_question(async_client: AsyncClient, cookies: dict, title: str = "Two Sum") -> str:
    """Helper to create a question and return its ID."""
    payload = {
        "title": title,
        "description": "Find two indices that sum to target.",
        "difficulty": "Easy",
        "topic": "Arrays",
        "starter_code": {"python": "def two_sum(): pass"},
    }
    res = await async_client.post("/api/v1/coding/questions", json=payload, cookies=cookies)
    assert res.status_code == 201
    return res.json()["id"]


async def test_test_case_full_lifecycle(async_client: AsyncClient):
    """Test full CRUD, batching, reordering, and sample filtering for test cases."""
    cookies = await get_auth_cookies(async_client, "tc_lifecycle@example.com")
    question_id = await create_dummy_question(async_client, cookies, "Test Case Lifecycle Problem")

    # 1. Add single sample test case
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
        cookies=cookies,
    )
    assert single_res.status_code == 201
    single_data = single_res.json()
    assert single_data["input_data"] == "[1, 2, 3]\n4"  # Verifies CRLF normalization
    assert single_data["expected_output"] == "[0, 2]"   # Verifies trailing newline strip
    assert single_data["is_sample"] is True
    first_tc_id = single_data["id"]

    # 2. Add batch test cases (mix of sample and hidden)
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
        cookies=cookies,
    )
    assert batch_res.status_code == 201
    batch_data = batch_res.json()
    assert len(batch_data) == 3

    # 3. List all test cases (authenticated view)
    all_res = await async_client.get(
        f"/api/v1/coding/questions/{question_id}/test-cases",
        cookies=cookies,
    )
    assert all_res.status_code == 200
    all_data = all_res.json()
    assert all_data["total_count"] == 4
    assert all_data["sample_count"] == 2
    assert all_data["hidden_count"] == 2
    assert len(all_data["test_cases"]) == 4

    # 4. List sample test cases (public view)
    samples_res = await async_client.get(
        f"/api/v1/coding/questions/{question_id}/test-cases/samples"
    )
    assert samples_res.status_code == 200
    samples_data = samples_res.json()
    assert len(samples_data) == 2
    assert all(c["is_sample"] is True for c in samples_data)

    # 5. Get individual test case
    get_res = await async_client.get(
        f"/api/v1/coding/test-cases/{first_tc_id}",
        cookies=cookies,
    )
    assert get_res.status_code == 200
    assert get_res.json()["id"] == first_tc_id

    # 6. Update test case
    update_payload = {
        "expected_output": "[0, 2] updated",
        "explanation": "Updated explanation",
    }
    update_res = await async_client.put(
        f"/api/v1/coding/test-cases/{first_tc_id}",
        json=update_payload,
        cookies=cookies,
    )
    assert update_res.status_code == 200
    assert update_res.json()["expected_output"] == "[0, 2] updated"
    assert update_res.json()["explanation"] == "Updated explanation"

    # 7. Reorder test cases
    reorder_payload = {
        "items": [
            {"id": first_tc_id, "order_index": 10},
            {"id": batch_data[0]["id"], "order_index": 1},
        ]
    }
    reorder_res = await async_client.put(
        f"/api/v1/coding/questions/{question_id}/test-cases/reorder",
        json=reorder_payload,
        cookies=cookies,
    )
    assert reorder_res.status_code == 200
    reordered_cases = reorder_res.json()
    case_order_map = {c["id"]: c["order_index"] for c in reordered_cases}
    assert case_order_map[first_tc_id] == 10
    assert case_order_map[batch_data[0]["id"]] == 1

    # 8. Delete test case
    del_res = await async_client.delete(
        f"/api/v1/coding/test-cases/{first_tc_id}",
        cookies=cookies,
    )
    assert del_res.status_code == 200
    assert "deleted successfully" in del_res.json()["message"]

    # Verify deleted test case returns 404
    check_del = await async_client.get(
        f"/api/v1/coding/test-cases/{first_tc_id}",
        cookies=cookies,
    )
    assert check_del.status_code == 404


async def test_test_case_error_handling(async_client: AsyncClient):
    fake_uuid = uuid.uuid4()
    # 1. Unauthorized access check (before logging in / with empty cookies)
    async_client.cookies.clear()
    unauth_res = await async_client.post(
        f"/api/v1/coding/questions/{fake_uuid}/test-cases",
        json={"input_data": "1", "expected_output": "2"},
    )
    assert unauth_res.status_code == 401

    # 2. Authenticate
    cookies = await get_auth_cookies(async_client, "tc_errors@example.com")

    # 3. Add test case to nonexistent question
    bad_q_res = await async_client.post(
        f"/api/v1/coding/questions/{fake_uuid}/test-cases",
        json={"input_data": "1", "expected_output": "2"},
        cookies=cookies,
    )
    assert bad_q_res.status_code == 404
    assert "question not found" in bad_q_res.json()["detail"].lower()

    # 4. Get nonexistent test case
    bad_tc_res = await async_client.get(
        f"/api/v1/coding/test-cases/{fake_uuid}",
        cookies=cookies,
    )
    assert bad_tc_res.status_code == 404
