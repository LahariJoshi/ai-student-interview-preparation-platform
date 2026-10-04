import os
import logging
from typing import Optional
from uuid import UUID

from fastapi import UploadFile, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.interview.models import (
    InterviewSession,
    InterviewQuestion,
    InterviewResponse,
)
from app.modules.interview.services.answer_analyzer import (
    answer_analyzer,
    AnswerAnalyzerService,
    LLMClientError,
    LLMTimeoutError,
)
from app.modules.voice.models import VoiceAnalysis
from app.modules.voice.schemas import (
    VoicePipelineResultOut,
    VoiceMetricsOut,
    CommunicationFeedbackResult,
)
from app.modules.voice.services.audio_service import audio_service, AudioService
from app.modules.voice.services.speech_to_text import (
    speech_to_text_service,
    SpeechToTextService,
    STTClientError,
    STTTimeoutError,
    STTResponseError,
    CorruptedAudioError,
    UnsupportedAudioError,
)
from app.modules.voice.services.voice_metrics import (
    voice_metrics_service,
    VoiceMetricsService,
)
from app.modules.voice.services.voice_feedback import (
    voice_feedback_service,
    VoiceFeedbackService,
)

logger = logging.getLogger(__name__)


class VoicePipelineService:
    """
    Unified Voice & Interview Answer Processing Pipeline.
    Coordinates:
    Audio Storage -> Speech-To-Text -> AI Answer Analysis -> Voice Metrics -> Communication Feedback -> Database Persistence.
    """

    def __init__(
        self,
        audio_srv: Optional[AudioService] = None,
        stt_srv: Optional[SpeechToTextService] = None,
        analyzer_srv: Optional[AnswerAnalyzerService] = None,
        metrics_srv: Optional[VoiceMetricsService] = None,
        feedback_srv: Optional[VoiceFeedbackService] = None,
    ):
        self.audio_service = audio_srv or audio_service
        self.speech_to_text_service = stt_srv or speech_to_text_service
        self.answer_analyzer = analyzer_srv or answer_analyzer
        self.voice_metrics_service = metrics_srv or voice_metrics_service
        self.voice_feedback_service = feedback_srv or voice_feedback_service

    async def process_voice_pipeline(
        self,
        db: AsyncSession,
        session_id: UUID,
        user_id: UUID,
        question_id: Optional[UUID] = None,
        response_id: Optional[UUID] = None,
        file: Optional[UploadFile] = None,
        duration_seconds: Optional[float] = None,
    ) -> VoicePipelineResultOut:
        """
        Executes the complete voice interview pipeline for a response.
        """
        # 1. Verify session exists and belongs to current user
        s_res = await db.execute(
            select(InterviewSession).where(InterviewSession.id == session_id)
        )
        session = s_res.scalar_one_or_none()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview session not found.",
            )

        if session.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this interview session.",
            )

        if session.status == "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="This interview session is already completed.",
            )

        # 2. Resolve InterviewResponse if response_id provided
        response: Optional[InterviewResponse] = None
        if response_id is not None:
            r_res = await db.execute(
                select(InterviewResponse).where(InterviewResponse.id == response_id)
            )
            response = r_res.scalar_one_or_none()
            if not response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Interview response not found.",
                )
            if response.session_id != session_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Interview response does not belong to this session.",
                )
            if question_id is None:
                question_id = response.question_id
            elif response.question_id != question_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Response does not match the provided question ID.",
                )
        elif question_id is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either question_id or response_id must be provided.",
            )

        # 3. Resolve and validate InterviewQuestion exists in this session
        q_res = await db.execute(
            select(InterviewQuestion).where(
                InterviewQuestion.id == question_id,
                InterviewQuestion.session_id == session_id,
            )
        )
        question = q_res.scalar_one_or_none()
        if not question:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview question not found.",
            )

        # 4. Resolve or create InterviewResponse if not loaded by response_id
        if response is None:
            existing_res = await db.execute(
                select(InterviewResponse).where(
                    InterviewResponse.session_id == session_id,
                    InterviewResponse.question_id == question_id,
                )
            )
            response = existing_res.scalar_one_or_none()
            if response is None:
                response = InterviewResponse(
                    session_id=session_id,
                    question_id=question_id,
                    transcribed_text="[Audio Recording]",
                )
                db.add(response)
                await db.flush()

        # 5. Upload / Store Audio File
        if file is not None:
            saved_path, _, _, _ = await self.audio_service.save_audio_file(
                file=file,
                session_id=session_id,
                response_id=response.id,
            )
            response.audio_file_path = saved_path
            if duration_seconds is not None and duration_seconds > 0:
                response.audio_duration_seconds = duration_seconds
        else:
            if not response.audio_file_path or not os.path.exists(response.audio_file_path):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No audio recording file provided or found on server for this response.",
                )

        # 5. Speech-To-Text Transcription
        try:
            stt_result = await self.speech_to_text_service.transcribe_file(
                response.audio_file_path
            )
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
        except (STTResponseError, STTClientError) as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Speech-to-text service failure: {str(exc)}",
            ) from exc

        raw_transcript = (stt_result.transcript or "").strip()
        if not raw_transcript:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No spoken words could be detected in the audio recording. Please speak clearly into your microphone and try again.",
            )

        # 6. Store Transcript
        response.transcribed_text = raw_transcript
        if duration_seconds and (not response.audio_duration_seconds or response.audio_duration_seconds <= 0):
            response.audio_duration_seconds = duration_seconds

        # 7. AI Answer Evaluation (Content, Technical Correctness, Structure)
        try:
            analysis = await self.answer_analyzer.analyze_answer(
                question_text=question.question_text,
                answer_text=raw_transcript,
                category=question.category or "Technical",
                topic=question.topic,
                expected_points=question.expected_points or [],
                difficulty=question.difficulty or session.difficulty or "Medium",
                target_role=session.target_role or "Software Engineer",
            )
        except LLMTimeoutError as exc:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="AI answer evaluation timed out. Please try again.",
            ) from exc
        except (LLMClientError, ValueError) as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"AI answer evaluation failed: {str(exc)}",
            ) from exc

        # Update response scores and feedback
        response.score = analysis.score
        response.feedback_text = (
            "\n".join(analysis.feedback) if analysis.feedback else f"Score: {analysis.score}"
        )
        response.key_strengths = analysis.strengths
        response.missing_concepts = (
            analysis.improvements if analysis.improvements else analysis.weaknesses
        )

        # Update session overall & technical scores
        scores_res = await db.execute(
            select(InterviewResponse.score).where(
                InterviewResponse.session_id == session_id,
                InterviewResponse.score.is_not(None),
            )
        )
        all_scores = [s for s in scores_res.scalars().all() if s is not None]
        if response.score is not None and response.score not in all_scores:
            all_scores.append(response.score)

        if all_scores:
            avg_score = round(sum(all_scores) / len(all_scores), 1)
            session.overall_score = avg_score
            session.technical_score = avg_score

        # 8. Voice Delivery Metrics
        effective_duration = response.audio_duration_seconds or 30.0
        metrics = self.voice_metrics_service.analyze_metrics(
            transcript=raw_transcript,
            duration_seconds=effective_duration,
        )

        # 9. Communication Feedback
        comm_result = self.voice_feedback_service.generate_feedback(
            metrics=metrics,
            transcript=raw_transcript,
        )

        # 10. Persist Voice Analysis
        va_res = await db.execute(
            select(VoiceAnalysis).where(VoiceAnalysis.response_id == response.id)
        )
        va = va_res.scalar_one_or_none()

        speaking_wpm = metrics["speaking_rate"]["speech_rate_wpm"]
        filler_count = metrics["filler_analysis"]["filler_word_count"]
        filler_dict = metrics["filler_analysis"]["filler_words"]
        pause_count = metrics["pause_analysis"]["pause_count"]
        total_pause_sec = metrics["pause_analysis"]["total_pause_seconds"]

        tone_label = (
            "Clear & Measured"
            if comm_result.communication_score >= 85.0
            else "Conversational" if comm_result.communication_score >= 70.0 else "Developing Pace"
        )

        if not va:
            va = VoiceAnalysis(
                response_id=response.id,
                audio_url=response.audio_file_path,
                speaking_rate_wpm=speaking_wpm,
                filler_word_count=filler_count,
                filler_words_detected=filler_dict,
                pause_count=pause_count,
                total_pause_duration_seconds=total_pause_sec,
                clarity_score=comm_result.communication_score,
                confidence_score=comm_result.communication_score,
                tone_evaluation=tone_label,
                communication_feedback="\n\n".join(comm_result.feedback),
            )
            db.add(va)
        else:
            va.audio_url = response.audio_file_path
            va.speaking_rate_wpm = speaking_wpm
            va.filler_word_count = filler_count
            va.filler_words_detected = filler_dict
            va.pause_count = pause_count
            va.total_pause_duration_seconds = total_pause_sec
            va.clarity_score = comm_result.communication_score
            va.confidence_score = comm_result.communication_score
            va.tone_evaluation = tone_label
            va.communication_feedback = "\n\n".join(comm_result.feedback)

        # Update session communication_score average
        va_all_res = await db.execute(
            select(VoiceAnalysis.clarity_score)
            .join(InterviewResponse, VoiceAnalysis.response_id == InterviewResponse.id)
            .where(InterviewResponse.session_id == session_id)
        )
        all_comm_scores = [s for s in va_all_res.scalars().all() if s is not None]
        if comm_result.communication_score not in all_comm_scores:
            all_comm_scores.append(comm_result.communication_score)
        if all_comm_scores:
            session.communication_score = round(sum(all_comm_scores) / len(all_comm_scores), 1)

        # 11. Commit all pipeline changes
        await db.commit()
        await db.refresh(response)

        # 12. Return clean, comprehensive pipeline output
        return VoicePipelineResultOut(
            response_id=response.id,
            session_id=session_id,
            question_id=question.id,
            transcript=raw_transcript,
            answer_score=analysis.score,
            communication_score=comm_result.communication_score,
            answer_analysis=analysis,
            voice_metrics=VoiceMetricsOut(**metrics),
            communication_feedback=comm_result,
            status="completed",
        )


voice_pipeline_service = VoicePipelineService()
