import io
import os
import uuid
import pytest
from httpx import AsyncClient

from app.modules.interview.services.llm_client import MockLLMClient, set_llm_client

pytestmark = pytest.mark.asyncio

WEBM_VALID_HEADER = b"\x1a\x45\xdf\xa3\x9f\x42\x86\x81\x01\x42\xf7\x81\x01\x42\xf2\x81\x04"
WAV_VALID_HEADER = b"RIFF" + b"\x24\x00\x00\x00" + b"WAVEfmt " + b"\x10\x00\x00\x00" + b"\x01\x00\x01\x00"


async def register_and_get_cookies(client: AsyncClient, email: str, name: str = "Test User"):
    reg_payload = {
        "email": email,
        "password": "Password123!",
        "full_name": name,
    }
    res = await client.post("/api/v1/auth/register", json=reg_payload)
    assert res.status_code == 201
    return res.cookies


async def setup_session_and_response(client: AsyncClient, cookies):
    set_llm_client(MockLLMClient())

    # 1. Create session
    create_res = await client.post(
        "/api/v1/interview/sessions",
        json={
            "target_role": "Voice Engineer",
            "interview_type": "Technical",
            "experience_level": "Intermediate",
            "difficulty": "Medium",
            "question_count": 2,
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

    # 3. Create response
    resp_res = await client.post(
        f"/api/v1/interview/sessions/{session['id']}/responses",
        json={
            "question_id": questions[0]["id"],
            "answer_text": "This is a candidate answer awaiting audio upload.",
        },
        cookies=cookies,
    )
    assert resp_res.status_code == 201
    response = resp_res.json()

    return session, questions, response


# ====================================================
# Voice Upload Tests
# ====================================================

async def test_upload_audio_unauthorized(async_client: AsyncClient):
    session_id = uuid.uuid4()
    response_id = uuid.uuid4()
    fake_audio = io.BytesIO(WEBM_VALID_HEADER + b"\x00" * 200)

    res = await async_client.post(
        f"/api/v1/voice/sessions/{session_id}/responses/{response_id}/audio",
        files={"file": ("recording.webm", fake_audio, "audio/webm")},
    )
    assert res.status_code == 401


async def test_upload_audio_wrong_session_ownership(async_client: AsyncClient):
    cookies_owner = await register_and_get_cookies(async_client, "voice_owner@example.com", "Owner")
    cookies_intruder = await register_and_get_cookies(async_client, "voice_intruder@example.com", "Intruder")

    session, _, response = await setup_session_and_response(async_client, cookies_owner)
    fake_audio = io.BytesIO(WEBM_VALID_HEADER + b"\x00" * 200)

    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/responses/{response['id']}/audio",
        files={"file": ("recording.webm", fake_audio, "audio/webm")},
        cookies=cookies_intruder,
    )
    assert res.status_code == 403
    assert "permission" in res.json()["detail"].lower()


async def test_upload_audio_session_not_found(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "voice_nf@example.com")
    fake_session_id = uuid.uuid4()
    fake_response_id = uuid.uuid4()
    fake_audio = io.BytesIO(WEBM_VALID_HEADER + b"\x00" * 200)

    res = await async_client.post(
        f"/api/v1/voice/sessions/{fake_session_id}/responses/{fake_response_id}/audio",
        files={"file": ("recording.webm", fake_audio, "audio/webm")},
        cookies=cookies,
    )
    assert res.status_code == 404
    assert "session not found" in res.json()["detail"].lower()


async def test_upload_audio_wrong_response_id(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "voice_wrong_resp@example.com")
    session, _, _ = await setup_session_and_response(async_client, cookies)

    fake_response_id = uuid.uuid4()
    fake_audio = io.BytesIO(WEBM_VALID_HEADER + b"\x00" * 200)

    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/responses/{fake_response_id}/audio",
        files={"file": ("recording.webm", fake_audio, "audio/webm")},
        cookies=cookies,
    )
    assert res.status_code == 404
    assert "response not found" in res.json()["detail"].lower()


async def test_upload_audio_response_mismatch_session(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "voice_mismatch@example.com")
    session1, _, response1 = await setup_session_and_response(async_client, cookies)
    session2, _, _ = await setup_session_and_response(async_client, cookies)

    fake_audio = io.BytesIO(WEBM_VALID_HEADER + b"\x00" * 200)

    # Trying to upload response1 to session2
    res = await async_client.post(
        f"/api/v1/voice/sessions/{session2['id']}/responses/{response1['id']}/audio",
        files={"file": ("recording.webm", fake_audio, "audio/webm")},
        cookies=cookies,
    )
    assert res.status_code == 400
    assert "does not belong" in res.json()["detail"].lower()


async def test_upload_valid_audio_webm(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "voice_valid_webm@example.com")
    session, _, response = await setup_session_and_response(async_client, cookies)

    payload_data = WEBM_VALID_HEADER + b"\x00" * 500
    audio_file = io.BytesIO(payload_data)

    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/responses/{response['id']}/audio",
        files={"file": ("candidate_answer.webm", audio_file, "audio/webm")},
        data={"duration_seconds": "18.5"},
        cookies=cookies,
    )
    assert res.status_code == 201
    data = res.json()
    assert data["response_id"] == response["id"]
    assert data["session_id"] == session["id"]
    assert data["file_size_bytes"] == len(payload_data)
    assert data["duration_seconds"] == 18.5
    assert data["mime_type"] == "audio/webm"
    assert "file_name" in data

    # Verify session detail reflects the uploaded audio
    session_res = await async_client.get(
        f"/api/v1/interview/sessions/{session['id']}",
        cookies=cookies,
    )
    assert session_res.status_code == 200
    session_detail = session_res.json()
    updated_resp = session_detail["responses"][0]
    assert updated_resp["audio_file_path"] is not None
    assert updated_resp["audio_duration_seconds"] == 18.5


async def test_upload_valid_audio_wav(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "voice_valid_wav@example.com")
    session, _, response = await setup_session_and_response(async_client, cookies)

    payload_data = WAV_VALID_HEADER + b"\x00" * 400
    audio_file = io.BytesIO(payload_data)

    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/responses/{response['id']}/audio",
        files={"file": ("interview.wav", audio_file, "audio/wav")},
        data={"duration_seconds": "12.0"},
        cookies=cookies,
    )
    assert res.status_code == 201
    data = res.json()
    assert data["response_id"] == response["id"]
    assert data["file_size_bytes"] == len(payload_data)


async def test_upload_invalid_audio_extension(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "voice_bad_ext@example.com")
    session, _, response = await setup_session_and_response(async_client, cookies)

    text_file = io.BytesIO(b"Hello world, this is text not audio.")

    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/responses/{response['id']}/audio",
        files={"file": ("notes.txt", text_file, "text/plain")},
        cookies=cookies,
    )
    assert res.status_code == 400
    assert "unsupported audio format" in res.json()["detail"].lower()


async def test_upload_disguised_file_signature_mismatch(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "voice_disguised@example.com")
    session, _, response = await setup_session_and_response(async_client, cookies)

    # Disguised as .webm but contains Windows executable header MZ
    fake_exe = io.BytesIO(b"MZ\x90\x00\x03\x00\x00\x00" + b"\x00" * 300)

    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/responses/{response['id']}/audio",
        files={"file": ("recording.webm", fake_exe, "audio/webm")},
        cookies=cookies,
    )
    assert res.status_code == 400
    assert "signature" in res.json()["detail"].lower()


async def test_upload_oversized_audio(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "voice_oversized@example.com")
    session, _, response = await setup_session_and_response(async_client, cookies)

    # 26 MB (exceeds 25 MB limit)
    oversized_data = WEBM_VALID_HEADER + b"\x00" * (26 * 1024 * 1024)
    huge_file = io.BytesIO(oversized_data)

    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/responses/{response['id']}/audio",
        files={"file": ("large_recording.webm", huge_file, "audio/webm")},
        cookies=cookies,
    )
    assert res.status_code == 400
    assert "exceeds" in res.json()["detail"].lower()


async def test_upload_empty_audio(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "voice_empty@example.com")
    session, _, response = await setup_session_and_response(async_client, cookies)

    empty_file = io.BytesIO(b"")

    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/responses/{response['id']}/audio",
        files={"file": ("empty.webm", empty_file, "audio/webm")},
        cookies=cookies,
    )
    assert res.status_code == 400
    assert "empty" in res.json()["detail"].lower()


async def test_upload_path_traversal_filename(async_client: AsyncClient):
    cookies = await register_and_get_cookies(async_client, "voice_traversal@example.com")
    session, _, response = await setup_session_and_response(async_client, cookies)

    payload_data = WEBM_VALID_HEADER + b"\x00" * 300
    audio_file = io.BytesIO(payload_data)

    res = await async_client.post(
        f"/api/v1/voice/sessions/{session['id']}/responses/{response['id']}/audio",
        files={"file": ("../../etc/passwd.webm", audio_file, "audio/webm")},
        cookies=cookies,
    )
    assert res.status_code == 400
    assert "traversal" in res.json()["detail"].lower()
