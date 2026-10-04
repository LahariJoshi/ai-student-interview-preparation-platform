import re
import logging
from typing import Dict, List, Optional, Any
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.interview.models import InterviewSession, InterviewResponse
from app.modules.voice.models import VoiceAnalysis
from app.modules.voice.schemas import CommunicationFeedbackResult
from app.modules.voice.services.voice_metrics import voice_metrics_service, VoiceMetricsService

logger = logging.getLogger(__name__)


class VoiceFeedbackService:
    """
    Constructive voice and communication feedback engine.
    Analyzes speaking pace, filler words, pause timing, and structural delivery.

    Strict Ethical & Technical Boundaries:
    - Never makes medical, neurological, or psychological claims.
    - Never diagnoses anxiety, speech disorders, or mental health states.
    - Does not infer personal character, emotional stability, or intrinsic traits.
    - Explicitly treats vocal metrics as delivery coaching signals rather than
      a complete measure of engineering or interview competence.
    """

    def __init__(self, metrics_service: Optional[VoiceMetricsService] = None):
        self.metrics_service = metrics_service or voice_metrics_service

    def evaluate_transcript_structure(self, transcript: str) -> Dict[str, Any]:
        """
        Analyzes basic sentence count and average sentence length for flow.
        """
        if not transcript or not transcript.strip():
            return {"sentence_count": 0, "avg_sentence_words": 0.0, "is_run_on": False}

        sentences = [s.strip() for s in re.split(r"[.!?]+", transcript) if s.strip()]
        sentence_count = max(1, len(sentences))
        total_words = len(transcript.strip().split())
        avg_sentence_words = round(total_words / sentence_count, 1)

        return {
            "sentence_count": sentence_count,
            "avg_sentence_words": avg_sentence_words,
            "is_run_on": avg_sentence_words > 35.0,
        }

    def compute_communication_score(
        self,
        speaking_rate_wpm: float,
        filler_rate: float,
        pause_data_available: bool,
        average_pause_seconds: float,
    ) -> float:
        """
        Computes an objective, normalized delivery score (0-100) based on
        cadence, verbal economy, and pause distribution.
        """
        # 1. Pacing subscore (0-100)
        # Optimal interview baseline is 120-160 WPM
        if 120.0 <= speaking_rate_wpm <= 160.0:
            pace_score = 100.0
        elif 105.0 <= speaking_rate_wpm < 120.0:
            pace_score = 85.0 + (speaking_rate_wpm - 105.0) * 1.0
        elif 160.0 < speaking_rate_wpm <= 180.0:
            pace_score = 100.0 - (speaking_rate_wpm - 160.0) * 1.0
        elif 80.0 <= speaking_rate_wpm < 105.0:
            pace_score = 70.0 + (speaking_rate_wpm - 80.0) * 0.6
        elif 180.0 < speaking_rate_wpm <= 210.0:
            pace_score = 80.0 - (speaking_rate_wpm - 180.0) * 0.7
        elif speaking_rate_wpm > 0.0:
            pace_score = 55.0
        else:
            pace_score = 0.0

        # 2. Filler-rate subscore (0-100)
        # 0 - 1.5% fillers is excellent; > 6% indicates excessive verbal crutches
        if filler_rate <= 1.5:
            filler_score = 100.0
        elif filler_rate <= 3.5:
            filler_score = 90.0 - (filler_rate - 1.5) * 5.0
        elif filler_rate <= 6.0:
            filler_score = 80.0 - (filler_rate - 3.5) * 6.0
        else:
            filler_score = max(40.0, 65.0 - (filler_rate - 6.0) * 4.0)

        # 3. Pause subscore (if precise timing available)
        if pause_data_available:
            if 0.5 <= average_pause_seconds <= 1.6:
                pause_score = 95.0
            elif average_pause_seconds < 0.5:
                pause_score = 85.0  # Slightly rushed between sentences
            elif average_pause_seconds <= 2.5:
                pause_score = 80.0
            else:
                pause_score = 65.0  # Prolonged silent gaps

            # 40% pacing, 35% filler control, 25% pause distribution
            final_score = (pace_score * 0.40) + (filler_score * 0.35) + (pause_score * 0.25)
        else:
            # 55% pacing, 45% filler control
            final_score = (pace_score * 0.55) + (filler_score * 0.45)

        return round(max(0.0, min(100.0, final_score)), 1)

    def generate_feedback(
        self,
        metrics: Dict[str, Any],
        transcript: str,
    ) -> CommunicationFeedbackResult:
        """
        Generates actionable, pedagogical coaching feedback from speech metrics.
        Explains clearly WHY each observation was generated.
        """
        speaking = metrics.get("speaking_rate", {})
        fillers = metrics.get("filler_analysis", {})
        pauses = metrics.get("pause_analysis", {})

        wpm = speaking.get("speech_rate_wpm", 0.0)
        word_count = speaking.get("word_count", 0)
        duration_sec = speaking.get("duration_seconds", 0.0)

        filler_count = fillers.get("filler_word_count", 0)
        filler_rate = fillers.get("filler_rate", 0.0)
        filler_breakdown = fillers.get("filler_words", {})

        pause_count = pauses.get("pause_count", 0)
        avg_pause = pauses.get("average_pause_seconds", 0.0)
        data_available = pauses.get("data_availability") == "precise"

        structure = self.evaluate_transcript_structure(transcript)

        strengths: List[str] = []
        areas_to_improve: List[str] = []
        feedback_paragraphs: List[str] = []

        # --- 1. Speaking Rate Feedback & Rationale ---
        if 120.0 <= wpm <= 160.0:
            strengths.append(
                f"Optimal Speaking Cadence: Your delivery rate of {wpm} WPM is within the 120-160 WPM ideal interview baseline, facilitating clear comprehension."
            )
            feedback_paragraphs.append(
                f"Pacing: Your pace ({wpm} WPM) strikes an effective balance between enthusiasm and clarity. Interviewers can comfortably process your technical architecture and trade-offs without feeling rushed."
            )
        elif wpm < 120.0 and wpm > 0.0:
            areas_to_improve.append(
                f"Pacing Acceleration: Your speaking pace was {wpm} WPM (recommended: 120-160 WPM). Aim to speak slightly more briskly to maximize coverage in timed interviews."
            )
            feedback_paragraphs.append(
                f"Pacing Rationale: At {wpm} WPM, detailed technical responses may take longer than necessary, reducing the total number of questions covered. Practicing concise sentence formulation will help bring your cadence toward 130-140 WPM."
            )
        elif wpm > 160.0:
            areas_to_improve.append(
                f"Moderate Delivery Pace: Your rate of {wpm} WPM is faster than the recommended 120-160 WPM window. Deliberately slowing your cadence helps highlight key points."
            )
            feedback_paragraphs.append(
                f"Pacing Rationale: Speaking at {wpm} WPM can lead interviewers to miss nuance in complex engineering explanations. Inserting deliberate pauses between thoughts ensures key conclusions land effectively."
            )
        else:
            feedback_paragraphs.append(
                "Pacing: Audio duration or word count was insufficient to calculate an accurate speaking cadence."
            )

        # --- 2. Filler-Word Feedback & Rationale ---
        if filler_rate <= 1.5:
            strengths.append(
                f"High Verbal Economy: Minimal filler usage ({filler_rate}% filler rate, {filler_count} detected), giving your explanation a structured, decisive impression."
            )
            feedback_paragraphs.append(
                "Verbal Economy: Your choice of vocabulary was disciplined. Using few verbal crutches allows your actual technical insights to stand out."
            )
        else:
            top_fillers = sorted(filler_breakdown.items(), key=lambda x: -x[1])[:3]
            top_str = ", ".join(f"'{k}' ({v}x)" for k, v in top_fillers)
            areas_to_improve.append(
                f"Filler Word Reduction: Filler words represented {filler_rate}% of spoken vocabulary (predominantly {top_str}). Replace vocal fillers with brief silent pauses."
            )
            feedback_paragraphs.append(
                f"Filler Words Rationale: Fillers such as {top_str} typically occur as verbal bridges while organizing the next thought. Practicing silent pauses instead of verbal placeholders enhances clarity and gives you time to structure your next sentence."
            )

        # --- 3. Pause Analysis & Pacing Transitions ---
        if data_available:
            if 0.5 <= avg_pause <= 1.6:
                strengths.append(
                    f"Natural Pause Distribution: You paused an average of {avg_pause}s between segments, providing natural transition points."
                )
            elif avg_pause > 2.0:
                areas_to_improve.append(
                    f"Transition Fluidity: Recorded pauses averaged {avg_pause}s. Keeping transitional pauses around 1.0s maintains delivery momentum."
                )
        else:
            feedback_paragraphs.append(
                "Timing Note: Detailed hardware pause telemetry was not recorded for this response and was not factored into precision scoring."
            )

        # --- 4. Structural Sentence Flow ---
        if structure["is_run_on"]:
            areas_to_improve.append(
                f"Sentence Chunking: Sentences averaged {structure['avg_sentence_words']} words. Breaking lengthy thoughts into shorter, distinct statements improves listener retention."
            )

        # --- 5. Mandatory Ethical Coaching Disclaimer ---
        feedback_paragraphs.append(
            "Communication Coaching Note: Speaking metrics measure verbal pacing, pause cadence, and clarity of articulation. They are an educational practice tool and should always be evaluated alongside technical depth, problem-solving reasoning, and domain competence."
        )

        communication_score = self.compute_communication_score(
            speaking_rate_wpm=wpm,
            filler_rate=filler_rate,
            pause_data_available=data_available,
            average_pause_seconds=avg_pause,
        )

        return CommunicationFeedbackResult(
            communication_score=communication_score,
            strengths=strengths,
            areas_to_improve=areas_to_improve,
            feedback=feedback_paragraphs,
            metrics=metrics,
        )

    async def generate_and_store_feedback(
        self,
        db: AsyncSession,
        session_id: UUID,
        response_id: UUID,
        user_id: UUID,
    ) -> CommunicationFeedbackResult:
        """
        Coordinates full feedback generation and database persistence in voice_analyses:
        1. Verifies session ownership and response validity.
        2. Computes voice metrics.
        3. Generates structured feedback.
        4. Persists the analysis in voice_analyses table.
        5. Updates session communication score average.
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
                detail="You do not have permission to access this interview session.",
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

        transcript = response.transcribed_text or response.answer_text or ""
        duration = response.audio_duration_seconds or 30.0

        # 3. Calculate voice metrics
        metrics = self.metrics_service.analyze_metrics(
            transcript=transcript,
            duration_seconds=duration,
        )

        # 4. Generate feedback
        result = self.generate_feedback(metrics=metrics, transcript=transcript)

        # 5. Persist into voice_analyses table
        va_query = select(VoiceAnalysis).where(VoiceAnalysis.response_id == response_id)
        va_res = await db.execute(va_query)
        voice_analysis = va_res.scalar_one_or_none()

        speaking_wpm = metrics["speaking_rate"]["speech_rate_wpm"]
        filler_count = metrics["filler_analysis"]["filler_word_count"]
        filler_dict = metrics["filler_analysis"]["filler_words"]
        pause_count = metrics["pause_analysis"]["pause_count"]
        total_pause_sec = metrics["pause_analysis"]["total_pause_seconds"]

        tone_label = (
            "Clear & Measured"
            if result.communication_score >= 85.0
            else "Conversational" if result.communication_score >= 70.0 else "Developing Pace"
        )

        if not voice_analysis:
            voice_analysis = VoiceAnalysis(
                response_id=response_id,
                audio_url=response.audio_file_path,
                speaking_rate_wpm=speaking_wpm,
                filler_word_count=filler_count,
                filler_words_detected=filler_dict,
                pause_count=pause_count,
                total_pause_duration_seconds=total_pause_sec,
                clarity_score=result.communication_score,
                confidence_score=result.communication_score,
                tone_evaluation=tone_label,
                communication_feedback="\n\n".join(result.feedback),
            )
            db.add(voice_analysis)
        else:
            voice_analysis.speaking_rate_wpm = speaking_wpm
            voice_analysis.filler_word_count = filler_count
            voice_analysis.filler_words_detected = filler_dict
            voice_analysis.pause_count = pause_count
            voice_analysis.total_pause_duration_seconds = total_pause_sec
            voice_analysis.clarity_score = result.communication_score
            voice_analysis.confidence_score = result.communication_score
            voice_analysis.tone_evaluation = tone_label
            voice_analysis.communication_feedback = "\n\n".join(result.feedback)

        # 6. Update session communication score average
        va_all_query = (
            select(VoiceAnalysis.clarity_score)
            .join(InterviewResponse, VoiceAnalysis.response_id == InterviewResponse.id)
            .where(InterviewResponse.session_id == session_id)
        )
        va_all_res = await db.execute(va_all_query)
        all_comm_scores = [s for s in va_all_res.scalars().all() if s is not None]
        if result.communication_score not in all_comm_scores:
            all_comm_scores.append(result.communication_score)

        if all_comm_scores:
            session.communication_score = round(sum(all_comm_scores) / len(all_comm_scores), 1)

        await db.commit()
        await db.refresh(voice_analysis)

        return result


voice_feedback_service = VoiceFeedbackService()
