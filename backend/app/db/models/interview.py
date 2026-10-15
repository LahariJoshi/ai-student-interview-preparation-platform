import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional, List, Dict, Any

from sqlalchemy import String, DateTime, UUID, ForeignKey, Text, Boolean, Integer, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.user import User
    from app.db.models.resume import Resume


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    resume_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("resumes.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    interview_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="mixed",  # technical, hr, behavioral, mixed
    )

    target_role: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        default="Software Developer",
    )

    experience_level: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Beginner",  # Beginner, Intermediate, Advanced
    )

    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=15,
    )

    custom_skills: Mapped[List[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="in_progress",  # in_progress, completed, abandoned
        index=True,
    )

    total_questions: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=5,
    )

    current_question_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    overall_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    technical_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    communication_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    strengths: Mapped[Optional[List[str]]] = mapped_column(
        JSON,
        nullable=True,
        default=list,
    )

    weaknesses: Mapped[Optional[List[str]]] = mapped_column(
        JSON,
        nullable=True,
        default=list,
    )

    recommendations: Mapped[Optional[List[Dict[str, Any]]]] = mapped_column(
        JSON,
        nullable=True,
        default=list,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    ended_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="interview_sessions")
    resume: Mapped[Optional["Resume"]] = relationship("Resume")
    questions: Mapped[List["InterviewQuestion"]] = relationship(
        "InterviewQuestion",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="InterviewQuestion.order_index",
    )
    answers: Mapped[List["InterviewAnswer"]] = relationship(
        "InterviewAnswer",
        back_populates="session",
        cascade="all, delete-orphan",
    )


class InterviewQuestion(Base):
    __tablename__ = "interview_questions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("interview_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    order_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    question_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="technical",  # technical, behavioral, hr, project_based
    )

    difficulty: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="Beginner",
    )

    topic_or_skill: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    expected_key_points: Mapped[List[str]] = mapped_column(
        JSON,
        nullable=False,
        default=list,
    )

    reference_answer: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    evaluation_rubric: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    session: Mapped["InterviewSession"] = relationship("InterviewSession", back_populates="questions")
    answer: Mapped[Optional["InterviewAnswer"]] = relationship(
        "InterviewAnswer",
        back_populates="question",
        uselist=False,
        cascade="all, delete-orphan",
    )


class InterviewAnswer(Base):
    __tablename__ = "interview_answers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("interview_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("interview_questions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    answer_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    is_voice_response: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    audio_file_path: Mapped[Optional[str]] = mapped_column(
        String(512),
        nullable=True,
    )

    duration_seconds: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    delivery_metrics: Mapped[Optional[Dict[str, Any]]] = mapped_column(
        JSON,
        nullable=True,
        default=dict,  # { speaking_rate_wpm, pause_count, filler_words: [], filler_count }
    )

    score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,  # 0 to 100
    )

    relevance_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    technical_accuracy_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    completeness_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    clarity_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    detailed_feedback: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    improvement_tips: Mapped[Optional[List[str]]] = mapped_column(
        JSON,
        nullable=True,
        default=list,
    )

    concepts_to_revise: Mapped[Optional[List[str]]] = mapped_column(
        JSON,
        nullable=True,
        default=list,
    )

    submitted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    evaluated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    session: Mapped["InterviewSession"] = relationship("InterviewSession", back_populates="answers")
    question: Mapped["InterviewQuestion"] = relationship("InterviewQuestion", back_populates="answer")
