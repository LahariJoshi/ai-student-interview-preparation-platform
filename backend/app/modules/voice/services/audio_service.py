import os
import re
import uuid
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Set
from uuid import UUID

from fastapi import UploadFile, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.interview.models import InterviewSession, InterviewResponse
from app.modules.voice.models import VoiceAnalysis
from app.modules.voice.schemas import AudioUploadOut

logger = logging.getLogger(__name__)

# Constants & Constraints
MAX_AUDIO_SIZE_BYTES = 25 * 1024 * 1024  # 25 MB
MIN_AUDIO_SIZE_BYTES = 100  # 100 bytes minimum

ALLOWED_AUDIO_EXTENSIONS: Set[str] = {
    ".webm",
    ".mp3",
    ".wav",
    ".m4a",
    ".ogg",
    ".mp4",
}

# Signatures for audio verification
WEBM_MAGIC_HEADER = b"\x1a\x45\xdf\xa3"
RIFF_MAGIC_HEADER = b"RIFF"
OGG_MAGIC_HEADER = b"OggS"
MP3_ID3_HEADER = b"ID3"
MP4_FTYP = b"ftyp"

# Dangerous binary signatures to explicitly block
DANGEROUS_HEADERS = [
    b"MZ",  # Windows Executable / DLL
    b"%PDF",  # PDF
    b"PK\x03\x04",  # Zip / Office
    b"\x7fELF",  # Linux Executable
    b"\x89PNG",  # PNG image
    b"GIF8",  # GIF image
    b"\xff\xd8\xff",  # JPEG image
    b"<html",
    b"<!DOCTYPE",
    b"<?php",
    b"#!/bin",
]


class AudioService:
    """
    Secure audio upload and storage service for candidate interview recordings.
    Enforces ownership validation, file type and size restrictions, path traversal prevention,
    and automatic cleanup of failed uploads.
    """

    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitizes uploaded filename and strictly blocks path traversal.
        """
        if not filename:
            return "recording.webm"

        # Check for path traversal attempts
        if ".." in filename or "/" in filename or "\\" in filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid filename: path traversal characters detected.",
            )

        # Extract only the base name
        base_name = Path(filename).name
        # Remove control characters
        base_name = re.sub(r"[\x00-\x1f\x7f]", "", base_name)
        # Replace non-alphanumeric except dots, dashes, underscores
        base_name = re.sub(r"[^\w\.-]", "_", base_name)

        return base_name or "recording.webm"

    @staticmethod
    def validate_audio_signature(header: bytes, ext: str) -> None:
        """
        Validates the audio file header signature to prevent executable or disguised files.
        """
        # 1. Reject dangerous signatures
        for dangerous in DANGEROUS_HEADERS:
            if header.startswith(dangerous) or dangerous in header[:16]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid file signature. File is not a valid audio format.",
                )

        # 2. Extension-specific signature checks
        if ext == ".wav" and not header.startswith(RIFF_MAGIC_HEADER):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid WAV file signature.",
            )

        if ext == ".webm" and not header.startswith(WEBM_MAGIC_HEADER):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid WebM file signature.",
            )

        if ext == ".ogg" and not header.startswith(OGG_MAGIC_HEADER):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OGG file signature.",
            )

        if ext in {".m4a", ".mp4"} and MP4_FTYP not in header[:16]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid M4A/MP4 audio file signature.",
            )

        if ext == ".mp3":
            is_id3 = header.startswith(MP3_ID3_HEADER)
            is_sync = (
                len(header) >= 2
                and header[0] == 0xFF
                and (header[1] & 0xE0) == 0xE0
            )
            if not is_id3 and not is_sync:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid MP3 file signature.",
                )

    async def save_audio_file(
        self,
        file: UploadFile,
        session_id: UUID,
        response_id: UUID,
    ) -> tuple[str, str, int, str]:
        """
        Validates, streams, and securely stores the audio recording to disk.
        Cleans up any partially written files if an error occurs.
        """
        raw_name = file.filename or "recording.webm"
        sanitized_name = self.sanitize_filename(raw_name)
        ext = Path(sanitized_name).suffix.lower()

        if ext not in ALLOWED_AUDIO_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported audio format '{ext}'. Allowed formats: {', '.join(sorted(ALLOWED_AUDIO_EXTENSIONS))}",
            )

        # Read first 512 bytes for signature validation
        header_bytes = await file.read(512)
        if not header_bytes or len(header_bytes) < 16:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded audio file is empty or corrupted.",
            )

        self.validate_audio_signature(header_bytes, ext)
        await file.seek(0)

        # Prepare secure storage directory
        storage_dir = os.path.join("uploads", "audio", str(session_id))
        os.makedirs(storage_dir, exist_ok=True)

        secure_filename = f"{response_id.hex}_{uuid.uuid4().hex[:8]}{ext}"
        destination_path = os.path.join(storage_dir, secure_filename)

        total_bytes = 0
        chunk_size = 512 * 1024  # 512 KB chunks

        try:
            with open(destination_path, "wb") as out_file:
                while True:
                    chunk = await file.read(chunk_size)
                    if not chunk:
                        break
                    total_bytes += len(chunk)

                    if total_bytes > MAX_AUDIO_SIZE_BYTES:
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Audio file exceeds the maximum allowed size limit of 25 MB.",
                        )
                    out_file.write(chunk)

            if total_bytes < MIN_AUDIO_SIZE_BYTES:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Uploaded audio file is too small to be a valid recording.",
                )

        except Exception as exc:
            # Clean up failed or partially written file immediately
            if os.path.exists(destination_path):
                try:
                    os.remove(destination_path)
                except OSError:
                    pass
            if isinstance(exc, HTTPException):
                raise
            logger.error(f"Failed to write audio file to disk: {exc}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An internal error occurred while saving the audio recording.",
            ) from exc

        mime_type = file.content_type or f"audio/{ext.lstrip('.')}"
        return destination_path, secure_filename, total_bytes, mime_type

    async def handle_audio_upload(
        self,
        db: AsyncSession,
        session_id: UUID,
        response_id: UUID,
        user_id: UUID,
        file: UploadFile,
        duration_seconds: Optional[float] = None,
    ) -> AudioUploadOut:
        """
        Coordinates full audio upload workflow:
        1. Verifies session ownership.
        2. Verifies response exists and belongs to the session.
        3. Saves file with strict validation and cleanup on error.
        4. Links audio file to InterviewResponse and VoiceAnalysis records.
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
                detail="You do not have permission to upload audio to this interview session.",
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

        # 3. Save audio file securely
        saved_path, filename, file_size, mime = await self.save_audio_file(
            file=file,
            session_id=session_id,
            response_id=response_id,
        )

        # 4. Update InterviewResponse model
        response.audio_file_path = saved_path
        if duration_seconds is not None and duration_seconds > 0:
            response.audio_duration_seconds = duration_seconds

        # 5. Link or initialize VoiceAnalysis record
        va_query = select(VoiceAnalysis).where(VoiceAnalysis.response_id == response_id)
        va_res = await db.execute(va_query)
        voice_analysis = va_res.scalar_one_or_none()

        if not voice_analysis:
            voice_analysis = VoiceAnalysis(
                response_id=response_id,
                audio_url=saved_path,
            )
            db.add(voice_analysis)
        else:
            voice_analysis.audio_url = saved_path

        await db.commit()
        await db.refresh(response)

        return AudioUploadOut(
            message="Audio uploaded successfully",
            response_id=response_id,
            session_id=session_id,
            file_name=filename,
            file_size_bytes=file_size,
            mime_type=mime,
            duration_seconds=duration_seconds,
            uploaded_at=datetime.now(timezone.utc),
        )


audio_service = AudioService()
