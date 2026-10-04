import io
import uuid
import pytest
from httpx import AsyncClient

from app.modules.interview.services.llm_client import (
    MockLLMClient,
    set_llm_client,
    LLMTimeoutError,
    LLMClientError,
)
from app.modules.voice.services.speech_to_text import (
    MockSTTClient,
    set_stt_client,
    STTClientError,
    STTTimeoutError,
)

pytestmark = pytest.mark.asyncio

WEBM_VALID_HEADER = b"\x1a\x45\xdf\xa3\x9f\x42\x86\x81\x01\x42\xf7\x81\x01\x42\xf2\x81\x04"


# ====================================================
# Helpers
# ====================================================

async def register_user(client: AsyncClient, email: str, name: str = "Test User"):
    res = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "Password123!", "full_name": name},
    )
    assert res.status_code == 201
    return res.cookies


# ====================================================
# Comprehensive Member 3 Integration Suite
# ====================================================

async def test_full_member3_lifecycle(async_client: AsyncClient):
    """
    Validates the entire lifecycle:
    1. Session creation
    2. Session retrieval & verification
    3. Question generation & persistence
    4. Answer submission
    5. Answer evaluation
    6. Audio upload & Voice pipeline (STT, metrics, feedback)
    7. Final result aggregation
    8. History retrieval
    """
    set_llm_client(MockLLMClient())
    set_stt_client(MockSTTClient())

    cookies = await register_user(async_client, "full_lifecycle@example.com")

    # 1. Session Creation
    create_res = await async_client.post(
        "/api/v1/interview/sessions",
        json={
            "target_role": "Full Stack Engineer",
            "interview_type": "Mixed",
            "experience_level": "Intermediate",
            "difficulty": "Medium",
            "question_count": 2,
            "answer_mode": "Voice + Text",
            "target_company": "TechCorp",
        },
        cookies=cookies,
    )
    assert create_res.status_code == 201
    session = create_res.json()
    session_id = session["id"]
    assert session["status"] == "pending"
    assert session["target_role"] == "Full Stack Engineer"

    # 2. Session Retrieval
    get_res = await async_client.get(f"/api/v1/interview/sessions/{session_id}", cookies=cookies)
    assert get_res.status_code == 200
    assert get_res.json()["id"] == session_id

    # 3. Question Generation & Persistence
    q_gen_res = await async_client.post(
        f"/api/v1/interview/sessions/{session_id}/generate-questions",
        cookies=cookies,
    )
    assert q_gen_res.status_code == 201
    questions = q_gen_res.json()
    assert len(questions) == 2
    q1_id = questions[0]["id"]
    q2_id = questions[1]["id"]

    # Verify questions persist
    q_list_res = await async_client.get(f"/api/v1/interview/sessions/{session_id}/questions", cookies=cookies)
    assert q_list_res.status_code == 200
    assert len(q_list_res.json()) == 2

    # 4. Start Session
    start_res = await async_client.post(f"/api/v1/interview/sessions/{session_id}/start", cookies=cookies)
    assert start_res.status_code == 200
    assert start_res.json()["status"] == "in_progress"

    # 5. Answer Submission (Text answer for Q1)
    ans1_res = await async_client.post(
        f"/api/v1/interview/sessions/{session_id}/responses",
        json={
            "question_id": q1_id,
            "answer_text": "We implement RESTful APIs using FastAPI and PostgreSQL with indexing and caching.",
        },
        cookies=cookies,
    )
    assert ans1_res.status_code == 201
    r1_id = ans1_res.json()["id"]

    # 6. Answer Analysis
    eval1_res = await async_client.post(
        f"/api/v1/interview/sessions/{session_id}/evaluate-answer",
        json={"question_id": q1_id},
        cookies=cookies,
    )
    assert eval1_res.status_code == 200
    eval1_data = eval1_res.json()
    assert 0 <= eval1_data["score"] <= 100
    assert 0 <= eval1_data["technical_score"] <= 100
    assert isinstance(eval1_data["strengths"], list)
    assert isinstance(eval1_data["weaknesses"], list)

    # 7. Audio Upload & Voice Pipeline for Q2
    audio_bytes = WEBM_VALID_HEADER + b"\x00" * 800
    pipe_res = await async_client.post(
        f"/api/v1/voice/sessions/{session_id}/process-audio",
        files={"file": ("speech.webm", io.BytesIO(audio_bytes), "audio/webm")},
        data={"question_id": q2_id, "duration_seconds": "15.0"},
        cookies=cookies,
    )
    assert pipe_res.status_code == 200
    pipe_data = pipe_res.json()
    assert pipe_data["transcript"] != ""
    assert pipe_data["answer_score"] >= 0
    assert pipe_data["communication_score"] >= 0
    assert "filler_analysis" in pipe_data["voice_metrics"]
    assert "speaking_rate" in pipe_data["voice_metrics"]
    assert "pause_analysis" in pipe_data["voice_metrics"]

    # 8. Complete Session
    comp_res = await async_client.post(f"/api/v1/interview/sessions/{session_id}/complete", cookies=cookies)
    assert comp_res.status_code == 200
    assert comp_res.json()["status"] == "completed"

    # 9. Interview Result
    res_res = await async_client.get(f"/api/v1/interview/sessions/{session_id}/result", cookies=cookies)
    assert res_res.status_code == 200
    result_data = res_res.json()
    assert result_data["session_id"] == session_id
    assert 0 <= result_data["interview_score"] <= 100
    assert 0 <= result_data["technical_score"] <= 100
    assert 0 <= result_data["communication_score"] <= 100
    assert result_data["total_questions"] == 2
    assert result_data["answered_questions"] == 2
    assert "formatted_duration" in result_data

    # 10. Interview History
    hist_res = await async_client.get("/api/v1/interview/history", cookies=cookies)
    assert hist_res.status_code == 200
    hist_data = hist_res.json()
    assert hist_data["total"] >= 1
    found_item = next((item for item in hist_data["items"] if item["id"] == session_id), None)
    assert found_item is not None
    assert found_item["status"] == "completed"
    assert found_item["target_role"] == "Full Stack Engineer"
    assert found_item["overall_score"] is not None


# ====================================================
# Security Tests
# ====================================================

async def test_security_unauthenticated_access(async_client: AsyncClient):
    random_id = uuid.uuid4()
    # Sessions
    assert (await async_client.post("/api/v1/interview/sessions", json={})).status_code == 401
    assert (await async_client.get("/api/v1/interview/sessions")).status_code == 401
    assert (await async_client.get(f"/api/v1/interview/sessions/{random_id}")).status_code == 401
    assert (await async_client.post(f"/api/v1/interview/sessions/{random_id}/start")).status_code == 401
    assert (await async_client.post(f"/api/v1/interview/sessions/{random_id}/complete")).status_code == 401
    assert (await async_client.post(f"/api/v1/interview/sessions/{random_id}/generate-questions")).status_code == 401
    assert (await async_client.get(f"/api/v1/interview/sessions/{random_id}/questions")).status_code == 401
    assert (await async_client.post(f"/api/v1/interview/sessions/{random_id}/responses", json={})).status_code == 401
    assert (await async_client.post(f"/api/v1/interview/sessions/{random_id}/evaluate-answer", json={})).status_code == 401
    assert (await async_client.get(f"/api/v1/interview/sessions/{random_id}/result")).status_code == 401
    assert (await async_client.get("/api/v1/interview/history")).status_code == 401
    # Voice
    assert (await async_client.post(f"/api/v1/voice/sessions/{random_id}/responses/{random_id}/audio")).status_code == 401
    assert (await async_client.post(f"/api/v1/voice/sessions/{random_id}/process-audio")).status_code == 401


async def test_security_cross_user_isolation(async_client: AsyncClient):
    set_llm_client(MockLLMClient())
    user_a = await register_user(async_client, "sec_user_a@example.com", "User A")
    user_b = await register_user(async_client, "sec_user_b@example.com", "User B")

    # User A creates a session and questions
    s_res = await async_client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "Security Analyst", "question_count": 2},
        cookies=user_a,
    )
    session_a = s_res.json()
    s_id = session_a["id"]

    q_res = await async_client.post(
        f"/api/v1/interview/sessions/{s_id}/generate-questions",
        cookies=user_a,
    )
    questions_a = q_res.json()
    q_id = questions_a[0]["id"]

    # 1. User B tries to get User A's session -> 403
    res1 = await async_client.get(f"/api/v1/interview/sessions/{s_id}", cookies=user_b)
    assert res1.status_code == 403

    # 2. User B tries to start User A's session -> 403
    res2 = await async_client.post(f"/api/v1/interview/sessions/{s_id}/start", cookies=user_b)
    assert res2.status_code == 403

    # 3. User B tries to complete User A's session -> 403
    res3 = await async_client.post(f"/api/v1/interview/sessions/{s_id}/complete", cookies=user_b)
    assert res3.status_code == 403

    # 4. User B tries to get User A's questions -> 403
    res4 = await async_client.get(f"/api/v1/interview/sessions/{s_id}/questions", cookies=user_b)
    assert res4.status_code == 403

    # 5. User B tries to submit response to User A's session -> 403
    res5 = await async_client.post(
        f"/api/v1/interview/sessions/{s_id}/responses",
        json={"question_id": q_id, "answer_text": "Intruder answer"},
        cookies=user_b,
    )
    assert res5.status_code == 403

    # 6. User B tries to get User A's results -> 403
    res6 = await async_client.get(f"/api/v1/interview/sessions/{s_id}/result", cookies=user_b)
    assert res6.status_code == 403

    # 7. User B creates a session, but tries to answer using User A's question_id -> 404
    s_b_res = await async_client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "Security Analyst", "question_count": 2},
        cookies=user_b,
    )
    s_b_id = s_b_res.json()["id"]
    res7 = await async_client.post(
        f"/api/v1/interview/sessions/{s_b_id}/responses",
        json={"question_id": q_id, "answer_text": "Mismatched question"},
        cookies=user_b,
    )
    assert res7.status_code == 404

    # 8. User B tries to process-audio on User A's session -> 403
    audio = io.BytesIO(WEBM_VALID_HEADER + b"\x00" * 200)
    res8 = await async_client.post(
        f"/api/v1/voice/sessions/{s_id}/process-audio",
        files={"file": ("test.webm", audio, "audio/webm")},
        data={"question_id": q_id},
        cookies=user_b,
    )
    assert res8.status_code == 403


async def test_security_invalid_files_and_traversal(async_client: AsyncClient):
    cookies = await register_user(async_client, "sec_files@example.com")
    s_res = await async_client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "File Security", "question_count": 2},
        cookies=cookies,
    )
    session_id = s_res.json()["id"]

    q_res = await async_client.post(
        f"/api/v1/interview/sessions/{session_id}/generate-questions",
        cookies=cookies,
    )
    q_id = q_res.json()[0]["id"]

    # Invalid file type (.exe)
    res_exe = await async_client.post(
        f"/api/v1/voice/sessions/{session_id}/process-audio",
        files={"file": ("malware.exe", io.BytesIO(b"MZ\x90\x00"), "application/x-msdownload")},
        data={"question_id": q_id},
        cookies=cookies,
    )
    assert res_exe.status_code == 400
    assert "unsupported" in res_exe.json()["detail"].lower()

    # Oversized file
    big_file = io.BytesIO(WEBM_VALID_HEADER + b"0" * (26 * 1024 * 1024))
    res_big = await async_client.post(
        f"/api/v1/voice/sessions/{session_id}/process-audio",
        files={"file": ("huge.webm", big_file, "audio/webm")},
        data={"question_id": q_id},
        cookies=cookies,
    )
    assert res_big.status_code == 400
    assert "exceeds" in res_big.json()["detail"].lower()


# ====================================================
# Failure Handling Tests
# ====================================================

async def test_failure_ai_provider_error(async_client: AsyncClient):
    class FailingLLMClient(MockLLMClient):
        async def generate(self, prompt: str, system_prompt: str = None, **kwargs):
            raise LLMClientError("Upstream LLM provider failure")

    set_llm_client(FailingLLMClient())

    cookies = await register_user(async_client, "fail_ai@example.com")
    s_res = await async_client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "Backend", "question_count": 2},
        cookies=cookies,
    )
    session_id = s_res.json()["id"]

    # Question generation handles provider error
    q_res = await async_client.post(
        f"/api/v1/interview/sessions/{session_id}/generate-questions",
        cookies=cookies,
    )
    assert q_res.status_code in [500, 502]


async def test_failure_ai_timeout(async_client: AsyncClient):
    class TimeoutLLMClient(MockLLMClient):
        async def generate(self, prompt: str, system_prompt: str = None, **kwargs):
            raise LLMTimeoutError("LLM call timed out")

    set_llm_client(TimeoutLLMClient())

    cookies = await register_user(async_client, "timeout_ai@example.com")
    s_res = await async_client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "Backend", "question_count": 2},
        cookies=cookies,
    )
    session_id = s_res.json()["id"]

    q_res = await async_client.post(
        f"/api/v1/interview/sessions/{session_id}/generate-questions",
        cookies=cookies,
    )
    assert q_res.status_code == 504


async def test_failure_stt_provider_error(async_client: AsyncClient):
    set_llm_client(MockLLMClient())
    set_stt_client(MockSTTClient(simulate_error="provider_error"))

    cookies = await register_user(async_client, "fail_stt@example.com")
    s_res = await async_client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "Backend", "question_count": 2},
        cookies=cookies,
    )
    session_id = s_res.json()["id"]

    q_res = await async_client.post(
        f"/api/v1/interview/sessions/{session_id}/generate-questions",
        cookies=cookies,
    )
    q_id = q_res.json()[0]["id"]

    audio = io.BytesIO(WEBM_VALID_HEADER + b"\x00" * 300)
    pipe_res = await async_client.post(
        f"/api/v1/voice/sessions/{session_id}/process-audio",
        files={"file": ("speech.webm", audio, "audio/webm")},
        data={"question_id": q_id},
        cookies=cookies,
    )
    assert pipe_res.status_code in [500, 502]


# ====================================================
# Task 17 — Full End-to-End User Journey Verification
# ====================================================

async def test_task17_complete_journey_integration(async_client: AsyncClient):
    """
    Simulates the exact end-to-end journey:
    Login -> Profile -> Setup -> Session -> AI Questions -> Answer ->
    Voice Recording -> Speech-to-Text -> Answer Analysis -> Voice Analysis ->
    Feedback -> Result -> History
    """
    set_llm_client(MockLLMClient())
    set_stt_client(MockSTTClient())

    # 1. Register
    email = "journey_student@example.com"
    password = "SecurePassword123!"
    reg_res = await async_client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password, "full_name": "Journey Student"},
    )
    assert reg_res.status_code == 201

    # 2. Login (verifies existing auth)
    login_res = await async_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert login_res.status_code == 200
    cookies = login_res.cookies

    # 3. Profile update (reusing existing Profile data)
    prof_update = await async_client.put(
        "/api/v1/profile",
        json={"target_role": "AI Solutions Architect", "experience_level": "intermediate"},
        cookies=cookies,
    )
    assert prof_update.status_code == 200

    # 4. Profile retrieval (Setup page reads from /profile)
    prof_get = await async_client.get("/api/v1/profile", cookies=cookies)
    assert prof_get.status_code == 200
    prof_data = prof_get.json()
    assert prof_data["target_role"] == "AI Solutions Architect"

    # 5. Interview Setup (creates session based on profile)
    setup_res = await async_client.post(
        "/api/v1/interview/sessions",
        json={
            "target_role": prof_data["target_role"],
            "interview_type": "Technical",
            "experience_level": "Intermediate",
            "difficulty": "Hard",
            "question_count": 2,
            "answer_mode": "Voice + Text",
        },
        cookies=cookies,
    )
    assert setup_res.status_code == 201
    session = setup_res.json()
    session_id = session["id"]

    # 6. AI Questions generation
    q_gen = await async_client.post(
        f"/api/v1/interview/sessions/{session_id}/generate-questions",
        cookies=cookies,
    )
    assert q_gen.status_code == 201
    questions = q_gen.json()
    assert len(questions) == 2
    q1 = questions[0]
    q2 = questions[1]

    # 7. Start Session
    start_res = await async_client.post(f"/api/v1/interview/sessions/{session_id}/start", cookies=cookies)
    assert start_res.status_code == 200

    # 8. Text Answer (Q1)
    ans1_res = await async_client.post(
        f"/api/v1/interview/sessions/{session_id}/responses",
        json={
            "question_id": q1["id"],
            "answer_text": "We utilize vector embeddings with cosine similarity search for retrieval-augmented generation.",
        },
        cookies=cookies,
    )
    assert ans1_res.status_code == 201

    # 9. Voice Recording + Speech-to-Text + Voice Analysis + Communication Feedback (Q2)
    voice_bytes = WEBM_VALID_HEADER + b"\x00" * 600
    pipe_res = await async_client.post(
        f"/api/v1/voice/sessions/{session_id}/process-audio",
        files={"file": ("candidate_answer.webm", io.BytesIO(voice_bytes), "audio/webm")},
        data={"question_id": q2["id"], "duration_seconds": "22.5"},
        cookies=cookies,
    )
    assert pipe_res.status_code == 200
    pipe_data = pipe_res.json()
    assert pipe_data["transcript"] != ""
    assert pipe_data["communication_score"] > 0
    assert "filler_analysis" in pipe_data["voice_metrics"]
    assert "speaking_rate" in pipe_data["voice_metrics"]

    # 10. Complete Interview Session
    comp_res = await async_client.post(f"/api/v1/interview/sessions/{session_id}/complete", cookies=cookies)
    assert comp_res.status_code == 200

    # 11. Final Result Aggregation
    result_res = await async_client.get(f"/api/v1/interview/sessions/{session_id}/result", cookies=cookies)
    assert result_res.status_code == 200
    res_data = result_res.json()
    assert res_data["interview_score"] > 0
    assert res_data["technical_score"] > 0
    assert res_data["communication_score"] > 0
    assert res_data["total_questions"] == 2
    assert res_data["answered_questions"] == 2
    assert len(res_data["question_performance"]) == 2
    assert len(res_data["recommendations"]) > 0

    # 12. Interview History Retrieval
    hist_res = await async_client.get("/api/v1/interview/history", cookies=cookies)
    assert hist_res.status_code == 200
    hist_data = hist_res.json()
    assert hist_data["total"] >= 1
    found = next((i for i in hist_data["items"] if i["id"] == session_id), None)
    assert found is not None
    assert found["target_role"] == "AI Solutions Architect"
    assert found["status"] == "completed"
    assert found["overall_score"] == res_data["interview_score"]

