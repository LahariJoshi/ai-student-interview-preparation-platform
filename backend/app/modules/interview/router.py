"""Interview API Router.

Endpoints:
- POST /sessions: Configure and initiate mock interview
- GET /sessions/{session_id}: Retrieve session details
- GET /sessions/{session_id}/current-question: Fetch the current active question
- POST /sessions/{session_id}/answers: Submit answer for current question and evaluate
- POST /sessions/{session_id}/audio-upload: Upload audio file and compute delivery metrics
- POST /sessions/{session_id}/end: Finalize interview session and aggregate results
- GET /sessions/{session_id}/results: Retrieve comprehensive scores, rubric, recommendations
- GET /history: Retrieve student's past interviews and progress
"""

import os
import uuid
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_user
from app.db.models.user import User
from app.db.models.resume import Resume
from app.db.models.interview import InterviewSession, InterviewQuestion, InterviewAnswer
from app.modules.interview.schemas import (
    InterviewSessionCreate,
    InterviewSessionOut,
    InterviewSessionListItem,
    InterviewHistoryResponse,
    InterviewResultsResponse,
    QuestionOut,
    AnswerSubmitRequest,
    AnswerOut,
    AudioUploadResponse,
)
from app.modules.interview.services.question_service import generate_interview_questions
from app.modules.interview.services.evaluation_service import (
    evaluate_single_answer,
    aggregate_session_feedback,
)
from app.modules.interview.services.voice_service import analyze_speech_delivery

router = APIRouter(prefix="/interviews", tags=["AI Mock Interview"])


@router.post("/sessions", response_model=InterviewSessionOut, status_code=status.HTTP_201_CREATED)
async def create_interview_session(
    data: InterviewSessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Validate configuration and start an interactive mock interview session."""
    # 1. Validate inputs
    valid_types = ["technical", "hr", "behavioral", "mixed"]
    if data.interview_type.lower() not in valid_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid interview type. Must be one of: {', '.join(valid_types)}",
        )

    valid_levels = ["Beginner", "Intermediate", "Advanced"]
    if data.experience_level not in valid_levels:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid experience level. Must be one of: {', '.join(valid_levels)}",
        )

    # 2. Check resume if linked
    resume_skills: List[str] = []
    resume_projects: List[str] = []
    if data.resume_id:
        res_stmt = select(Resume).where(
            Resume.id == data.resume_id,
            Resume.user_id == current_user.id,
        ).options(selectinload(Resume.analysis))
        res_res = await db.execute(res_stmt)
        resume = res_res.scalar_one_or_none()
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Selected resume not found or does not belong to you.",
            )
        if resume.analysis and resume.analysis.skills:
            if isinstance(resume.analysis.skills, dict):
                for skill_list in resume.analysis.skills.values():
                    if isinstance(skill_list, list):
                        resume_skills.extend(skill_list)
            elif isinstance(resume.analysis.skills, list):
                resume_skills = resume.analysis.skills

    # Determine question count based on duration (1 question per ~3-4 mins, minimum 3, maximum 10)
    total_q = max(3, min(10, data.duration_minutes // 3))

    # 3. Generate tailored questions
    questions_data = await generate_interview_questions(
        role=data.target_role,
        interview_type=data.interview_type.lower(),
        experience_level=data.experience_level,
        skills=data.custom_skills,
        resume_skills=resume_skills,
        resume_projects=resume_projects,
        total_questions=total_q,
    )

    # 4. Create interview session
    session = InterviewSession(
        user_id=current_user.id,
        resume_id=data.resume_id,
        interview_type=data.interview_type.lower(),
        target_role=data.target_role,
        experience_level=data.experience_level,
        duration_minutes=data.duration_minutes,
        custom_skills=data.custom_skills,
        status="in_progress",
        total_questions=len(questions_data),
        current_question_index=0,
    )
    db.add(session)
    await db.flush()

    # 5. Add questions
    created_questions = []
    for idx, q in enumerate(questions_data):
        iq = InterviewQuestion(
            session_id=session.id,
            order_index=idx,
            question_text=q["question_text"],
            category=q["category"],
            difficulty=q["difficulty"],
            topic_or_skill=q.get("topic_or_skill"),
            expected_key_points=q["expected_key_points"],
            reference_answer=q["reference_answer"],
            evaluation_rubric=q["evaluation_rubric"],
        )
        db.add(iq)
        created_questions.append(iq)

    await db.commit()
    await db.refresh(session)

    # Reload with questions
    session_stmt = (
        select(InterviewSession)
        .where(InterviewSession.id == session.id)
        .options(selectinload(InterviewSession.questions))
    )
    res = await db.execute(session_stmt)
    return res.scalar_one()


@router.get("/sessions/{session_id}", response_model=InterviewSessionOut)
async def get_interview_session(
    session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve details for an interview session."""
    stmt = (
        select(InterviewSession)
        .where(InterviewSession.id == session_id, InterviewSession.user_id == current_user.id)
        .options(selectinload(InterviewSession.questions))
    )
    res = await db.execute(stmt)
    session = res.scalar_one_or_none()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found or unauthorized.",
        )
    return session


@router.get("/sessions/{session_id}/current-question", response_model=QuestionOut)
async def get_current_question(
    session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve the current active question for an in-progress session."""
    stmt = (
        select(InterviewSession)
        .where(InterviewSession.id == session_id, InterviewSession.user_id == current_user.id)
        .options(selectinload(InterviewSession.questions))
    )
    res = await db.execute(stmt)
    session = res.scalar_one_or_none()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found or unauthorized.",
        )

    if session.status != "in_progress":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Interview session is currently '{session.status}'.",
        )

    if session.current_question_index >= len(session.questions):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="All questions for this session have been completed.",
        )

    current_q = session.questions[session.current_question_index]
    return current_q


@router.post("/sessions/{session_id}/answers", response_model=AnswerOut)
async def submit_answer(
    session_id: uuid.UUID,
    data: AnswerSubmitRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Submit a student's answer for the active question, evaluate it, and advance question index."""
    # 1. Fetch session
    sess_stmt = (
        select(InterviewSession)
        .where(InterviewSession.id == session_id, InterviewSession.user_id == current_user.id)
        .options(selectinload(InterviewSession.questions))
    )
    res = await db.execute(sess_stmt)
    session = res.scalar_one_or_none()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found or unauthorized.",
        )

    if session.status != "in_progress":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot submit answer to a session with status '{session.status}'.",
        )

    # 2. Fetch question
    q_stmt = select(InterviewQuestion).where(
        InterviewQuestion.id == data.question_id,
        InterviewQuestion.session_id == session.id,
    )
    q_res = await db.execute(q_stmt)
    question = q_res.scalar_one_or_none()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found in this interview session.",
        )

    # 3. Check for duplicate answer submission
    existing_stmt = select(InterviewAnswer).where(InterviewAnswer.question_id == question.id)
    existing_res = await db.execute(existing_stmt)
    if existing_res.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An answer has already been submitted for this question.",
        )

    # 4. Evaluate answer
    eval_result = await evaluate_single_answer(
        question=question,
        answer_text=data.answer_text,
    )

    # 5. Persist answer
    answer = InterviewAnswer(
        session_id=session.id,
        question_id=question.id,
        answer_text=data.answer_text,
        is_voice_response=data.is_voice_response,
        duration_seconds=data.duration_seconds,
        delivery_metrics=data.delivery_metrics or {},
        score=eval_result.get("score"),
        relevance_score=eval_result.get("relevance_score"),
        technical_accuracy_score=eval_result.get("technical_accuracy_score"),
        completeness_score=eval_result.get("completeness_score"),
        clarity_score=eval_result.get("clarity_score"),
        detailed_feedback=eval_result.get("detailed_feedback"),
        improvement_tips=eval_result.get("improvement_tips", []),
        concepts_to_revise=eval_result.get("concepts_to_revise", []),
        evaluated_at=datetime.now(timezone.utc),
    )
    db.add(answer)

    # Advance current question index
    session.current_question_index += 1
    if session.current_question_index >= session.total_questions:
        session.status = "completed"
        session.ended_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(answer)
    return answer


@router.post("/sessions/{session_id}/audio-upload", response_model=AudioUploadResponse)
async def upload_audio_answer(
    session_id: uuid.UUID,
    audio_file: UploadFile = File(...),
    duration_seconds: float = Form(default=0.0),
    transcription_text: Optional[str] = Form(default=None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Receive an audio recording, validate size/format, and compute delivery metrics."""
    # Verify session ownership
    sess_stmt = select(InterviewSession).where(
        InterviewSession.id == session_id,
        InterviewSession.user_id == current_user.id,
    )
    res = await db.execute(sess_stmt)
    session = res.scalar_one_or_none()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found or unauthorized.",
        )

    # Validate file size (max configured MB)
    content = await audio_file.read()
    max_bytes = settings.MAX_AUDIO_SIZE_MB * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Audio file exceeds maximum size limit of {settings.MAX_AUDIO_SIZE_MB}MB.",
        )

    # Save audio safely
    audio_dir = settings.INTERVIEW_AUDIO_DIR
    os.makedirs(audio_dir, exist_ok=True)
    filename = f"{session.id}_{uuid.uuid4().hex[:8]}_{audio_file.filename}"
    filepath = os.path.join(audio_dir, filename)
    with open(filepath, "wb") as f:
        f.write(content)

    # Transcribe text fallback or passed from Web Speech API
    transcript = transcription_text.strip() if transcription_text else "Voice answer recorded."

    # Compute delivery metrics
    metrics = analyze_speech_delivery(
        transcript=transcript,
        duration_seconds=duration_seconds,
    )

    return AudioUploadResponse(
        transcript=transcript,
        duration_seconds=duration_seconds,
        delivery_metrics=metrics,
    )


@router.post("/sessions/{session_id}/end", response_model=InterviewSessionOut)
async def end_interview_session(
    session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """End the mock interview and compute overall results & personalized recommendations."""
    sess_stmt = (
        select(InterviewSession)
        .where(InterviewSession.id == session_id, InterviewSession.user_id == current_user.id)
        .options(
            selectinload(InterviewSession.questions),
            selectinload(InterviewSession.answers).selectinload(InterviewAnswer.question),
        )
    )
    res = await db.execute(sess_stmt)
    session = res.scalar_one_or_none()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found or unauthorized.",
        )

    session.status = "completed"
    session.ended_at = datetime.now(timezone.utc)

    # Compute aggregate feedback
    feedback = aggregate_session_feedback(
        session=session,
        questions=session.questions,
        answers=session.answers,
    )

    session.overall_score = feedback["overall_score"]
    session.technical_score = feedback["technical_score"]
    session.communication_score = feedback["communication_score"]
    session.strengths = feedback["strengths"]
    session.weaknesses = feedback["weaknesses"]
    session.recommendations = feedback["recommendations"]

    await db.commit()
    await db.refresh(session)
    return session


@router.get("/sessions/{session_id}/results", response_model=InterviewResultsResponse)
async def get_interview_results(
    session_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve full evaluation breakdown, individual answers, and recommendations."""
    sess_stmt = (
        select(InterviewSession)
        .where(InterviewSession.id == session_id, InterviewSession.user_id == current_user.id)
        .options(
            selectinload(InterviewSession.questions),
            selectinload(InterviewSession.answers).selectinload(InterviewAnswer.question),
        )
    )
    res = await db.execute(sess_stmt)
    session = res.scalar_one_or_none()
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found or unauthorized.",
        )

    # If completed without aggregate scores, compute now
    if session.overall_score is None:
        feedback = aggregate_session_feedback(
            session=session,
            questions=session.questions,
            answers=session.answers,
        )
        session.overall_score = feedback["overall_score"]
        session.technical_score = feedback["technical_score"]
        session.communication_score = feedback["communication_score"]
        session.strengths = feedback["strengths"]
        session.weaknesses = feedback["weaknesses"]
        session.recommendations = feedback["recommendations"]
        await db.commit()
        await db.refresh(session)

    # Map answers in order
    return InterviewResultsResponse(
        session_id=session.id,
        interview_type=session.interview_type,
        target_role=session.target_role,
        experience_level=session.experience_level,
        status=session.status,
        overall_score=session.overall_score or 0.0,
        technical_score=session.technical_score or 0.0,
        communication_score=session.communication_score or 0.0,
        strengths=session.strengths or [],
        weaknesses=session.weaknesses or [],
        recommendations=session.recommendations or [],
        started_at=session.started_at,
        ended_at=session.ended_at,
        total_questions=session.total_questions,
        questions=session.questions,
        answers=session.answers,
    )


@router.get("/history", response_model=InterviewHistoryResponse)
async def get_interview_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Retrieve chronological history of the student's mock interviews."""
    stmt = (
        select(InterviewSession)
        .where(InterviewSession.user_id == current_user.id)
        .order_by(desc(InterviewSession.started_at))
    )
    res = await db.execute(stmt)
    sessions = res.scalars().all()

    completed = [s for s in sessions if s.status == "completed" and s.overall_score is not None]
    avg_score = (
        round(sum(s.overall_score for s in completed) / len(completed), 1)
        if completed
        else 0.0
    )

    return InterviewHistoryResponse(
        total_interviews=len(sessions),
        completed_interviews=len(completed),
        average_score=avg_score,
        sessions=sessions,
    )
