import uuid
import pytest
from httpx import AsyncClient

from app.modules.interview.services.llm_client import MockLLMClient, set_llm_client

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


async def setup_session_with_questions(client: AsyncClient, cookies):
    set_llm_client(MockLLMClient())
    # 1. Create session
    create_res = await client.post(
        "/api/v1/interview/sessions",
        json={
            "target_role": "Backend Engineer",
            "interview_type": "Technical",
            "experience_level": "Intermediate",
            "difficulty": "Medium",
            "question_count": 3,
            "answer_mode": "Voice + Text",
        },
        cookies=cookies,
    )
    assert create_res.status_code == 201
    session = create_res.json()

    # 2. Generate questions
    q_res = await client.post(
        f"/api/v1/interview/sessions/{session['id']}/generate-questions",
        cookies=cookies,
    )
    assert q_res.status_code == 201
    questions = q_res.json()
    assert len(questions) > 0

    return session, questions


async def test_submit_response_unauthorized(async_client: AsyncClient):
    session_id = uuid.uuid4()
    payload = {
        "question_id": str(uuid.uuid4()),
        "answer_text": "My answer here",
    }
    res = await async_client.post(
        f"/api/v1/interview/sessions/{session_id}/responses",
        json=payload,
    )
    assert res.status_code == 401


async def test_submit_response_session_not_found(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "resp_notfound@example.com")
    fake_session_id = uuid.uuid4()
    payload = {
        "question_id": str(uuid.uuid4()),
        "answer_text": "My answer here",
    }
    res = await async_client.post(
        f"/api/v1/interview/sessions/{fake_session_id}/responses",
        json=payload,
        cookies=cookies,
    )
    assert res.status_code == 404


async def test_submit_response_forbidden_other_user(async_client: AsyncClient):
    cookies1 = await register_and_get_cookies(async_client, "resp_owner@example.com", "Owner")
    cookies2 = await register_and_get_cookies(async_client, "resp_intruder@example.com", "Intruder")

    session, questions = await setup_session_with_questions(async_client, cookies1)

    payload = {
        "question_id": questions[0]["id"],
        "answer_text": "An intruder is answering.",
    }
    res = await async_client.post(
        f"/api/v1/interview/sessions/{session['id']}/responses",
        json=payload,
        cookies=cookies2,
    )
    assert res.status_code == 403


async def test_submit_response_question_not_in_session(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "resp_badq@example.com")
    session, _ = await setup_session_with_questions(async_client, cookies)

    payload = {
        "question_id": str(uuid.uuid4()),
        "answer_text": "Valid answer for nonexistent question",
    }
    res = await async_client.post(
        f"/api/v1/interview/sessions/{session['id']}/responses",
        json=payload,
        cookies=cookies,
    )
    assert res.status_code == 404
    assert "Question not found in this interview session" in res.json()["detail"]


async def test_submit_response_empty_or_whitespace_validation(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "resp_empty@example.com")
    session, questions = await setup_session_with_questions(async_client, cookies)

    # Empty string
    res_empty = await async_client.post(
        f"/api/v1/interview/sessions/{session['id']}/responses",
        json={"question_id": questions[0]["id"], "answer_text": ""},
        cookies=cookies,
    )
    assert res_empty.status_code in [400, 422]

    # Whitespace only
    res_ws = await async_client.post(
        f"/api/v1/interview/sessions/{session['id']}/responses",
        json={"question_id": questions[0]["id"], "answer_text": "     \n\t   "},
        cookies=cookies,
    )
    assert res_ws.status_code in [400, 422]


async def test_submit_response_success_and_duplicate_prevention(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "resp_success@example.com")
    session, questions = await setup_session_with_questions(async_client, cookies)

    q1 = questions[0]
    first_answer = "Dependency injection decouples object creation from business logic."

    # 1. First submission (status 201 Created)
    res1 = await async_client.post(
        f"/api/v1/interview/sessions/{session['id']}/responses",
        json={"question_id": q1["id"], "answer_text": first_answer},
        cookies=cookies,
    )
    assert res1.status_code == 201
    resp_data = res1.json()
    assert "id" in resp_data
    assert resp_data["session_id"] == session["id"]
    assert resp_data["question_id"] == q1["id"]
    assert resp_data["transcribed_text"] == first_answer
    first_id = resp_data["id"]

    # 2. Check session updated to in_progress and index advanced
    session_res = await async_client.get(
        f"/api/v1/interview/sessions/{session['id']}",
        cookies=cookies,
    )
    assert session_res.status_code == 200
    session_detail = session_res.json()
    assert session_detail["status"] == "in_progress"
    assert session_detail["current_question_index"] >= 1
    assert len(session_detail["responses"]) == 1

    # 3. Duplicate submission without allow_retry -> 400 Bad Request
    res_dup = await async_client.post(
        f"/api/v1/interview/sessions/{session['id']}/responses",
        json={"question_id": q1["id"], "answer_text": "Updated answer attempt."},
        cookies=cookies,
    )
    assert res_dup.status_code == 400
    assert "already been submitted" in res_dup.json()["detail"]

    # 4. Submission with allow_retry=True -> 200 OK, same ID updated
    updated_answer = "Refined answer: Dependency injection enables inversion of control."
    res_retry = await async_client.post(
        f"/api/v1/interview/sessions/{session['id']}/responses",
        json={
            "question_id": q1["id"],
            "answer_text": updated_answer,
            "allow_retry": True,
        },
        cookies=cookies,
    )
    assert res_retry.status_code == 200
    retry_data = res_retry.json()
    assert retry_data["id"] == first_id
    assert retry_data["transcribed_text"] == updated_answer


async def test_submit_response_completed_session_blocked(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "resp_complete@example.com")
    session, questions = await setup_session_with_questions(async_client, cookies)

    # Complete the session
    comp_res = await async_client.post(
        f"/api/v1/interview/sessions/{session['id']}/complete",
        cookies=cookies,
    )
    assert comp_res.status_code == 200

    # Try to answer a question
    res = await async_client.post(
        f"/api/v1/interview/sessions/{session['id']}/responses",
        json={"question_id": questions[0]["id"], "answer_text": "Too late to answer."},
        cookies=cookies,
    )
    assert res.status_code == 400
    assert "completed session" in res.json()["detail"]


async def test_legacy_answer_endpoint_compatibility(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "resp_legacy@example.com")
    session, questions = await setup_session_with_questions(async_client, cookies)

    res = await async_client.post(
        f"/api/v1/interview/sessions/{session['id']}/answer",
        json={"question_id": questions[0]["id"], "answer_text": "Answering via legacy endpoint"},
        cookies=cookies,
    )
    assert res.status_code == 200
    data = res.json()
    assert data["transcribed_text"] == "Answering via legacy endpoint"
    assert "id" in data
