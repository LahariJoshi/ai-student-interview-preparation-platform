import io
import json
import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.interview.models import (
    InterviewSession,
    InterviewQuestion,
    InterviewResponse,
)
from app.modules.interview.services.llm_client import MockLLMClient, set_llm_client
from app.modules.voice.models import VoiceAnalysis
from app.modules.voice.schemas import VoicePipelineResultOut
from app.modules.voice.services.speech_to_text import (
    MockSTTClient,
    set_stt_client,
)
from app.modules.voice.services.voice_pipeline import (
    VoicePipelineService,
    voice_pipeline_service,
)

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
        json={"target_role": "Backend Engineer", "difficulty": "Medium"},
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
# API Integration Tests for Voice Pipeline
# ====================================================

@pytest.mark.asyncio
async def test_pipeline_unauthorized(async_client: AsyncClient):
    fake_session_id = uuid.uuid4()
    audio_file = io.BytesIO(WEBM_HEADER + b"\x00" * 300)

    res = await async_client.post(
        f"/api/v1/voice/sessions/{fake_session_id}/process-audio",
        files={"file": ("recording.webm", audio_file, "audio/webm")},
        data={"question_id": str(uuid.uuid4())},
    )
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_pipeline_session_not_found(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "pipe_nf@example.com")
    fake_session_id = uuid.uuid4()
    audio_file = io.BytesIO(WEBM_HEADER + b"\x00" * 300)

    res = await async_client.post(
        f"/api/v1/voice/sessions/{fake_session_id}/process-audio",
        files={"file": ("recording.webm", audio_file, "audio/webm")},
        data={"question_id": str(uuid.uuid4())},
        cookies=cookies,
    )
    assert res.status_code == 404
    assert "session not found" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_pipeline_forbidden_other_user(async_client: AsyncClient):
    cookies_owner = await register_and_get_cookies(async_client, "pipe_owner@example.com")
    cookies_intruder = await register_and_get_cookies(async_client, "pipe_intruder@example.com")

    session, questions = await setup_interview_session(async_client, cookies_owner)
    audio_file = io.BytesIO(WEBM_HEADER + b"\x00" * 300)

    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/process-audio",
        files={"file": ("recording.webm", audio_file, "audio/webm")},
        data={"question_id": questions[0]["id"]},
        cookies=cookies_intruder,
    )
    assert res.status_code == 403
    assert "permission" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_pipeline_question_not_found(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "pipe_q_nf@example.com")
    session, _ = await setup_interview_session(async_client, cookies)
    fake_q_id = uuid.uuid4()
    audio_file = io.BytesIO(WEBM_HEADER + b"\x00" * 300)

    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/process-audio",
        files={"file": ("recording.webm", audio_file, "audio/webm")},
        data={"question_id": str(fake_q_id)},
        cookies=cookies,
    )
    assert res.status_code == 404
    assert "question not found" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_pipeline_completed_session(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "pipe_completed@example.com")
    session, questions = await setup_interview_session(async_client, cookies)

    # Complete the session
    comp_res = await async_client.post(
        f"/api/v1/interview/sessions/{session['id']}/complete",
        cookies=cookies,
    )
    assert comp_res.status_code == 200

    audio_file = io.BytesIO(WEBM_HEADER + b"\x00" * 300)
    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/process-audio",
        files={"file": ("recording.webm", audio_file, "audio/webm")},
        data={"question_id": questions[0]["id"]},
        cookies=cookies,
    )
    assert res.status_code == 400
    assert "already completed" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_pipeline_invalid_audio_format(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "pipe_inv_format@example.com")
    session, questions = await setup_interview_session(async_client, cookies)

    bad_file = io.BytesIO(b"Just plain text data that exceeds minimum bytes requirement easily.")
    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/process-audio",
        files={"file": ("notes.txt", bad_file, "text/plain")},
        data={"question_id": questions[0]["id"]},
        cookies=cookies,
    )
    assert res.status_code == 400
    assert "unsupported audio format" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_pipeline_corrupted_audio_signature(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "pipe_corrupt@example.com")
    session, questions = await setup_interview_session(async_client, cookies)

    disguised = io.BytesIO(b"%PDF-1.5 disguised file header padding padding padding padding padding")
    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/process-audio",
        files={"file": ("recording.webm", disguised, "audio/webm")},
        data={"question_id": questions[0]["id"]},
        cookies=cookies,
    )
    assert res.status_code == 400
    assert "invalid" in res.json()["detail"].lower() or "signature" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_pipeline_stt_timeout(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "pipe_timeout@example.com")
    session, questions = await setup_interview_session(async_client, cookies)

    set_stt_client(MockSTTClient(simulate_error="timeout"))
    audio_file = io.BytesIO(WEBM_HEADER + b"\x00" * 400)

    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/process-audio",
        files={"file": ("recording.webm", audio_file, "audio/webm")},
        data={"question_id": questions[0]["id"]},
        cookies=cookies,
    )
    assert res.status_code == 504
    assert "timed out" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_pipeline_stt_empty_transcript(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "pipe_empty_stt@example.com")
    session, questions = await setup_interview_session(async_client, cookies)

    set_stt_client(MockSTTClient(simulate_error="empty"))
    audio_file = io.BytesIO(WEBM_HEADER + b"\x00" * 400)

    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/process-audio",
        files={"file": ("recording.webm", audio_file, "audio/webm")},
        data={"question_id": questions[0]["id"]},
        cookies=cookies,
    )
    assert res.status_code == 502
    assert "empty" in res.json()["detail"].lower() or "failure" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_pipeline_success_full_workflow(async_client: AsyncClient, db_session: AsyncSession):
    cookies = await register_and_get_cookies(async_client, "pipe_success@example.com")
    session, questions = await setup_interview_session(async_client, cookies)

    # Setup canned mock AI speech & evaluation
    canned_speech = (
        "Um, basically I designed our database architecture with PostgreSQL and read-replicas. "
        "We, like, indexed the primary query paths, which reduced our p95 query latency down to 15 milliseconds."
    )
    set_stt_client(MockSTTClient(canned_transcript=canned_speech))
    set_llm_client(
        MockLLMClient(
            canned_response=json.dumps(
                {
                    "score": 88.5,
                    "technical_score": 90.0,
                    "relevance_score": 92.0,
                    "clarity_score": 85.0,
                    "strengths": ["Clear explanation of read-replicas", "Quantified latency reduction to 15ms"],
                    "weaknesses": ["Could elaborate on write contention"],
                    "feedback": ["Solid architecture and optimization explanation."],
                    "improvements": ["Mention connection pooling or caching layers."],
                }
            )
        )
    )

    audio_file = io.BytesIO(WEBM_HEADER + b"\x00" * 500)
    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/process-audio",
        files={"file": ("candidate_recording.webm", audio_file, "audio/webm")},
        data={
            "question_id": questions[0]["id"],
            "duration_seconds": "35.0",
        },
        cookies=cookies,
    )
    assert res.status_code == 200
    data = res.json()

    # 1. Verify response structure
    assert data["session_id"] == session["id"]
    assert data["question_id"] == questions[0]["id"]
    assert data["status"] == "completed"
    assert "Um, basically" in data["transcript"]
    assert data["answer_score"] == 88.5
    assert data["communication_score"] > 0.0

    # 2. Verify sub-objects
    assert "answer_analysis" in data
    assert data["answer_analysis"]["technical_score"] == 90.0
    assert "voice_metrics" in data
    assert data["voice_metrics"]["speaking_rate"]["word_count"] > 10
    assert data["voice_metrics"]["filler_analysis"]["filler_word_count"] >= 2
    assert "communication_feedback" in data
    assert len(data["communication_feedback"]["feedback"]) > 0

    # 3. Verify Database Persistence in InterviewResponse
    r_res = await db_session.execute(
        select(InterviewResponse).where(InterviewResponse.id == uuid.UUID(data["response_id"]))
    )
    saved_response = r_res.scalar_one_or_none()
    assert saved_response is not None
    assert saved_response.score == 88.5
    assert saved_response.transcribed_text == canned_speech
    assert saved_response.audio_file_path is not None
    assert saved_response.audio_duration_seconds == 35.0

    # 4. Verify Database Persistence in VoiceAnalysis
    va_res = await db_session.execute(
        select(VoiceAnalysis).where(VoiceAnalysis.response_id == uuid.UUID(data["response_id"]))
    )
    saved_va = va_res.scalar_one_or_none()
    assert saved_va is not None
    assert saved_va.clarity_score == data["communication_score"]
    assert saved_va.filler_word_count >= 2
    assert "communication coaching note" in saved_va.communication_feedback.lower()

    # 5. Verify Session Scores Updated
    s_res = await db_session.execute(
        select(InterviewSession).where(InterviewSession.id == uuid.UUID(session["id"]))
    )
    saved_session = s_res.scalar_one_or_none()
    assert saved_session is not None
    assert saved_session.overall_score == 88.5
    assert saved_session.technical_score == 88.5
    assert saved_session.communication_score == data["communication_score"]


@pytest.mark.asyncio
async def test_pipeline_retry_and_idempotency(async_client: AsyncClient, db_session: AsyncSession):
    cookies = await register_and_get_cookies(async_client, "pipe_retry@example.com")
    session, questions = await setup_interview_session(async_client, cookies)

    set_stt_client(MockSTTClient(canned_transcript="Initial candidate answer."))
    set_llm_client(MockLLMClient())

    audio_file1 = io.BytesIO(WEBM_HEADER + b"\x00" * 400)
    res1 = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/process-audio",
        files={"file": ("attempt1.webm", audio_file1, "audio/webm")},
        data={"question_id": questions[0]["id"], "duration_seconds": "20.0"},
        cookies=cookies,
    )
    assert res1.status_code == 200
    data1 = res1.json()

    # Second attempt (Candidate re-records and retries)
    set_stt_client(MockSTTClient(canned_transcript="Second refined attempt with much better architecture depth."))
    audio_file2 = io.BytesIO(WEBM_HEADER + b"\x00" * 500)
    res2 = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/process-audio",
        files={"file": ("attempt2.webm", audio_file2, "audio/webm")},
        data={
            "question_id": questions[0]["id"],
            "response_id": data1["response_id"],
            "duration_seconds": "28.0",
        },
        cookies=cookies,
    )
    assert res2.status_code == 200
    data2 = res2.json()

    assert data2["response_id"] == data1["response_id"]
    assert "Second refined attempt" in data2["transcript"]

    # Verify only ONE VoiceAnalysis record exists in DB for this response
    va_res = await db_session.execute(
        select(VoiceAnalysis).where(VoiceAnalysis.response_id == uuid.UUID(data1["response_id"]))
    )
    analyses = va_res.scalars().all()
    assert len(analyses) == 1
