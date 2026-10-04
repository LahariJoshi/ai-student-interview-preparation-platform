import uuid
import pytest
from httpx import AsyncClient

from app.modules.interview.services.llm_client import MockLLMClient, set_llm_client


# ====================================================
# Test Helpers
# ====================================================

async def register_and_get_cookies(client: AsyncClient, email: str, name: str = "Test User"):
    reg_payload = {
        "email": email,
        "password": "Password123!",
        "full_name": name,
    }
    res = await client.post("/api/v1/auth/register", json=reg_payload)
    assert res.status_code == 201
    return res.cookies


# ====================================================
# Integration Tests: GET /interview/history
# ====================================================

@pytest.mark.asyncio
async def test_get_history_unauthorized(async_client: AsyncClient):
    res = await async_client.get("/api/v1/interview/history")
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_get_history_empty(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "hist_empty@example.com")
    res = await async_client.get("/api/v1/interview/history", cookies=cookies)
    assert res.status_code == 200
    data = res.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["skip"] == 0
    assert data["limit"] == 10
    assert data["page"] == 1
    assert data["total_pages"] == 1


@pytest.mark.asyncio
async def test_get_history_user_isolation(async_client: AsyncClient):
    cookies_user_a = await register_and_get_cookies(async_client, "hist_user_a@example.com", "User A")
    cookies_user_b = await register_and_get_cookies(async_client, "hist_user_b@example.com", "User B")

    # User A creates 2 sessions
    res_a1 = await async_client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "Backend Engineer", "interview_type": "Technical", "question_count": 3},
        cookies=cookies_user_a,
    )
    assert res_a1.status_code == 201
    session_a1 = res_a1.json()

    res_a2 = await async_client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "DevOps Engineer", "interview_type": "Behavioral", "question_count": 4},
        cookies=cookies_user_a,
    )
    assert res_a2.status_code == 201
    session_a2 = res_a2.json()

    # User B creates 1 session
    res_b = await async_client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "Frontend Engineer", "interview_type": "Technical", "question_count": 5},
        cookies=cookies_user_b,
    )
    assert res_b.status_code == 201
    session_b = res_b.json()

    # User A history check
    hist_a_res = await async_client.get("/api/v1/interview/history", cookies=cookies_user_a)
    assert hist_a_res.status_code == 200
    hist_a_data = hist_a_res.json()
    assert hist_a_data["total"] == 2
    assert len(hist_a_data["items"]) == 2
    a_ids = [item["id"] for item in hist_a_data["items"]]
    assert session_a1["id"] in a_ids
    assert session_a2["id"] in a_ids
    assert session_b["id"] not in a_ids

    # User B history check
    hist_b_res = await async_client.get("/api/v1/interview/history", cookies=cookies_user_b)
    assert hist_b_res.status_code == 200
    hist_b_data = hist_b_res.json()
    assert hist_b_data["total"] == 1
    assert len(hist_b_data["items"]) == 1
    assert hist_b_data["items"][0]["id"] == session_b["id"]
    assert hist_b_data["items"][0]["target_role"] == "Frontend Engineer"


@pytest.mark.asyncio
async def test_get_history_fields_and_formatting(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "hist_fields@example.com")

    # Create session
    create_res = await async_client.post(
        "/api/v1/interview/sessions",
        json={
            "target_role": "AI Engineer",
            "interview_type": "Mixed",
            "experience_level": "Intermediate",
            "difficulty": "Hard",
            "question_count": 3,
        },
        cookies=cookies,
    )
    assert create_res.status_code == 201
    sess = create_res.json()

    res = await async_client.get("/api/v1/interview/history", cookies=cookies)
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 1
    item = data["items"][0]

    # Verify all expected fields
    assert item["id"] == sess["id"]
    assert "date" in item
    assert "created_at" in item
    assert item["target_role"] == "AI Engineer"
    assert item["interview_type"] == "Mixed"
    assert item["experience_level"] == "Intermediate"
    assert item["difficulty"] == "Hard"
    assert item["status"] == "pending"
    assert item["number_of_questions"] == 3
    assert item["question_count"] == 3
    assert "duration" in item
    assert "formatted_duration" in item
    assert isinstance(item["duration_seconds"], (int, float))


@pytest.mark.asyncio
async def test_get_history_pagination_skip_limit(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "hist_page@example.com")

    # Create 5 sessions
    created_ids = []
    for i in range(5):
        res = await async_client.post(
            "/api/v1/interview/sessions",
            json={"target_role": f"Role {i}", "question_count": 2},
            cookies=cookies,
        )
        assert res.status_code == 201
        created_ids.append(res.json()["id"])

    # First page: skip=0, limit=2
    res_p1 = await async_client.get("/api/v1/interview/history?skip=0&limit=2", cookies=cookies)
    assert res_p1.status_code == 200
    data_p1 = res_p1.json()
    assert data_p1["total"] == 5
    assert len(data_p1["items"]) == 2
    assert data_p1["skip"] == 0
    assert data_p1["limit"] == 2
    assert data_p1["page"] == 1
    assert data_p1["total_pages"] == 3

    # Second page: skip=2, limit=2
    res_p2 = await async_client.get("/api/v1/interview/history?skip=2&limit=2", cookies=cookies)
    assert res_p2.status_code == 200
    data_p2 = res_p2.json()
    assert data_p2["total"] == 5
    assert len(data_p2["items"]) == 2
    assert data_p2["skip"] == 2
    assert data_p2["page"] == 2

    # Third page: skip=4, limit=2
    res_p3 = await async_client.get("/api/v1/interview/history?skip=4&limit=2", cookies=cookies)
    assert res_p3.status_code == 200
    data_p3 = res_p3.json()
    assert data_p3["total"] == 5
    assert len(data_p3["items"]) == 1
    assert data_p3["page"] == 3

    # Beyond page: skip=6, limit=2
    res_p4 = await async_client.get("/api/v1/interview/history?skip=6&limit=2", cookies=cookies)
    assert res_p4.status_code == 200
    data_p4 = res_p4.json()
    assert data_p4["items"] == []


@pytest.mark.asyncio
async def test_get_history_page_page_size_params(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "hist_pagesize@example.com")

    # Create 3 sessions
    for i in range(3):
        res = await async_client.post(
            "/api/v1/interview/sessions",
            json={"target_role": f"Engineer {i}", "question_count": 2},
            cookies=cookies,
        )
        assert res.status_code == 201

    # Query with page=2&page_size=1
    res = await async_client.get("/api/v1/interview/history?page=2&page_size=1", cookies=cookies)
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 3
    assert len(data["items"]) == 1
    assert data["skip"] == 1
    assert data["limit"] == 1
    assert data["page"] == 2
    assert data["total_pages"] == 3


@pytest.mark.asyncio
async def test_get_history_chronological_descending(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "hist_order@example.com")

    # Session 1: Junior
    res1 = await async_client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "Junior Analyst", "question_count": 2},
        cookies=cookies,
    )
    s1_id = res1.json()["id"]

    # Session 2: Senior
    res2 = await async_client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "Senior Architect", "question_count": 2},
        cookies=cookies,
    )
    s2_id = res2.json()["id"]

    # Get history
    res = await async_client.get("/api/v1/interview/history", cookies=cookies)
    assert res.status_code == 200
    items = res.json()["items"]
    assert len(items) == 2
    # Most recent first
    assert items[0]["id"] == s2_id
    assert items[1]["id"] == s1_id


@pytest.mark.asyncio
async def test_get_history_completed_session_duration_and_scores(async_client: AsyncClient):
    set_llm_client(MockLLMClient())
    cookies = await register_and_get_cookies(async_client, "hist_completed@example.com")

    # Create and start session
    create_res = await async_client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "Platform Engineer", "difficulty": "Medium", "question_count": 2},
        cookies=cookies,
    )
    session = create_res.json()
    session_id = session["id"]

    # Generate questions
    q_res = await async_client.post(
        f"/api/v1/interview/sessions/{session_id}/generate-questions",
        cookies=cookies,
    )
    assert q_res.status_code == 201
    questions = q_res.json()

    # Start session
    start_res = await async_client.post(
        f"/api/v1/interview/sessions/{session_id}/start",
        cookies=cookies,
    )
    assert start_res.status_code == 200

    # Submit answer
    sub_res = await async_client.post(
        f"/api/v1/interview/sessions/{session_id}/responses",
        json={"question_id": questions[0]["id"], "answer_text": "We build scalable microservices with gRPC."},
        cookies=cookies,
    )
    assert sub_res.status_code == 201

    # Evaluate answer
    eval_res = await async_client.post(
        f"/api/v1/interview/sessions/{session_id}/evaluate-answer",
        json={"question_id": questions[0]["id"]},
        cookies=cookies,
    )
    assert eval_res.status_code == 200

    # Complete session
    comp_res = await async_client.post(
        f"/api/v1/interview/sessions/{session_id}/complete",
        cookies=cookies,
    )
    assert comp_res.status_code == 200

    # Fetch result to trigger aggregation
    result_res = await async_client.get(
        f"/api/v1/interview/sessions/{session_id}/result",
        cookies=cookies,
    )
    assert result_res.status_code == 200
    res_data = result_res.json()

    # Now verify history reflects this completed interview
    hist_res = await async_client.get("/api/v1/interview/history", cookies=cookies)
    assert hist_res.status_code == 200
    hist_data = hist_res.json()
    assert hist_data["total"] == 1
    item = hist_data["items"][0]
    assert item["id"] == session_id
    assert item["status"] == "completed"
    assert item["overall_score"] is not None
    assert item["technical_score"] is not None
    assert item["overall_score"] == res_data["interview_score"]
    assert item["completed_at"] is not None
    assert "formatted_duration" in item
