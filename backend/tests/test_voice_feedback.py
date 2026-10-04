import uuid
import pytest
from httpx import AsyncClient
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.interview.models import InterviewSession
from app.modules.interview.services.llm_client import MockLLMClient, set_llm_client
from app.modules.voice.models import VoiceAnalysis
from app.modules.voice.schemas import CommunicationFeedbackResult
from app.modules.voice.services.voice_feedback import (
    VoiceFeedbackService,
    voice_feedback_service,
)
from app.modules.voice.services.voice_metrics import VoiceMetricsService


# ====================================================
# Unit Tests: VoiceFeedbackService
# ====================================================

def test_transcript_structure_evaluation():
    service = VoiceFeedbackService()

    # Short normal sentences
    normal_text = "I designed the database schema. Then I added Redis for caching. We observed lower latency."
    struct = service.evaluate_transcript_structure(normal_text)
    assert struct["sentence_count"] == 3
    assert struct["is_run_on"] is False

    # Long run-on sentence (> 35 words)
    run_on_text = (
        "I was thinking about how we could optimize the application and then decided to implement "
        "a distributed caching layer using Redis clusters while also rewriting the database queries "
        "to leverage index scans instead of sequential table scans which reduced response times significantly "
        "across all microservice endpoints."
    )
    run_on_struct = service.evaluate_transcript_structure(run_on_text)
    assert run_on_struct["sentence_count"] == 1
    assert run_on_struct["is_run_on"] is True
    assert run_on_struct["avg_sentence_words"] > 35.0

    # Empty text
    empty_struct = service.evaluate_transcript_structure("")
    assert empty_struct["sentence_count"] == 0
    assert empty_struct["is_run_on"] is False


def test_feedback_optimal_pacing_and_low_filler():
    service = VoiceFeedbackService()
    metrics = {
        "speaking_rate": {
            "word_count": 140,
            "duration_seconds": 60.0,
            "speech_rate_wpm": 140.0,
        },
        "filler_analysis": {
            "filler_word_count": 1,
            "filler_words": {"like": 1},
            "filler_rate": 0.7,
        },
        "pause_analysis": {
            "pause_count": 0,
            "total_pause_seconds": 0.0,
            "average_pause_seconds": 0.0,
            "longest_pause_seconds": 0.0,
            "data_availability": "unavailable",
            "is_estimated": True,
        },
    }
    transcript = "I architected the service with event sourcing and PostgreSQL for durable storage."

    result = service.generate_feedback(metrics, transcript)

    assert isinstance(result, CommunicationFeedbackResult)
    assert result.communication_score >= 90.0
    # Strengths should highlight cadence and verbal economy
    strength_text = " ".join(result.strengths).lower()
    assert "cadence" in strength_text or "140" in strength_text
    assert "verbal economy" in strength_text or "filler" in strength_text


def test_feedback_fast_pacing_explains_why():
    service = VoiceFeedbackService()
    metrics = {
        "speaking_rate": {
            "word_count": 185,
            "duration_seconds": 60.0,
            "speech_rate_wpm": 185.0,
        },
        "filler_analysis": {
            "filler_word_count": 0,
            "filler_words": {},
            "filler_rate": 0.0,
        },
        "pause_analysis": {
            "pause_count": 0,
            "total_pause_seconds": 0.0,
            "average_pause_seconds": 0.0,
            "longest_pause_seconds": 0.0,
            "data_availability": "unavailable",
            "is_estimated": True,
        },
    }
    transcript = "Quickly explaining everything at high speed to make sure everything gets covered in the response."

    result = service.generate_feedback(metrics, transcript)

    areas_text = " ".join(result.areas_to_improve).lower()
    feedback_text = " ".join(result.feedback).lower()

    # Must explain that pace is fast and why deliberately slowing helps
    assert "faster" in areas_text or "185" in areas_text or "slowing" in areas_text
    assert "pacing rationale" in feedback_text or "deliberate pauses" in feedback_text


def test_feedback_slow_pacing_explains_why():
    service = VoiceFeedbackService()
    metrics = {
        "speaking_rate": {
            "word_count": 50,
            "duration_seconds": 35.0,
            "speech_rate_wpm": 85.7,
        },
        "filler_analysis": {
            "filler_word_count": 0,
            "filler_words": {},
            "filler_rate": 0.0,
        },
        "pause_analysis": {
            "pause_count": 0,
            "total_pause_seconds": 0.0,
            "average_pause_seconds": 0.0,
            "longest_pause_seconds": 0.0,
            "data_availability": "unavailable",
            "is_estimated": True,
        },
    }
    transcript = "I worked on the frontend components using React and TypeScript."

    result = service.generate_feedback(metrics, transcript)

    areas_text = " ".join(result.areas_to_improve).lower()
    feedback_text = " ".join(result.feedback).lower()

    # Must constructively recommend acceleration and explain why
    assert "acceleration" in areas_text or "85.7" in areas_text or "briskly" in areas_text
    assert "timed interviews" in feedback_text or "concise sentence formulation" in feedback_text


def test_feedback_high_fillers_explains_why():
    service = VoiceFeedbackService()
    metrics = {
        "speaking_rate": {
            "word_count": 100,
            "duration_seconds": 45.0,
            "speech_rate_wpm": 133.3,
        },
        "filler_analysis": {
            "filler_word_count": 8,
            "filler_words": {"um": 4, "basically": 2, "like": 2},
            "filler_rate": 8.0,
        },
        "pause_analysis": {
            "pause_count": 0,
            "total_pause_seconds": 0.0,
            "average_pause_seconds": 0.0,
            "longest_pause_seconds": 0.0,
            "data_availability": "unavailable",
            "is_estimated": True,
        },
    }
    transcript = "Um, so basically, I was, like, working on the API, um, and basically we deployed it, like, yesterday."

    result = service.generate_feedback(metrics, transcript)

    areas_text = " ".join(result.areas_to_improve).lower()
    feedback_text = " ".join(result.feedback).lower()

    # Must identify top fillers and suggest silent pauses as organizing tools
    assert "filler word reduction" in areas_text or "8.0%" in areas_text
    assert "'um'" in areas_text or "'basically'" in areas_text
    assert "silent pauses" in feedback_text
    assert "organizing" in feedback_text or "thought" in feedback_text


def test_feedback_with_precise_pause_data():
    service = VoiceFeedbackService()
    metrics = {
        "speaking_rate": {
            "word_count": 140,
            "duration_seconds": 60.0,
            "speech_rate_wpm": 140.0,
        },
        "filler_analysis": {
            "filler_word_count": 1,
            "filler_words": {"you know": 1},
            "filler_rate": 0.7,
        },
        "pause_analysis": {
            "pause_count": 4,
            "total_pause_seconds": 4.8,
            "average_pause_seconds": 1.2,
            "longest_pause_seconds": 1.5,
            "data_availability": "precise",
            "is_estimated": False,
        },
    }
    transcript = "Here is a well segmented answer with natural pauses between sentences."

    result = service.generate_feedback(metrics, transcript)

    # Should praise natural pause distribution
    strength_text = " ".join(result.strengths).lower()
    assert "pause distribution" in strength_text or "1.2s" in strength_text


def test_communication_score_boundaries():
    service = VoiceFeedbackService()

    # Perfect scenario
    score_perfect = service.compute_communication_score(
        speaking_rate_wpm=135.0,
        filler_rate=0.5,
        pause_data_available=True,
        average_pause_seconds=1.0,
    )
    assert 90.0 <= score_perfect <= 100.0

    # Very slow with excessive fillers
    score_low = service.compute_communication_score(
        speaking_rate_wpm=45.0,
        filler_rate=12.0,
        pause_data_available=False,
        average_pause_seconds=0.0,
    )
    assert 0.0 <= score_low <= 60.0


def test_strict_ethical_boundaries_no_medical_or_psychological_claims():
    """
    CRITICAL ETHICAL AUDIT:
    Feedback must NEVER contain medical, psychiatric, or psychological claims,
    and must NEVER diagnose anxiety, personality traits, or emotional instability.
    """
    service = VoiceFeedbackService()

    # Generate feedback for a wide variety of edge-case metrics
    test_cases = [
        {"wpm": 60.0, "fillers": 15, "filler_rate": 15.0},
        {"wpm": 210.0, "fillers": 0, "filler_rate": 0.0},
        {"wpm": 130.0, "fillers": 3, "filler_rate": 2.5},
        {"wpm": 0.0, "fillers": 0, "filler_rate": 0.0},
    ]

    prohibited_terms = [
        "anxiety",
        "anxious",
        "nervous",
        "nervousness",
        "mental",
        "psychological",
        "psychiatric",
        "disorder",
        "pathology",
        "panic",
        "depressed",
        "depression",
        "neurotic",
        "adhd",
        "autism",
        "cognitive deficit",
        "personality",
    ]

    for tc in test_cases:
        metrics = {
            "speaking_rate": {"speech_rate_wpm": tc["wpm"], "word_count": 80, "duration_seconds": 30.0},
            "filler_analysis": {"filler_word_count": tc["fillers"], "filler_rate": tc["filler_rate"], "filler_words": {"um": tc["fillers"]}},
            "pause_analysis": {"pause_count": 2, "average_pause_seconds": 1.1, "data_availability": "precise"},
        }
        res = service.generate_feedback(metrics, "Sample interview answer for ethical evaluation testing.")

        full_text = " ".join(res.strengths + res.areas_to_improve + res.feedback).lower()
        for term in prohibited_terms:
            assert term not in full_text, f"Prohibited clinical/psychological term '{term}' found in feedback: {full_text}"


def test_mandatory_educational_coaching_disclaimer():
    """
    Ensures generated feedback explicitly treats vocal metrics as delivery coaching signals
    rather than a complete measure of engineering or interview competence.
    """
    service = VoiceFeedbackService()
    metrics = {
        "speaking_rate": {"speech_rate_wpm": 130.0, "word_count": 65, "duration_seconds": 30.0},
        "filler_analysis": {"filler_word_count": 0, "filler_rate": 0.0, "filler_words": {}},
        "pause_analysis": {"pause_count": 0, "average_pause_seconds": 0.0, "data_availability": "unavailable"},
    }
    res = service.generate_feedback(metrics, "Architecture response.")

    feedback_combined = " ".join(res.feedback)
    assert "educational practice tool" in feedback_combined.lower()
    assert "technical depth" in feedback_combined.lower()


# ====================================================
# API Integration & Database Persistence Tests
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


async def setup_interview_response(client: AsyncClient, cookies: dict, answer_text: str = "I built the system using microservices."):
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

    resp_res = await client.post(
        f"/api/v1/interview/sessions/{session['id']}/responses",
        json={
            "question_id": questions[0]["id"],
            "answer_text": answer_text,
        },
        cookies=cookies,
    )
    assert resp_res.status_code == 201
    response = resp_res.json()

    return session, questions, response


@pytest.mark.asyncio
async def test_feedback_endpoint_unauthorized(async_client: AsyncClient):
    fake_session_id = uuid.uuid4()
    fake_response_id = uuid.uuid4()

    res = await async_client.post(
        f"/api/v1/voice/sessions/{fake_session_id}/responses/{fake_response_id}/feedback"
    )
    assert res.status_code == 401


@pytest.mark.asyncio
async def test_feedback_session_not_found(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "vf_nf@example.com")
    fake_session_id = uuid.uuid4()
    fake_response_id = uuid.uuid4()

    res = await async_client.post(
        f"/api/v1/voice/sessions/{fake_session_id}/responses/{fake_response_id}/feedback",
        cookies=cookies,
    )
    assert res.status_code == 404
    assert "session not found" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_feedback_forbidden_other_user(async_client: AsyncClient):
    cookies_owner = await register_and_get_cookies(async_client, "vf_owner@example.com")
    cookies_intruder = await register_and_get_cookies(async_client, "vf_intruder@example.com")

    session, _, response = await setup_interview_response(async_client, cookies_owner)

    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/responses/{response['id']}/feedback",
        cookies=cookies_intruder,
    )
    assert res.status_code == 403
    assert "permission" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_feedback_response_not_found(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "vf_resp_nf@example.com")
    session, _, _ = await setup_interview_response(async_client, cookies)

    fake_response_id = uuid.uuid4()
    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/responses/{fake_response_id}/feedback",
        cookies=cookies,
    )
    assert res.status_code == 404
    assert "response not found" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_feedback_response_wrong_session(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "vf_wrong_sess@example.com")
    session1, _, resp1 = await setup_interview_response(async_client, cookies)
    session2, _, _ = await setup_interview_response(async_client, cookies)

    # Calling with session2 but resp1
    res = await async_client.post(
        f"/api/v1/voice/sessions/{session2['id']}/responses/{resp1['id']}/feedback",
        cookies=cookies,
    )
    assert res.status_code == 400
    assert "does not belong to this interview session" in res.json()["detail"].lower()


@pytest.mark.asyncio
async def test_feedback_success_and_db_persistence(async_client: AsyncClient, db_session: AsyncSession):
    cookies = await register_and_get_cookies(async_client, "vf_success@example.com")
    speech = (
        "Um, basically I designed the system architecture using event streaming with Kafka. "
        "We, like, decoupled our producers and consumers to guarantee high throughput and zero message loss."
    )
    session, _, response = await setup_interview_response(async_client, cookies, answer_text=speech)

    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/responses/{response['id']}/feedback",
        cookies=cookies,
    )
    assert res.status_code == 200
    data = res.json()

    assert "communication_score" in data
    assert "strengths" in data
    assert "areas_to_improve" in data
    assert "feedback" in data
    assert "metrics" in data

    assert 0.0 <= data["communication_score"] <= 100.0
    assert len(data["feedback"]) >= 1

    # Verify Database Persistence in voice_analyses table
    va_res = await db_session.execute(
        select(VoiceAnalysis).where(VoiceAnalysis.response_id == uuid.UUID(response["id"]))
    )
    saved_va = va_res.scalar_one_or_none()
    assert saved_va is not None
    assert saved_va.clarity_score == data["communication_score"]
    assert saved_va.filler_word_count >= 2
    assert saved_va.tone_evaluation is not None
    assert len(saved_va.communication_feedback) > 0

    # Verify InterviewSession.communication_score was updated
    s_res = await db_session.execute(
        select(InterviewSession).where(InterviewSession.id == uuid.UUID(session["id"]))
    )
    saved_session = s_res.scalar_one_or_none()
    assert saved_session is not None
    assert saved_session.communication_score is not None
    assert saved_session.communication_score == data["communication_score"]


@pytest.mark.asyncio
async def test_feedback_idempotent_recalculation(async_client: AsyncClient, db_session: AsyncSession):
    cookies = await register_and_get_cookies(async_client, "vf_idempotent@example.com")
    session, _, response = await setup_interview_response(async_client, cookies)

    # First call
    res1 = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/responses/{response['id']}/feedback",
        cookies=cookies,
    )
    assert res1.status_code == 200

    # Second call (idempotent recalculation)
    res2 = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/responses/{response['id']}/feedback",
        cookies=cookies,
    )
    assert res2.status_code == 200

    # Verify only ONE VoiceAnalysis record exists in the DB for this response
    va_res = await db_session.execute(
        select(VoiceAnalysis).where(VoiceAnalysis.response_id == uuid.UUID(response["id"]))
    )
    analyses = va_res.scalars().all()
    assert len(analyses) == 1
