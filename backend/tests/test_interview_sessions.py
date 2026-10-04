import pytest
import uuid
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def register_and_get_cookies(client: AsyncClient, email: str, name: str = "Test User"):
    reg_payload = {
        "email": email,
        "password": "Password123!",
        "full_name": name,
    }
    res = await client.post("/api/v1/auth/register", json=reg_payload)
    assert res.status_code == 201
    return res.cookies


async def test_create_session_unauthorized(async_client: AsyncClient):
    payload = {
        "target_role": "Backend Developer",
        "interview_type": "Technical",
        "experience_level": "Fresher",
        "difficulty": "Easy",
        "question_count": 5,
        "answer_mode": "Voice + Text",
    }
    res = await async_client.post("/api/v1/interview/sessions", json=payload)
    assert res.status_code == 401
    assert "detail" in res.json()


async def test_create_session_success(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "session_user1@example.com", "Alice Smith")

    payload = {
        "target_role": "Fullstack Developer",
        "interview_type": "Technical",
        "experience_level": "Beginner",
        "difficulty": "Medium",
        "question_count": 5,
        "answer_mode": "Voice + Text",
        "target_company": "Microsoft",
    }
    res = await async_client.post("/api/v1/interview/sessions", json=payload, cookies=cookies)
    assert res.status_code == 201
    data = res.json()
    assert data["target_role"] == "Fullstack Developer"
    assert data["interview_type"] == "Technical"
    assert data["experience_level"] == "Beginner"
    assert data["difficulty"] == "Medium"
    assert data["question_count"] == 5
    assert data["answer_mode"] == "Voice + Text"
    assert data["target_company"] == "Microsoft"
    assert data["status"] == "pending"
    assert data["current_question_index"] == 0
    assert "id" in data
    assert "user_id" in data


async def test_create_session_validation_error(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "session_user2@example.com")

    # Invalid interview_type
    bad_payload = {
        "target_role": "Developer",
        "interview_type": "invalid_type",
    }
    res = await async_client.post("/api/v1/interview/sessions", json=bad_payload, cookies=cookies)
    assert res.status_code == 422


async def test_list_sessions_and_user_isolation(async_client: AsyncClient):
    cookies_user1 = await register_and_get_cookies(async_client, "iso1@example.com", "User 1")
    cookies_user2 = await register_and_get_cookies(async_client, "iso2@example.com", "User 2")

    # User 1 creates 2 sessions
    await async_client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "Role A", "difficulty": "Easy"},
        cookies=cookies_user1,
    )
    await async_client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "Role B", "difficulty": "Hard"},
        cookies=cookies_user1,
    )

    # User 2 creates 1 session
    await async_client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "Role C", "difficulty": "Medium"},
        cookies=cookies_user2,
    )

    # Check User 1 sessions
    res1 = await async_client.get("/api/v1/interview/sessions", cookies=cookies_user1)
    assert res1.status_code == 200
    sessions1 = res1.json()
    assert len(sessions1) == 2
    roles1 = [s["target_role"] for s in sessions1]
    assert "Role A" in roles1 and "Role B" in roles1
    assert "Role C" not in roles1

    # Check User 2 sessions
    res2 = await async_client.get("/api/v1/interview/sessions", cookies=cookies_user2)
    assert res2.status_code == 200
    sessions2 = res2.json()
    assert len(sessions2) == 1
    assert sessions2[0]["target_role"] == "Role C"


async def test_get_session_by_id_and_ownership(async_client: AsyncClient):
    cookies_owner = await register_and_get_cookies(async_client, "owner@example.com")
    cookies_other = await register_and_get_cookies(async_client, "other@example.com")

    # Owner creates session
    create_res = await async_client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "DevOps Engineer", "difficulty": "Medium"},
        cookies=cookies_owner,
    )
    session_id = create_res.json()["id"]

    # Owner can get session
    get_res = await async_client.get(f"/api/v1/interview/sessions/{session_id}", cookies=cookies_owner)
    assert get_res.status_code == 200
    assert get_res.json()["id"] == session_id

    # Other user gets 403 Forbidden
    other_res = await async_client.get(f"/api/v1/interview/sessions/{session_id}", cookies=cookies_other)
    assert other_res.status_code == 403

    # Non-existent UUID gets 404 Not Found
    random_id = uuid.uuid4()
    not_found_res = await async_client.get(f"/api/v1/interview/sessions/{random_id}", cookies=cookies_owner)
    assert not_found_res.status_code == 404


async def test_start_and_complete_session_flow(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "flow_user@example.com")

    # 1. Create session (pending)
    create_res = await async_client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "Frontend Developer", "difficulty": "Hard"},
        cookies=cookies,
    )
    session_id = create_res.json()["id"]
    assert create_res.json()["status"] == "pending"

    # 2. Start session (pending -> in_progress)
    start_res = await async_client.post(f"/api/v1/interview/sessions/{session_id}/start", cookies=cookies)
    assert start_res.status_code == 200
    assert start_res.json()["status"] == "in_progress"

    # 3. Starting again is idempotent
    start_again_res = await async_client.post(f"/api/v1/interview/sessions/{session_id}/start", cookies=cookies)
    assert start_again_res.status_code == 200
    assert start_again_res.json()["status"] == "in_progress"

    # 4. Complete session (in_progress -> completed)
    complete_res = await async_client.post(f"/api/v1/interview/sessions/{session_id}/complete", cookies=cookies)
    assert complete_res.status_code == 200
    data = complete_res.json()
    assert data["status"] == "completed"
    assert data["completed_at"] is not None

    # 5. Starting or completing an already completed session returns 400 Bad Request
    restart_res = await async_client.post(f"/api/v1/interview/sessions/{session_id}/start", cookies=cookies)
    assert restart_res.status_code == 400

    recomplete_res = await async_client.post(f"/api/v1/interview/sessions/{session_id}/complete", cookies=cookies)
    assert recomplete_res.status_code == 400


async def test_submit_answer_and_detail_flow(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "answer_test@example.com")

    # 1. Create session and generate questions
    create_res = await async_client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "Python Engineer", "question_count": 2},
        cookies=cookies,
    )
    session_id = create_res.json()["id"]

    gen_res = await async_client.post(
        f"/api/v1/interview/sessions/{session_id}/generate-questions",
        cookies=cookies,
    )
    assert gen_res.status_code == 201
    questions = gen_res.json()
    first_question = questions[0]

    # 2. Submit answer for first question
    answer_res = await async_client.post(
        f"/api/v1/interview/sessions/{session_id}/answer",
        json={
            "question_id": first_question["id"],
            "answer_text": "I utilize async/await with asyncio event loop and connection pooling.",
        },
        cookies=cookies,
    )
    assert answer_res.status_code == 200
    answer_data = answer_res.json()
    assert answer_data["question_id"] == first_question["id"]
    assert "async/await" in answer_data["transcribed_text"]

    # 3. GET /sessions/{session_id} should return detail including questions and responses
    get_res = await async_client.get(
        f"/api/v1/interview/sessions/{session_id}",
        cookies=cookies,
    )
    assert get_res.status_code == 200
    session_detail = get_res.json()
    assert len(session_detail["questions"]) == 2
    assert len(session_detail["responses"]) == 1
    assert session_detail["responses"][0]["question_id"] == first_question["id"]

