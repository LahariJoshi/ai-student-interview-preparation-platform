import io
import os
import uuid
import pytest
from httpx import AsyncClient

from app.modules.interview.services.llm_client import MockLLMClient, set_llm_client
from app.modules.voice.schemas import STTResultOut
from app.modules.voice.services.speech_to_text import (
    SpeechToTextService,
    MockSTTClient,
    set_stt_client,
    get_stt_client,
    STTClientError,
    STTTimeoutError,
    STTResponseError,
    CorruptedAudioError,
    UnsupportedAudioError,
)

pytestmark = pytest.mark.asyncio

WEBM_HEADER = b"\x1a\x45\xdf\xa3\x9f\x42\x86\x81\x01\x42\xf7\x81\x01\x42\xf2\x81\x04"


# ====================================================
# Unit Tests for SpeechToTextService & Mock Client
# ====================================================

async def test_mock_stt_client_transcribe(tmp_path):
    dummy_file = tmp_path / "valid.webm"
    dummy_file.write_bytes(WEBM_HEADER + b"\x00" * 200)

    client = MockSTTClient(
        canned_transcript="I prefer using PostgreSQL because of its robust transaction isolation and JSON support.",
        canned_language="en",
        canned_confidence=0.98,
    )
    result = await client.transcribe(str(dummy_file))

    assert isinstance(result, STTResultOut)
    assert "PostgreSQL" in result.transcript
    assert result.language == "en"
    assert result.confidence == 0.98


async def test_transcribe_service_nonexistent_file():
    service = SpeechToTextService(stt_client=MockSTTClient())
    with pytest.raises(CorruptedAudioError, match="not found"):
        await service.transcribe_file("nonexistent_path_to_audio.webm")


async def test_transcribe_service_empty_file(tmp_path):
    empty_file = tmp_path / "empty.webm"
    empty_file.write_bytes(b"")

    service = SpeechToTextService(stt_client=MockSTTClient())
    with pytest.raises(CorruptedAudioError, match="empty or corrupted"):
        await service.transcribe_file(str(empty_file))


async def test_transcribe_service_unsupported_format(tmp_path):
    bad_file = tmp_path / "notes.txt"
    bad_file.write_bytes(b"This is just a text file with lots of notes to exceed 50 bytes minimum.")

    service = SpeechToTextService(stt_client=MockSTTClient())
    with pytest.raises(UnsupportedAudioError, match="Unsupported audio format"):
        await service.transcribe_file(str(bad_file))


async def test_transcribe_service_corrupted_signature(tmp_path):
    disguised_file = tmp_path / "fake.webm"
    disguised_file.write_bytes(b"%PDF-1.5 fake pdf content pretending to be webm format padding padding")

    service = SpeechToTextService(stt_client=MockSTTClient())
    with pytest.raises(CorruptedAudioError, match="Invalid audio file signature"):
        await service.transcribe_file(str(disguised_file))


async def test_transcribe_service_timeout(tmp_path):
    valid_file = tmp_path / "timeout.webm"
    valid_file.write_bytes(WEBM_HEADER + b"\x00" * 150)

    service = SpeechToTextService(stt_client=MockSTTClient(simulate_error="timeout"))
    with pytest.raises(STTTimeoutError):
        await service.transcribe_file(str(valid_file))


async def test_transcribe_service_provider_error(tmp_path):
    valid_file = tmp_path / "error.webm"
    valid_file.write_bytes(WEBM_HEADER + b"\x00" * 150)

    service = SpeechToTextService(stt_client=MockSTTClient(simulate_error="provider_error"))
    with pytest.raises(STTClientError):
        await service.transcribe_file(str(valid_file))


async def test_transcribe_service_empty_transcript_handling(tmp_path):
    valid_file = tmp_path / "empty_transcript.webm"
    valid_file.write_bytes(WEBM_HEADER + b"\x00" * 150)

    service = SpeechToTextService(stt_client=MockSTTClient(simulate_error="empty"))
    with pytest.raises(STTResponseError, match="empty transcript"):
        await service.transcribe_file(str(valid_file))


# ====================================================
# API Integration Tests
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


async def setup_interview_with_audio(client: AsyncClient, cookies):
    set_llm_client(MockLLMClient())
    set_stt_client(MockSTTClient())

    # 1. Create session
    create_res = await client.post(
        "/api/v1/interview/sessions",
        json={
            "target_role": "Voice Engineer",
            "interview_type": "Technical",
            "experience_level": "Intermediate",
            "difficulty": "Medium",
            "question_count": 2,
            "answer_mode": "Voice",
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

    # 3. Create response
    resp_res = await client.post(
        f"/api/v1/interview/sessions/{session['id']}/responses",
        json={
            "question_id": questions[0]["id"],
            "answer_text": "[Audio pending transcription]",
        },
        cookies=cookies,
    )
    assert resp_res.status_code == 201
    response = resp_res.json()

    # 4. Upload audio
    audio_file = io.BytesIO(WEBM_HEADER + b"\x00" * 500)
    upload_res = await client.post(
        f"/api/v1/voice/sessions/{session['id']}/responses/{response['id']}/audio",
        files={"file": ("interview_recording.webm", audio_file, "audio/webm")},
        data={"duration_seconds": "15.0"},
        cookies=cookies,
    )
    assert upload_res.status_code == 201

    return session, questions, response


async def test_transcribe_unauthorized(async_client: AsyncClient):
    session_id = uuid.uuid4()
    response_id = uuid.uuid4()
    res = await async_client.post(
        f"/api/v1/voice/sessions/{session_id}/responses/{response_id}/transcribe"
    )
    assert res.status_code == 401


async def test_transcribe_forbidden_other_user(async_client: AsyncClient):
    cookies_owner = await register_and_get_cookies(async_client, "stt_owner@example.com", "Owner")
    cookies_intruder = await register_and_get_cookies(async_client, "stt_intruder@example.com", "Intruder")

    session, _, response = await setup_interview_with_audio(async_client, cookies_owner)

    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/responses/{response['id']}/transcribe",
        cookies=cookies_intruder,
    )
    assert res.status_code == 403


async def test_transcribe_response_not_found(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "stt_nf@example.com")
    session, _, _ = await setup_interview_with_audio(async_client, cookies)

    fake_response_id = uuid.uuid4()
    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/responses/{fake_response_id}/transcribe",
        cookies=cookies,
    )
    assert res.status_code == 404


async def test_transcribe_no_audio_file(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "stt_no_audio@example.com")
    set_llm_client(MockLLMClient())

    # Create session and response without uploading audio
    create_res = await async_client.post(
        "/api/v1/interview/sessions",
        json={"target_role": "Developer", "difficulty": "Easy"},
        cookies=cookies,
    )
    session = create_res.json()

    q_res = await async_client.post(
        f"/api/v1/interview/sessions/{session['id']}/generate-questions",
        cookies=cookies,
    )
    questions = q_res.json()

    resp_res = await async_client.post(
        f"/api/v1/interview/sessions/{session['id']}/responses",
        json={"question_id": questions[0]["id"], "answer_text": "Text only answer"},
        cookies=cookies,
    )
    response = resp_res.json()

    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/responses/{response['id']}/transcribe",
        cookies=cookies,
    )
    assert res.status_code == 400
    assert "no audio recording found" in res.json()["detail"].lower()


async def test_transcribe_success_and_db_persistence(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "stt_success@example.com")
    session, _, response = await setup_interview_with_audio(async_client, cookies)

    expected_transcript = (
        "I designed our microservices with asynchronous message brokers to ensure event delivery decoupling."
    )
    set_stt_client(MockSTTClient(canned_transcript=expected_transcript))

    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/responses/{response['id']}/transcribe",
        cookies=cookies,
    )
    assert res.status_code == 200
    data = res.json()

    # Verify return format
    assert data["transcript"] == expected_transcript
    assert data["language"] == "en"
    assert "confidence" in data
    assert 0.0 <= data["confidence"] <= 1.0

    # Verify database persistence: check response transcribed_text
    session_res = await async_client.get(
        f"/api/v1/interview/sessions/{session['id']}",
        cookies=cookies,
    )
    assert session_res.status_code == 200
    updated_session = session_res.json()
    updated_response = updated_session["responses"][0]
    assert updated_response["transcribed_text"] == expected_transcript


async def test_transcribe_with_file_in_request(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "stt_direct_upload@example.com")
    session, questions, response = await setup_interview_with_audio(async_client, cookies)

    expected_transcript = "Direct audio upload transcribed successfully."
    set_stt_client(MockSTTClient(canned_transcript=expected_transcript))

    audio_bytes = io.BytesIO(WEBM_HEADER + b"\x00" * 300)
    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/responses/{response['id']}/transcribe",
        files={"file": ("direct_recording.webm", audio_bytes, "audio/webm")},
        cookies=cookies,
    )
    assert res.status_code == 200
    data = res.json()
    assert data["transcript"] == expected_transcript


async def test_transcribe_timeout_api_mapping(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "stt_timeout@example.com")
    session, _, response = await setup_interview_with_audio(async_client, cookies)

    set_stt_client(MockSTTClient(simulate_error="timeout"))

    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/responses/{response['id']}/transcribe",
        cookies=cookies,
    )
    assert res.status_code == 504
    assert "timed out" in res.json()["detail"].lower()
    set_stt_client(MockSTTClient())


async def test_transcribe_empty_transcript_api_mapping(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "stt_empty@example.com")
    session, _, response = await setup_interview_with_audio(async_client, cookies)

    set_stt_client(MockSTTClient(simulate_error="empty"))

    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/responses/{response['id']}/transcribe",
        cookies=cookies,
    )
    assert res.status_code == 502
    assert "empty or invalid" in res.json()["detail"].lower()
    set_stt_client(MockSTTClient())
