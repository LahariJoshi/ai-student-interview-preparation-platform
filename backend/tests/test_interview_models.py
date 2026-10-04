import pytest
import uuid
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.modules.interview.models import (
    InterviewSession,
    InterviewQuestion,
    InterviewResponse,
    InterviewFeedback,
)
from app.modules.voice.models import VoiceAnalysis


@pytest.mark.asyncio
async def test_create_interview_session_and_questions(db_session: AsyncSession):
    # 1. Create a user
    user = User(
        email="test_student@example.com",
        password_hash="fakehash123",
        full_name="Alex Rivera",
        role="student",
    )
    db_session.add(user)
    await db_session.flush()

    # 2. Create an InterviewSession
    session = InterviewSession(
        user_id=user.id,
        role="Backend Engineer",
        interview_type="technical",
        difficulty="medium",
        target_company="Stripe",
        total_questions=3,
        status="in_progress",
    )
    db_session.add(session)
    await db_session.flush()

    assert session.id is not None
    assert isinstance(session.id, uuid.UUID)
    assert session.role == "Backend Engineer"
    assert session.current_question_index == 0
    assert session.total_questions == 3
    assert session.status == "in_progress"

    # 3. Add InterviewQuestions
    q1 = InterviewQuestion(
        session_id=session.id,
        question_order=1,
        category="technical",
        topic="Database Indexing",
        question_text="Explain the difference between B-tree and Hash indexes.",
        expected_points=["B-tree supports range queries", "Hash index is O(1) equality only"],
        difficulty="medium",
    )
    q2 = InterviewQuestion(
        session_id=session.id,
        question_order=2,
        category="technical",
        topic="Caching",
        question_text="How would you design a cache invalidation strategy?",
        expected_points=["Write-through", "Cache-aside", "TTL expiration"],
        difficulty="medium",
    )
    db_session.add_all([q1, q2])
    await db_session.flush()

    # Query back session with questions
    result = await db_session.execute(
        select(InterviewSession).where(InterviewSession.id == session.id)
    )
    loaded_session = result.scalar_one()
    assert len(loaded_session.questions) == 2
    assert loaded_session.questions[0].topic == "Database Indexing"


@pytest.mark.asyncio
async def test_interview_response_and_voice_analysis(db_session: AsyncSession):
    # 1. Create user and session
    user = User(
        email="voice_test@example.com",
        password_hash="fakehash456",
        full_name="Samantha Ray",
    )
    db_session.add(user)
    await db_session.flush()

    session = InterviewSession(
        user_id=user.id,
        role="Frontend Developer",
        interview_type="behavioral",
    )
    db_session.add(session)
    await db_session.flush()

    question = InterviewQuestion(
        session_id=session.id,
        question_order=1,
        category="behavioral",
        topic="Teamwork",
        question_text="Tell me about a time you resolved a conflict with a teammate.",
        expected_points=["STAR format", "Empathy", "Action taken"],
    )
    db_session.add(question)
    await db_session.flush()

    # 2. Add an interview response
    response = InterviewResponse(
        session_id=session.id,
        question_id=question.id,
        transcribed_text="In my previous project, we had differing opinions on state management. I organized a meeting and we chose Zustand.",
        audio_file_path="/uploads/audio/resp_123.wav",
        audio_duration_seconds=45.2,
        score=85.0,
        feedback_text="Solid structured answer with clear resolution.",
        key_strengths=["Clear communication", "Structured approach"],
        missing_concepts=["Measurable impact metrics"],
    )
    db_session.add(response)
    await db_session.flush()

    assert response.id is not None
    assert response.score == 85.0

    # 3. Add 1:1 VoiceAnalysis
    voice_analysis = VoiceAnalysis(
        response_id=response.id,
        speaking_rate_wpm=142.5,
        filler_word_count=2,
        filler_words_detected={"um": 1, "like": 1},
        pause_count=3,
        total_pause_duration_seconds=2.4,
        clarity_score=88.0,
        confidence_score=90.0,
        tone_evaluation="Confident and composed",
        communication_feedback="Excellent pace and clear articulation with minimal filler words.",
    )
    db_session.add(voice_analysis)
    await db_session.flush()

    assert voice_analysis.id is not None
    assert voice_analysis.speaking_rate_wpm == 142.5
    assert voice_analysis.filler_word_count == 2
    assert voice_analysis.response.transcribed_text.startswith("In my previous project")


@pytest.mark.asyncio
async def test_interview_feedback_and_cascade_delete(db_session: AsyncSession):
    # 1. Setup session with full tree
    user = User(
        email="cascade_test@example.com",
        password_hash="fakehash789",
        full_name="David Chen",
    )
    db_session.add(user)
    await db_session.flush()

    session = InterviewSession(
        user_id=user.id,
        role="Data Engineer",
    )
    db_session.add(session)
    await db_session.flush()

    q = InterviewQuestion(
        session_id=session.id,
        question_order=1,
        question_text="Explain MapReduce architecture.",
    )
    db_session.add(q)
    await db_session.flush()

    resp = InterviewResponse(
        session_id=session.id,
        question_id=q.id,
        transcribed_text="MapReduce processes large data sets in parallel.",
    )
    db_session.add(resp)
    await db_session.flush()

    va = VoiceAnalysis(
        response_id=resp.id,
        speaking_rate_wpm=130.0,
        communication_feedback="Good pace.",
    )
    db_session.add(va)
    await db_session.flush()

    fb = InterviewFeedback(
        session_id=session.id,
        overall_score=82.0,
        technical_score=80.0,
        communication_score=84.0,
        summary="Strong candidate overall.",
        key_strengths=["Clear technical explanations"],
        areas_for_improvement=["Elaborate on edge cases"],
        actionable_recommendations=["Review distributed storage primitives"],
    )
    db_session.add(fb)
    await db_session.flush()

    # Verify feedback was stored
    res_fb = await db_session.execute(
        select(InterviewFeedback).where(InterviewFeedback.session_id == session.id)
    )
    assert res_fb.scalar_one().overall_score == 82.0

    # Delete session and verify cascade deletes questions, responses, feedback, and voice analysis
    await db_session.delete(session)
    await db_session.flush()

    res_q = await db_session.execute(select(InterviewQuestion).where(InterviewQuestion.session_id == session.id))
    assert res_q.scalars().all() == []

    res_resp = await db_session.execute(select(InterviewResponse).where(InterviewResponse.session_id == session.id))
    assert res_resp.scalars().all() == []

    res_fb = await db_session.execute(select(InterviewFeedback).where(InterviewFeedback.session_id == session.id))
    assert res_fb.scalars().all() == []

    res_va = await db_session.execute(select(VoiceAnalysis).where(VoiceAnalysis.id == va.id))
    assert res_va.scalars().all() == []
