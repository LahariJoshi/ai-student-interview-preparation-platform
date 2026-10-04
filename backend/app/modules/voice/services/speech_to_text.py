import os
import re
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional
from uuid import UUID

import httpx
from fastapi import UploadFile, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.interview.models import InterviewSession, InterviewResponse
from app.modules.voice.models import VoiceAnalysis
from app.modules.voice.schemas import STTResultOut
from app.modules.voice.services.audio_service import (
    audio_service,
    ALLOWED_AUDIO_EXTENSIONS,
    DANGEROUS_HEADERS,
)

logger = logging.getLogger(__name__)


# ==========================================
# Custom STT Exceptions
# ==========================================
class STTClientError(Exception):
    """Base exception for speech-to-text errors."""
    pass


class STTTimeoutError(STTClientError):
    """Raised when speech-to-text request times out."""
    pass


class STTResponseError(STTClientError):
    """Raised when STT returns empty or malformed output."""
    pass


class CorruptedAudioError(STTClientError):
    """Raised when the audio recording file is corrupted or unreadable."""
    pass


class UnsupportedAudioError(STTClientError):
    """Raised when audio format is not supported."""
    pass


# ==========================================
# Abstract STT Provider Interface
# ==========================================
class BaseSTTClient(ABC):
    """Abstract interface for speech-to-text providers."""

    @abstractmethod
    async def transcribe(self, audio_file_path: str, mime_type: Optional[str] = None) -> STTResultOut:
        """Transcribes the audio file at audio_file_path into text."""
        pass


# ==========================================
# OpenAI Whisper Provider Implementation
# ==========================================
class WhisperSTTClient(BaseSTTClient):
    """OpenAI Whisper API client for real-world speech transcription."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        timeout_seconds: float = 30.0,
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.model = model or os.getenv("OPENAI_WHISPER_MODEL", "whisper-1")
        self.timeout_seconds = timeout_seconds
        self.endpoint = "https://api.openai.com/v1/audio/transcriptions"

    async def transcribe(self, audio_file_path: str, mime_type: Optional[str] = None) -> STTResultOut:
        if not self.api_key:
            raise STTClientError("OPENAI_API_KEY is not configured for Whisper STT.")

        if not os.path.exists(audio_file_path):
            raise CorruptedAudioError(f"Audio file not found: {audio_file_path}")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

        try:
            filename = Path(audio_file_path).name
            actual_mime = mime_type or "audio/webm"

            with open(audio_file_path, "rb") as f:
                file_bytes = f.read()

            files = {
                "file": (filename, file_bytes, actual_mime),
            }
            data = {
                "model": self.model,
                "response_format": "verbose_json",
            }

            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.post(self.endpoint, headers=headers, files=files, data=data)
                response.raise_for_status()
                res_data = response.json()

                transcript = res_data.get("text", "").strip()
                language = res_data.get("language", "en")
                confidence = 0.95

                if not transcript:
                    raise STTResponseError("Whisper returned an empty transcript.")

                return STTResultOut(
                    transcript=transcript,
                    language=language,
                    confidence=confidence,
                )

        except httpx.TimeoutException as exc:
            raise STTTimeoutError(f"Whisper STT request timed out after {self.timeout_seconds}s") from exc
        except httpx.HTTPStatusError as exc:
            raise STTClientError(f"Whisper API error: {exc.response.status_code} - {exc.response.text}") from exc
        except Exception as exc:
            if isinstance(exc, STTClientError):
                raise
            raise STTClientError(f"Unexpected error calling Whisper STT: {str(exc)}") from exc


# ==========================================
# Mock STT Client for Tests & Local Dev
# ==========================================
class MockSTTClient(BaseSTTClient):
    """
    Mock speech-to-text provider generating realistic transcripts without external API keys.
    Used in test suites and local development.
    """

    def __init__(
        self,
        canned_transcript: Optional[str] = None,
        canned_language: str = "en",
        canned_confidence: float = 0.95,
        simulate_error: Optional[str] = None,
    ):
        self.canned_transcript = canned_transcript
        self.canned_language = canned_language
        self.canned_confidence = canned_confidence
        self.simulate_error = simulate_error

    async def transcribe(self, audio_file_path: str, mime_type: Optional[str] = None) -> STTResultOut:
        if self.simulate_error == "timeout":
            raise STTTimeoutError("Simulated speech-to-text provider timeout.")
        elif self.simulate_error == "provider_error":
            raise STTClientError("Simulated speech-to-text service internal failure.")
        elif self.simulate_error == "empty":
            return STTResultOut(transcript="", language="en", confidence=0.0)
        elif self.simulate_error == "corrupted":
            raise CorruptedAudioError("Simulated audio decoder decompression error.")

        if self.canned_transcript is not None:
            return STTResultOut(
                transcript=self.canned_transcript,
                language=self.canned_language,
                confidence=self.canned_confidence,
            )

        # Generate realistic interview candidate response based on filename
        return STTResultOut(
            transcript=(
                "I implemented dependency injection and layered architecture to isolate our business logic. "
                "This enabled full unit test coverage and simplified integration with third-party APIs."
            ),
            language="en",
            confidence=0.96,
        )


# ==========================================
# Provider Factory & Registry
# ==========================================
_stt_client_instance: Optional[BaseSTTClient] = None


def get_stt_client() -> BaseSTTClient:
    """
    Factory function returning the configured STT client.
    Reads provider from STT_PROVIDER env var ('whisper', 'openai', 'mock').
    Defaults to MockSTTClient if API key is not present.
    """
    global _stt_client_instance
    if _stt_client_instance is not None:
        return _stt_client_instance

    provider = os.getenv("STT_PROVIDER", "mock").lower().strip()

    if (provider in ["whisper", "openai"]) and os.getenv("OPENAI_API_KEY"):
        return WhisperSTTClient()
    return MockSTTClient()


def set_stt_client(client: Optional[BaseSTTClient]) -> None:
    """Override STT client in unit and integration tests."""
    global _stt_client_instance
    _stt_client_instance = client


# ==========================================
# Speech-To-Text Service
# ==========================================
class SpeechToTextService:
    """
    High-level speech-to-text transcription service coordinating
    audio validation, provider calls, error mapping, and database storage.
    """

    def __init__(self, stt_client: Optional[BaseSTTClient] = None):
        self._stt_client = stt_client

    @property
    def stt_client(self) -> BaseSTTClient:
        return self._stt_client or get_stt_client()

    def validate_audio_file(self, audio_path: str) -> None:
        """
        Validates file existence, format support, minimum size, and basic integrity.
        """
        if not os.path.exists(audio_path):
            raise CorruptedAudioError(f"Audio recording file not found: {audio_path}")

        file_size = os.path.getsize(audio_path)
        if file_size < 50:
            raise CorruptedAudioError("Audio recording file is empty or corrupted (size < 50 bytes).")

        ext = Path(audio_path).suffix.lower()
        if ext not in ALLOWED_AUDIO_EXTENSIONS:
            raise UnsupportedAudioError(
                f"Unsupported audio format '{ext}'. Allowed: {', '.join(sorted(ALLOWED_AUDIO_EXTENSIONS))}"
            )

        # Check binary signature for obvious non-audio files
        with open(audio_path, "rb") as f:
            header = f.read(64)

        for dangerous in DANGEROUS_HEADERS:
            if header.startswith(dangerous) or dangerous in header[:16]:
                raise CorruptedAudioError("Invalid audio file signature: file content is not a valid audio stream.")

    async def transcribe_file(self, audio_path: str, mime_type: Optional[str] = None) -> STTResultOut:
        """
        Validates the audio recording and invokes the STT provider.
        """
        self.validate_audio_file(audio_path)

        result = await self.stt_client.transcribe(audio_path, mime_type=mime_type)

        if not result.transcript or not result.transcript.strip():
            raise STTResponseError("Speech-to-text service returned an empty transcript.")

        return result

    async def transcribe_response(
        self,
        db: AsyncSession,
        session_id: UUID,
        response_id: UUID,
        user_id: UUID,
        file: Optional[UploadFile] = None,
    ) -> STTResultOut:
        """
        Coordinates full transcription pipeline:
        1. Verifies session ownership.
        2. Verifies response exists and belongs to the session.
        3. Optionally receives and saves a new audio file, or uses existing audio_file_path.
        4. Validates audio integrity and transcribes via provider.
        5. Persists the resulting transcript to InterviewResponse.transcribed_text.
        """
        # 1. Verify session exists & user ownership
        s_query = select(InterviewSession).where(InterviewSession.id == session_id)
        s_res = await db.execute(s_query)
        session = s_res.scalar_one_or_none()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview session not found.",
            )

        if session.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to transcribe audio for this interview session.",
            )

        # 2. Verify response exists & belongs to this session
        r_query = select(InterviewResponse).where(InterviewResponse.id == response_id)
        r_res = await db.execute(r_query)
        response = r_res.scalar_one_or_none()
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview response not found.",
            )

        if response.session_id != session_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Interview response does not belong to this interview session.",
            )

        # 3. Handle incoming file upload if provided
        if file is not None:
            saved_path, _, _, _ = await audio_service.save_audio_file(
                file=file,
                session_id=session_id,
                response_id=response_id,
            )
            response.audio_file_path = saved_path

        # 4. Check that audio file path exists
        if not response.audio_file_path:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No audio recording found for this response. Please upload an audio file first.",
            )

        # 5. Transcribe with comprehensive error mapping
        try:
            stt_result = await self.transcribe_file(response.audio_file_path)
        except STTTimeoutError as exc:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Speech-to-text provider timed out. Please try again.",
            ) from exc
        except UnsupportedAudioError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc),
            ) from exc
        except CorruptedAudioError as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Corrupted or invalid audio file: {str(exc)}",
            ) from exc
        except STTResponseError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Speech-to-text service returned an empty or invalid transcript.",
            ) from exc
        except STTClientError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Speech-to-text service error: {str(exc)}",
            ) from exc

        # 6. Store transcript in database
        response.transcribed_text = stt_result.transcript.strip()

        await db.commit()
        await db.refresh(response)

        return stt_result


speech_to_text_service = SpeechToTextService()
