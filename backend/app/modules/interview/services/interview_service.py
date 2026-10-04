from datetime import datetime, timezone
from typing import List, Optional, Dict
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.interview.models import (
    InterviewSession,
    InterviewQuestion,
    InterviewResponse,
    InterviewFeedback,
)
from app.modules.interview.schemas import (
    InterviewSessionCreate,
    AnswerAnalysisResult,
    InterviewResultOut,
    QuestionPerformanceOut,
    AggregateVoiceMetricsOut,
    InterviewHistoryItemOut,
    InterviewHistoryPaginationOut,
)
from app.modules.interview.services.question_generator import question_generator
from app.modules.interview.services.answer_analyzer import answer_analyzer
from app.modules.interview.services.llm_client import LLMTimeoutError, LLMClientError
from app.modules.voice.models import VoiceAnalysis


class InterviewService:
    @staticmethod
    async def create_session(
        db: AsyncSession,
        user_id: UUID,
        data: InterviewSessionCreate,
    ) -> InterviewSession:
        role = data.get_role()

        session = InterviewSession(
            user_id=user_id,
            target_role=role,
            interview_type=data.interview_type.value,
            experience_level=data.experience_level.value,
            difficulty=data.difficulty.value,
            answer_mode=data.answer_mode.value,
            question_count=data.question_count,
            target_company=data.target_company,
            status="pending",
            current_question_index=0,
        )

        db.add(session)
        await db.commit()
        await db.refresh(session)
        return session

    @staticmethod
    async def get_user_sessions(
        db: AsyncSession,
        user_id: UUID,
    ) -> List[InterviewSession]:
        result = await db.execute(
            select(InterviewSession)
            .where(InterviewSession.user_id == user_id)
            .order_by(InterviewSession.created_at.desc())
        )
        return list(result.scalars().all())

    @staticmethod
    async def get_session_by_id(
        db: AsyncSession,
        session_id: UUID,
        user_id: UUID,
    ) -> InterviewSession:
        result = await db.execute(
            select(InterviewSession).where(InterviewSession.id == session_id)
        )
        session = result.scalar_one_or_none()

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Interview session with ID {session_id} not found.",
            )

        if session.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this interview session.",
            )

        return session

    @staticmethod
    async def start_session(
        db: AsyncSession,
        session_id: UUID,
        user_id: UUID,
    ) -> InterviewSession:
        session = await InterviewService.get_session_by_id(db, session_id, user_id)

        if session.status == "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot start an already completed interview session.",
            )

        if session.status == "in_progress":
            return session

        session.status = "in_progress"
        await db.commit()
        await db.refresh(session)
        return session

    @staticmethod
    async def complete_session(
        db: AsyncSession,
        session_id: UUID,
        user_id: UUID,
    ) -> InterviewSession:
        session = await InterviewService.get_session_by_id(db, session_id, user_id)

        if session.status == "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Interview session is already completed.",
            )

        session.status = "completed"
        session.completed_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(session)
        return session

    @staticmethod
    async def generate_session_questions(
        db: AsyncSession,
        session_id: UUID,
        user_id: UUID,
    ) -> List[InterviewQuestion]:
        session = await InterviewService.get_session_by_id(db, session_id, user_id)

        # Prevent duplicate question generation
        existing_result = await db.execute(
            select(InterviewQuestion)
            .where(InterviewQuestion.session_id == session_id)
            .order_by(InterviewQuestion.question_order)
        )
        existing_questions = list(existing_result.scalars().all())
        if existing_questions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Questions have already been generated for this session.",
            )

        try:
            generated_list = await question_generator.generate_questions(
                interview_type=session.interview_type,
                target_role=session.target_role,
                experience_level=session.experience_level,
                difficulty=session.difficulty,
                question_count=session.question_count,
                target_company=session.target_company,
            )
        except LLMTimeoutError as exc:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Question generation timed out. Please try again.",
            ) from exc
        except (LLMClientError, ValueError) as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Question generation failed: {str(exc)}",
            ) from exc

        db_questions = [
            InterviewQuestion(
                session_id=session.id,
                question_order=q.question_order,
                category=q.category,
                topic=q.topic,
                question_text=q.question_text,
                expected_points=q.expected_points,
                difficulty=q.difficulty,
            )
            for q in generated_list
        ]

        db.add_all(db_questions)
        session.question_count = len(db_questions)
        await db.commit()

        # Re-fetch with fresh session state
        result = await db.execute(
            select(InterviewQuestion)
            .where(InterviewQuestion.session_id == session_id)
            .order_by(InterviewQuestion.question_order)
        )
        return list(result.scalars().all())

    @staticmethod
    async def submit_answer(
        db: AsyncSession,
        session_id: UUID,
        user_id: UUID,
        question_id: UUID,
        answer_text: str,
        allow_retry: bool = False,
    ) -> tuple[InterviewResponse, bool]:
        if not answer_text or not answer_text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Answer text cannot be empty.",
            )

        session = await InterviewService.get_session_by_id(db, session_id, user_id)

        if session.status == "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot submit answers to a completed session.",
            )

        if session.status == "pending":
            session.status = "in_progress"

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
                detail="Question not found in this interview session.",
            )

        resp_res = await db.execute(
            select(InterviewResponse).where(
                InterviewResponse.session_id == session_id,
                InterviewResponse.question_id == question_id,
            )
        )
        response = resp_res.scalar_one_or_none()

        if response:
            if not allow_retry:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Answer has already been submitted for this question.",
                )
            response.transcribed_text = answer_text.strip()
            is_created = False
        else:
            response = InterviewResponse(
                session_id=session_id,
                question_id=question_id,
                transcribed_text=answer_text.strip(),
            )
            db.add(response)
            is_created = True

        if question.question_order > session.current_question_index:
            session.current_question_index = question.question_order

        await db.commit()
        await db.refresh(response)
        return response, is_created

    @staticmethod
    async def evaluate_response(
        db: AsyncSession,
        session_id: UUID,
        user_id: UUID,
        response_id: Optional[UUID] = None,
        question_id: Optional[UUID] = None,
        answer_text: Optional[str] = None,
    ) -> AnswerAnalysisResult:
        """
        Evaluates a candidate's answer using the AI AnswerAnalyzerService.
        Stores the resulting score, feedback, strengths, and improvements in the InterviewResponse
        model and updates the session's running score.
        """
        session = await InterviewService.get_session_by_id(db, session_id, user_id)

        target_response: Optional[InterviewResponse] = None
        target_question: Optional[InterviewQuestion] = None

        if response_id:
            r_res = await db.execute(
                select(InterviewResponse).where(
                    InterviewResponse.id == response_id,
                    InterviewResponse.session_id == session_id,
                )
            )
            target_response = r_res.scalar_one_or_none()
            if not target_response:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Interview response not found in this session.",
                )
            q_res = await db.execute(
                select(InterviewQuestion).where(InterviewQuestion.id == target_response.question_id)
            )
            target_question = q_res.scalar_one_or_none()

        elif question_id:
            q_res = await db.execute(
                select(InterviewQuestion).where(
                    InterviewQuestion.id == question_id,
                    InterviewQuestion.session_id == session_id,
                )
            )
            target_question = q_res.scalar_one_or_none()
            if not target_question:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Question not found in this interview session.",
                )

            r_res = await db.execute(
                select(InterviewResponse).where(
                    InterviewResponse.question_id == question_id,
                    InterviewResponse.session_id == session_id,
                )
            )
            target_response = r_res.scalar_one_or_none()
            if not target_response:
                if not answer_text or not answer_text.strip():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="No answer has been submitted for this question yet.",
                    )
                target_response = InterviewResponse(
                    session_id=session_id,
                    question_id=question_id,
                    transcribed_text=answer_text.strip(),
                )
                db.add(target_response)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Either response_id or question_id must be provided for evaluation.",
            )

        text_to_analyze = (answer_text or (target_response.transcribed_text if target_response else "") or "").strip()
        if not text_to_analyze:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Answer text cannot be empty for analysis.",
            )

        question_text = target_question.question_text if target_question else "Interview Question"
        category = target_question.category if target_question else "Technical"
        topic = target_question.topic if target_question else None
        expected_points = target_question.expected_points if target_question else []
        difficulty = target_question.difficulty if target_question else session.difficulty

        try:
            analysis = await answer_analyzer.analyze_answer(
                question_text=question_text,
                answer_text=text_to_analyze,
                category=category,
                topic=topic,
                expected_points=expected_points,
                difficulty=difficulty,
                target_role=session.target_role,
            )
        except LLMTimeoutError as exc:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="AI answer evaluation timed out. Please try again.",
            ) from exc
        except LLMClientError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"AI service unavailable: {str(exc)}",
            ) from exc
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"AI answer evaluation failed: {str(exc)}",
            ) from exc

        # Store analysis appropriately in InterviewResponse model
        target_response.score = analysis.score
        target_response.feedback_text = (
            "\n".join(analysis.feedback) if analysis.feedback else f"Score: {analysis.score}"
        )
        target_response.key_strengths = analysis.strengths
        target_response.missing_concepts = (
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
        if target_response.score is not None and target_response.score not in all_scores:
            all_scores.append(target_response.score)

        if all_scores:
            avg_score = round(sum(all_scores) / len(all_scores), 1)
            session.overall_score = avg_score
            session.technical_score = avg_score

        await db.commit()
        await db.refresh(target_response)
        return analysis

    @staticmethod
    async def get_interview_result(
        db: AsyncSession,
        session_id: UUID,
        user_id: UUID,
    ) -> InterviewResultOut:
        # 1. Verify session exists and belongs to current user
        session_res = await db.execute(
            select(InterviewSession).where(InterviewSession.id == session_id)
        )
        session = session_res.scalar_one_or_none()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interview session not found.",
            )

        if session.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to view results for this interview session.",
            )

        # 2. Load questions
        q_res = await db.execute(
            select(InterviewQuestion)
            .where(InterviewQuestion.session_id == session_id)
            .order_by(InterviewQuestion.question_order)
        )
        questions = q_res.scalars().all()

        # 3. Load responses
        r_res = await db.execute(
            select(InterviewResponse)
            .where(InterviewResponse.session_id == session_id)
        )
        responses = r_res.scalars().all()
        responses_by_q_id = {r.question_id: r for r in responses}
        response_ids = [r.id for r in responses]

        # 4. Load voice analyses for responses
        voice_analyses_by_resp_id: Dict[UUID, VoiceAnalysis] = {}
        if response_ids:
            va_res = await db.execute(
                select(VoiceAnalysis).where(VoiceAnalysis.response_id.in_(response_ids))
            )
            for va in va_res.scalars().all():
                voice_analyses_by_resp_id[va.response_id] = va

        # 5. Calculate Technical Score
        scored_responses = [r.score for r in responses if r.score is not None]
        if scored_responses:
            technical_score = round(sum(scored_responses) / len(scored_responses), 1)
        elif session.technical_score is not None:
            technical_score = session.technical_score
        else:
            technical_score = 0.0

        # 6. Aggregate Voice Metrics & Calculate Communication Score
        has_voice = False
        speaking_rates: List[float] = []
        clarity_scores: List[float] = []
        total_fillers = 0
        combined_fillers: Dict[str, int] = {}
        total_pauses = 0
        total_pause_duration = 0.0
        tone_evaluations: List[str] = []
        comm_feedbacks: List[str] = []

        for va in voice_analyses_by_resp_id.values():
            has_voice = True
            if va.speaking_rate_wpm and va.speaking_rate_wpm > 0:
                speaking_rates.append(va.speaking_rate_wpm)
            if va.clarity_score is not None:
                clarity_scores.append(va.clarity_score)
            if va.filler_word_count:
                total_fillers += va.filler_word_count
            if va.filler_words_detected:
                for word, count in va.filler_words_detected.items():
                    combined_fillers[word] = combined_fillers.get(word, 0) + count
            if va.pause_count:
                total_pauses += va.pause_count
            if va.total_pause_duration_seconds:
                total_pause_duration += va.total_pause_duration_seconds
            if va.tone_evaluation:
                tone_evaluations.append(va.tone_evaluation)
            if va.communication_feedback:
                for line in va.communication_feedback.split("\n\n"):
                    trimmed = line.strip()
                    if trimmed and trimmed not in comm_feedbacks:
                        comm_feedbacks.append(trimmed)

        avg_speaking_rate = round(sum(speaking_rates) / len(speaking_rates), 1) if speaking_rates else 0.0
        if clarity_scores:
            communication_score = round(sum(clarity_scores) / len(clarity_scores), 1)
        elif session.communication_score is not None:
            communication_score = session.communication_score
        else:
            communication_score = 0.0

        dominant_tone = tone_evaluations[0] if tone_evaluations else None

        # 7. Calculate Overall Interview Score (Backend calculation)
        if has_voice and communication_score > 0:
            overall_score = round((technical_score * 0.65) + (communication_score * 0.35), 1)
        else:
            overall_score = technical_score

        # Update and persist session scores
        session.overall_score = overall_score
        session.technical_score = technical_score
        session.communication_score = communication_score

        # 8. Build Question Performance List
        question_performance: List[QuestionPerformanceOut] = []
        all_strengths: List[str] = []
        all_weaknesses: List[str] = []
        all_answer_feedbacks: List[str] = []

        for q in questions:
            resp = responses_by_q_id.get(q.id)
            va = voice_analyses_by_resp_id.get(resp.id) if resp else None

            q_strengths = resp.key_strengths if (resp and resp.key_strengths) else []
            q_weaknesses = resp.missing_concepts if (resp and resp.missing_concepts) else []

            for s in q_strengths:
                if s not in all_strengths:
                    all_strengths.append(s)
            for w in q_weaknesses:
                if w not in all_weaknesses:
                    all_weaknesses.append(w)

            if resp and resp.feedback_text:
                for line in resp.feedback_text.split("\n"):
                    line_clean = line.strip()
                    if line_clean and line_clean not in all_answer_feedbacks:
                        all_answer_feedbacks.append(line_clean)

            question_performance.append(
                QuestionPerformanceOut(
                    question_id=q.id,
                    question_order=q.question_order,
                    question_text=q.question_text,
                    category=q.category,
                    difficulty=q.difficulty,
                    topic=q.topic,
                    candidate_answer=resp.transcribed_text if resp else None,
                    score=resp.score if resp else None,
                    feedback=resp.feedback_text if resp else None,
                    strengths=q_strengths,
                    weaknesses=q_weaknesses,
                    audio_duration_seconds=resp.audio_duration_seconds if resp else None,
                    speaking_rate_wpm=va.speaking_rate_wpm if va else None,
                    filler_word_count=va.filler_word_count if va else None,
                    clarity_score=va.clarity_score if va else None,
                )
            )

        # Fallback default strengths & weaknesses if none were recorded
        if not all_strengths:
            all_strengths = [
                f"Completed {session.interview_type} practice session for {session.target_role}",
                "Structured progression across technical questions",
            ]
        if not all_weaknesses:
            all_weaknesses = [
                "Continue detailing architectural trade-offs and complexity analysis",
                "Elaborate on production failure modes and recovery strategies",
            ]

        # 9. Synthesize Actionable Recommendations
        recommendations: List[str] = []
        if technical_score >= 80.0:
            recommendations.append("Technical Depth: Strong conceptual and practical grounding. Continue practicing complex system edge-cases and distributed failure recovery.")
        elif technical_score >= 60.0:
            recommendations.append("Technical Articulation: Review core trade-offs (e.g. latency vs. throughput, consistency vs. availability) to sharpen technical depth.")
        else:
            recommendations.append("Technical Fundamentals: Dedicate focused prep to the fundamental data structures, algorithms, and core domain frameworks for your target role.")

        if has_voice:
            if avg_speaking_rate > 160.0:
                recommendations.append(f"Pacing: Delivery averaged {avg_speaking_rate} WPM (ideal: 120-160 WPM). Consciously insert pauses between major points to aid interviewer comprehension.")
            elif avg_speaking_rate < 115.0 and avg_speaking_rate > 0.0:
                recommendations.append(f"Pacing: Delivery averaged {avg_speaking_rate} WPM. Practice formulating concise statements to cover more ground in timed interviews.")
            else:
                recommendations.append(f"Pacing: Average rate of {avg_speaking_rate} WPM is in the optimal interview cadence range.")

            if total_fillers > 4:
                top_fillers_str = ", ".join(f"'{k}' ({v}x)" for k, v in sorted(combined_fillers.items(), key=lambda x: -x[1])[:3])
                recommendations.append(f"Verbal Economy: {total_fillers} filler words detected ({top_fillers_str}). Practice replacing fillers with deliberate silent pauses while organizing thoughts.")
            else:
                recommendations.append("Verbal Economy: Controlled delivery with minimal verbal crutches.")

        recommendations.append(f"Practice Next: Schedule another {session.interview_type} mock interview to solidify improvements before real hiring loops.")

        # 10. Summary text
        summary = (
            f"Overall performance for {session.target_role} ({session.interview_type}, {session.difficulty}): "
            f"Blended Score {overall_score}/100 with Technical Score {technical_score}/100"
            + (f" and Communication Score {communication_score}/100." if has_voice else ".")
        )

        # 11. Interview Duration Calculation
        if session.completed_at and session.created_at:
            duration_sec = max(0.0, (session.completed_at - session.created_at).total_seconds())
        else:
            total_audio_sec = sum(r.audio_duration_seconds or 0.0 for r in responses)
            duration_sec = total_audio_sec if total_audio_sec > 0 else 60.0 * len(responses)

        duration_sec = round(duration_sec, 1)
        mins = int(duration_sec // 60)
        secs = int(duration_sec % 60)
        formatted_duration = f"{mins}m {secs}s" if mins > 0 else f"{secs}s"

        # 12. Create or Update InterviewFeedback record
        fb_res = await db.execute(
            select(InterviewFeedback).where(InterviewFeedback.session_id == session_id)
        )
        feedback_obj = fb_res.scalar_one_or_none()
        if not feedback_obj:
            feedback_obj = InterviewFeedback(
                session_id=session_id,
                overall_score=overall_score,
                technical_score=technical_score,
                communication_score=communication_score,
                summary=summary,
                key_strengths=all_strengths[:5],
                areas_for_improvement=all_weaknesses[:5],
                actionable_recommendations=recommendations,
            )
            db.add(feedback_obj)
        else:
            feedback_obj.overall_score = overall_score
            feedback_obj.technical_score = technical_score
            feedback_obj.communication_score = communication_score
            feedback_obj.summary = summary
            feedback_obj.key_strengths = all_strengths[:5]
            feedback_obj.areas_for_improvement = all_weaknesses[:5]
            feedback_obj.actionable_recommendations = recommendations

        await db.commit()
        await db.refresh(session)

        # 13. Assemble AggregateVoiceMetricsOut
        voice_metrics_out = AggregateVoiceMetricsOut(
            has_voice_data=has_voice,
            average_speaking_rate_wpm=avg_speaking_rate,
            total_filler_word_count=total_fillers,
            filler_words_detected=combined_fillers,
            average_clarity_score=communication_score,
            total_pause_count=total_pauses,
            total_pause_duration_seconds=round(total_pause_duration, 1),
            tone_evaluation=dominant_tone,
            communication_feedback=comm_feedbacks,
        )

        return InterviewResultOut(
            session_id=session.id,
            target_role=session.target_role,
            interview_type=session.interview_type,
            experience_level=session.experience_level,
            difficulty=session.difficulty,
            status=session.status,
            interview_score=overall_score,
            technical_score=technical_score,
            communication_score=communication_score,
            total_questions=len(questions),
            answered_questions=len(responses),
            interview_duration_seconds=duration_sec,
            formatted_duration=formatted_duration,
            summary=summary,
            strengths=all_strengths,
            weaknesses=all_weaknesses,
            answer_feedback=all_answer_feedbacks,
            recommendations=recommendations,
            voice_metrics=voice_metrics_out,
            question_performance=question_performance,
            created_at=session.created_at,
            completed_at=session.completed_at,
        )

    @staticmethod
    async def get_interview_history(
        db: AsyncSession,
        user_id: UUID,
        skip: int = 0,
        limit: int = 10,
    ) -> InterviewHistoryPaginationOut:
        # 1. Total count for the user
        count_stmt = select(func.count(InterviewSession.id)).where(InterviewSession.user_id == user_id)
        total_res = await db.execute(count_stmt)
        total = total_res.scalar() or 0

        # 2. Query paginated sessions ordered by creation date descending
        stmt = (
            select(InterviewSession)
            .where(InterviewSession.user_id == user_id)
            .order_by(InterviewSession.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        sessions_res = await db.execute(stmt)
        sessions = list(sessions_res.scalars().all())

        if not sessions:
            page_num = (skip // limit) + 1 if limit > 0 else 1
            total_pgs = (total + limit - 1) // limit if total > 0 and limit > 0 else 1
            return InterviewHistoryPaginationOut(
                items=[],
                total=total,
                skip=skip,
                limit=limit,
                page=page_num,
                total_pages=total_pgs,
            )

        # 3. Batch query responses for non-completed sessions to calculate elapsed/audio durations if needed
        uncompleted_ids = [s.id for s in sessions if not s.completed_at]
        durations_by_session: Dict[UUID, float] = {}
        if uncompleted_ids:
            resp_stmt = (
                select(
                    InterviewResponse.session_id,
                    func.sum(InterviewResponse.audio_duration_seconds),
                    func.count(InterviewResponse.id),
                )
                .where(InterviewResponse.session_id.in_(uncompleted_ids))
                .group_by(InterviewResponse.session_id)
            )
            resp_res = await db.execute(resp_stmt)
            for sess_id, sum_dur, count_resp in resp_res.all():
                if sum_dur and float(sum_dur) > 0.0:
                    durations_by_session[sess_id] = float(sum_dur)
                elif count_resp:
                    durations_by_session[sess_id] = float(count_resp * 60.0)

        # 4. Fallback for missing overall_score if any session is completed but overall_score is None:
        missing_score_ids = [s.id for s in sessions if s.overall_score is None]
        feedbacks_by_session: Dict[UUID, InterviewFeedback] = {}
        if missing_score_ids:
            fb_stmt = select(InterviewFeedback).where(InterviewFeedback.session_id.in_(missing_score_ids))
            fb_res = await db.execute(fb_stmt)
            for fb in fb_res.scalars().all():
                feedbacks_by_session[fb.session_id] = fb

        # 5. Build items
        items: List[InterviewHistoryItemOut] = []
        for s in sessions:
            if s.completed_at and s.created_at:
                dur_sec = max(0.0, (s.completed_at - s.created_at).total_seconds())
            else:
                dur_sec = durations_by_session.get(s.id, 0.0)

            dur_sec = round(dur_sec, 1)
            mins = int(dur_sec // 60)
            secs = int(dur_sec % 60)
            formatted_dur = f"{mins}m {secs}s" if mins > 0 else f"{secs}s"

            # Determine scores
            ov_score = s.overall_score
            tech_score = s.technical_score
            comm_score = s.communication_score
            if ov_score is None and s.id in feedbacks_by_session:
                fb = feedbacks_by_session[s.id]
                ov_score = fb.overall_score
                tech_score = fb.technical_score
                comm_score = fb.communication_score

            items.append(
                InterviewHistoryItemOut(
                    id=s.id,
                    date=s.created_at,
                    created_at=s.created_at,
                    completed_at=s.completed_at,
                    target_role=s.target_role,
                    interview_type=s.interview_type,
                    experience_level=s.experience_level,
                    difficulty=s.difficulty,
                    status=s.status,
                    number_of_questions=s.question_count,
                    question_count=s.question_count,
                    overall_score=ov_score,
                    technical_score=tech_score,
                    communication_score=comm_score,
                    duration=formatted_dur,
                    formatted_duration=formatted_dur,
                    duration_seconds=dur_sec,
                )
            )

        page_num = (skip // limit) + 1 if limit > 0 else 1
        total_pgs = (total + limit - 1) // limit if total > 0 and limit > 0 else 1

        return InterviewHistoryPaginationOut(
            items=items,
            total=total,
            skip=skip,
            limit=limit,
            page=page_num,
            total_pages=total_pgs,
        )


interview_service = InterviewService()



