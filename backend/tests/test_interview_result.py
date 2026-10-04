import io
import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.interview.models import (
    InterviewSession,
    InterviewFeedback,
)
from app.modules.interview.services.llm_client import MockLLMClient, set_llm_client
from app.modules.voice.models import VoiceAnalysis
from app.modules.voice.services.speech_to_text import MockSTTClient, set_stt_client

WEBM_HEADER = b"\x1a\x45\xdf\xa3\x9f\x42\x86\x81\x01\x42\xf7\x81\x01\x42\xf2\x81\x04"


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


async def setup_interview_session(client: AsyncClient, cookies: dict):
    set_llm_client(MockLLMClient())

    create_res = await client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "Full Stack Engineer", "difficulty": "Medium", "question_count": 3},
        cookies=cookies,
    )
    assert create_res.status_code == 201
    session = create_res.json()

    q_res = await client.post(
        f"/api/v1/interview/sessions/{session['id']}/generate-questions",
        cookies=cookies,
    )
    assert q_res.status_code == 201
    questions = q_res.json()

    return session, questions


# ====================================================
# Integration Tests: GET /interview/sessions/{id}/result
# ====================================================

@pytest.mark.asyncio
async def test_get_result_unauthorized(async_client: AsyncClient):
    fake_id = uuid.uuid4()
    res = await async_client.get(f"/api/v1/interview/sessions/{fake_id}/result")
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_get_result_session_not_found(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "res_nf@example.com")
    fake_id = uuid.uuid4()
    res = await async_client.get(f"/api/v1/interview/sessions/{fake_id}/result", cookies=cookies)
    assert res.status_code == 404
    assert "not found" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_get_result_forbidden_other_user(async_client: AsyncClient):
    cookies_owner = await register_and_get_cookies(async_client, "res_owner@example.com")
    cookies_intruder = await register_and_get_cookies(async_client, "res_intruder@example.com")

    session, _ = await setup_interview_session(async_client, cookies_owner)

    res = await async_client.get(
        f"/api/v1/interview/sessions/{session['id']}/result",
        cookies=cookies_intruder,
    )
    assert res.status_code == 403
    assert "permission" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_get_result_empty_session_without_responses(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "res_empty@example.com")
    session, questions = await setup_interview_session(async_client, cookies)

    res = await async_client.get(
        f"/api/v1/interview/sessions/{session['id']}/result",
        cookies=cookies,
    )
    assert res.status_code == 200
    data = res.json()

    assert data["session_id"] == session["id"]
    assert data["target_role"] == "Full Stack Engineer"
    assert data["total_questions"] == len(questions)
    assert data["answered_questions"] == 0
    assert data["interview_score"] == 0.0
    assert data["technical_score"] == 0.0
    assert data["communication_score"] == 0.0
    assert data["voice_metrics"]["has_voice_data"] is False
    assert len(data["question_performance"]) == len(questions)
    assert data["formatted_duration"] is not None


@pytest.mark.asyncio
async def test_get_result_with_text_responses(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "res_text@example.com")
    session, questions = await setup_interview_session(async_client, cookies)

    # Submit an answer and evaluate
    resp_res = await async_client.post(
        f"/api/v1/interview/sessions/{session['id']}/responses",
        json={"question_id": questions[0]["id"], "answer_text": "I used React and TypeScript to build UI components with high reusability."},
        cookies=cookies,
    )
    assert resp_res.status_code == 201
    resp_data = resp_res.json()

    # Evaluate the response
    eval_res = await async_client.post(
        f"/api/v1/interview/sessions/{session['id']}/responses/{resp_data['id']}/evaluate",
        cookies=cookies,
    )
    assert eval_res.status_code == 200

    # Get final aggregated result
    res = await async_client.get(
        f"/api/v1/interview/sessions/{session['id']}/result",
        cookies=cookies,
    )
    assert res.status_code == 200
    data = res.json()

    assert data["answered_questions"] == 1
    assert data["technical_score"] > 0.0
    assert data["interview_score"] == data["technical_score"]  # No voice, matches tech score
    assert len(data["strengths"]) > 0
    assert len(data["recommendations"]) > 0

    # Check question performance
    qp = data["question_performance"][0]
    assert qp["question_id"] == questions[0]["id"]
    assert qp["score"] is not None
    assert "React" in qp["candidate_answer"]


@pytest.mark.asyncio
async def test_get_result_with_voice_responses_and_metrics(async_client: AsyncClient, db_session: AsyncSession):
    cookies = await register_and_get_cookies(async_client, "res_voice@example.com")
    session, questions = await setup_interview_session(async_client, cookies)

    # Setup realistic STT and LLM mocks
    set_stt_client(
        MockSTTClient(
            canned_transcript="Um, basically I architected our services using Kafka and Postgres with read-replicas, like, yesterday."
        )
    )
    set_llm_client(MockLLMClient())

    # Process first voice response
    audio_file1 = io.BytesIO(WEBM_HEADER + b"\x00" * 400)
    p_res1 = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/process-audio",
        files={"file": ("recording1.webm", audio_file1, "audio/webm")},
        data={"question_id": questions[0]["id"], "duration_seconds": "30.0"},
        cookies=cookies,
    )
    assert p_res1.status_code == 200

    # Process second voice response
    set_stt_client(
        MockSTTClient(
            canned_transcript="For caching we utilized Redis cluster to maintain sub-millisecond response times for session state."
        )
    )
    audio_file2 = io.BytesIO(WEBM_HEADER + b"\x00" * 400)
    p_res2 = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/process-audio",
        files={"file": ("recording2.webm", audio_file2, "audio/webm")},
        data={"question_id": questions[1]["id"], "duration_seconds": "35.0"},
        cookies=cookies,
    )
    assert p_res2.status_code == 200

    # Complete the interview
    comp_res = await async_client.post(
        f"/api/v1/interview/sessions/{session['id']}/complete",
        cookies=cookies,
    )
    assert comp_res.status_code == 200

    # Fetch final aggregated result
    res = await async_client.get(
        f"/api/v1/interview/sessions/{session['id']}/result",
        cookies=cookies,
    )
    assert res.status_code == 200
    data = res.json()

    # 1. Verify Score Aggregation
    assert data["status"] == "completed"
    assert data["answered_questions"] == 2
    assert 0.0 <= data["technical_score"] <= 100.0
    assert 0.0 <= data["communication_score"] <= 100.0
    assert 0.0 <= data["interview_score"] <= 100.0
    # Blended score: 65% tech + 35% comm
    expected_blended = round((data["technical_score"] * 0.65) + (data["communication_score"] * 0.35), 1)
    assert data["interview_score"] == expected_blended

    # 2. Verify Aggregated Voice Metrics
    vm = data["voice_metrics"]
    assert vm["has_voice_data"] is True
    assert vm["average_speaking_rate_wpm"] > 0.0
    assert vm["total_filler_word_count"] >= 2  # 'um', 'basically', 'like' detected in speech 1
    assert "um" in vm["filler_words_detected"]
    assert vm["average_clarity_score"] > 0.0
    assert len(vm["communication_feedback"]) > 0

    # 3. Verify Question-wise breakdown
    qp = data["question_performance"]
    assert len(qp) == len(questions)
    assert qp[0]["candidate_answer"] is not None
    assert qp[0]["speaking_rate_wpm"] is not None
    assert qp[0]["filler_word_count"] is not None
    assert qp[1]["candidate_answer"] is not None

    # 4. Verify Strengths, Weaknesses, Recommendations & Duration
    assert len(data["strengths"]) > 0
    assert len(data["weaknesses"]) > 0
    assert len(data["recommendations"]) > 0
    assert "m " in data["formatted_duration"] or "s" in data["formatted_duration"]

    # 5. Verify Database Persistence of InterviewFeedback
    fb_res = await db_session.execute(
        select(InterviewFeedback).where(InterviewFeedback.session_id == uuid.UUID(session["id"]))
    )
    saved_fb = fb_res.scalar_one_or_none()
    assert saved_fb is not None
    assert saved_fb.overall_score == data["interview_score"]
    assert saved_fb.technical_score == data["technical_score"]
    assert saved_fb.communication_score == data["communication_score"]
    assert len(saved_fb.actionable_recommendations) > 0
