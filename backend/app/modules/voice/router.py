from typing import Optional
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_current_user
from app.db.models.user import User
from app.modules.voice.schemas import (
    AudioUploadOut,
    STTResultOut,
    VoiceMetricsRequest,
    VoiceMetricsOut,
    CommunicationFeedbackResult,
    VoicePipelineResultOut,
)
from app.modules.voice.services.audio_service import audio_service
from app.modules.voice.services.speech_to_text import speech_to_text_service
from app.modules.voice.services.voice_metrics import voice_metrics_service
from app.modules.voice.services.voice_feedback import voice_feedback_service
from app.modules.voice.services.voice_pipeline import voice_pipeline_service

router = APIRouter(
    prefix="/voice",
    tags=["Voice"],
)


@router.post(
    "/sessions/{session_id}/responses/{response_id}/audio",
    response_model=AudioUploadOut,
    status_code=status.HTTP_201_CREATED,
    summary="Upload and securely store audio recording for an interview response",
)
async def upload_response_audio(
    session_id: UUID,
    response_id: UUID,
    file: UploadFile = File(..., description="Audio recording file (webm, mp3, wav, m4a, ogg)"),
    duration_seconds: Optional[float] = Form(None, description="Optional recorded duration in seconds"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await audio_service.handle_audio_upload(
        db=db,
        session_id=session_id,
        response_id=response_id,
        user_id=current_user.id,
        file=file,
        duration_seconds=duration_seconds,
    )


@router.post(
    "/sessions/{session_id}/responses/{response_id}/transcribe",
    response_model=STTResultOut,
    status_code=status.HTTP_200_OK,
    summary="Transcribe response audio into text using speech-to-text service",
)
async def transcribe_response_audio(
    session_id: UUID,
    response_id: UUID,
    file: Optional[UploadFile] = File(None, description="Optional audio file to upload and transcribe in one step"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await speech_to_text_service.transcribe_response(
        db=db,
        session_id=session_id,
        response_id=response_id,
        user_id=current_user.id,
        file=file,
    )


@router.post(
    "/metrics",
    response_model=VoiceMetricsOut,
    status_code=status.HTTP_200_OK,
    summary="Calculate filler words, speaking rate, and pause metrics from text and duration",
)
async def calculate_voice_metrics(
    payload: VoiceMetricsRequest,
    current_user: User = Depends(get_current_user),
):
    return voice_metrics_service.analyze_metrics(
        transcript=payload.transcribed_text,
        duration_seconds=payload.duration_seconds,
    )


@router.post(
    "/sessions/{session_id}/responses/{response_id}/feedback",
    response_model=CommunicationFeedbackResult,
    status_code=status.HTTP_200_OK,
    summary="Generate and persist communication feedback for an interview response",
)
async def generate_response_communication_feedback(
    session_id: UUID,
    response_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await voice_feedback_service.generate_and_store_feedback(
        db=db,
        session_id=session_id,
        response_id=response_id,
        user_id=current_user.id,
    )


@router.post(
    "/sessions/{session_id}/process-audio",
    response_model=VoicePipelineResultOut,
    status_code=status.HTTP_200_OK,
    summary="Execute complete voice pipeline (Upload -> STT -> Analysis -> Metrics -> Feedback -> Persistence)",
)
async def process_session_audio_pipeline(
    session_id: UUID,
    question_id: UUID = Form(..., description="ID of the interview question being answered"),
    file: UploadFile = File(..., description="Recorded audio file"),
    duration_seconds: Optional[float] = Form(None, description="Recorded audio duration in seconds"),
    response_id: Optional[UUID] = Form(None, description="Optional response ID if retrying an existing response"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await voice_pipeline_service.process_voice_pipeline(
        db=db,
        session_id=session_id,
        user_id=current_user.id,
        question_id=question_id,
        response_id=response_id,
        file=file,
        duration_seconds=duration_seconds,
    )


@router.post(
    "/sessions/{session_id}/responses/{response_id}/process-audio",
    response_model=VoicePipelineResultOut,
    status_code=status.HTTP_200_OK,
    summary="Execute complete voice pipeline for an existing interview response",
)
async def process_response_audio_pipeline(
    session_id: UUID,
    response_id: UUID,
    file: Optional[UploadFile] = File(None, description="Optional audio file if not uploaded yet"),
    duration_seconds: Optional[float] = Form(None, description="Recorded audio duration in seconds"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await voice_pipeline_service.process_voice_pipeline(
        db=db,
        session_id=session_id,
        user_id=current_user.id,
        response_id=response_id,
        file=file,
        duration_seconds=duration_seconds,
    )




