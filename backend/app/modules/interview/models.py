import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional, List

from sqlalchemy import String, DateTime, UUID, ForeignKey, Float, Integer, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.user import User
    from app.modules.voice.models import VoiceAnalysis


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
    target_role: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    interview_type: Mapped[str] = mapped_column(
        String(50),
        default="Mixed",  # "Technical", "Behavioral", "HR", "Mixed"
        nullable=False,
    )
    experience_level: Mapped[str] = mapped_column(
        String(50),
        default="Fresher",  # "Fresher", "Beginner", "Intermediate"
        nullable=False,
    )
    difficulty: Mapped[str] = mapped_column(
        String(50),
        default="Medium",  # "Easy", "Medium", "Hard"
        nullable=False,
    )
    answer_mode: Mapped[str] = mapped_column(
        String(50),
        default="Voice + Text",  # "Voice", "Text", "Voice + Text"
        nullable=False,
    )
    question_count: Mapped[int] = mapped_column(
        Integer,
        default=5,
        nullable=False,
    )
    target_company: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",  # "pending", "in_progress", "completed", "abandoned"
        nullable=False,
        index=True,
    )
    current_question_index: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    def __init__(self, **kwargs):
        if "role" in kwargs and "target_role" not in kwargs:
            kwargs["target_role"] = kwargs.pop("role")
        if "total_questions" in kwargs and "question_count" not in kwargs:
            kwargs["question_count"] = kwargs.pop("total_questions")
        super().__init__(**kwargs)

    @property
    def role(self) -> str:
        return self.target_role

    @role.setter
    def role(self, val: str):
        self.target_role = val

    @property
    def total_questions(self) -> int:
        return self.question_count

    @total_questions.setter
    def total_questions(self, val: int):
        self.question_count = val

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
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="interview_sessions",
    )
    questions: Mapped[List["InterviewQuestion"]] = relationship(
        "InterviewQuestion",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="InterviewQuestion.question_order",
        lazy="selectin",
    )
    responses: Mapped[List["InterviewResponse"]] = relationship(
        "InterviewResponse",
        back_populates="session",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    feedback: Mapped[Optional["InterviewFeedback"]] = relationship(
        "InterviewFeedback",
        back_populates="session",
        cascade="all, delete-orphan",
        uselist=False,
        lazy="selectin",
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
    question_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    category: Mapped[str] = mapped_column(
        String(50),
        default="technical",  # "technical", "behavioral", "situational"
        nullable=False,
    )
    topic: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    question_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    expected_points: Mapped[Optional[List[str]]] = mapped_column(
        JSON,
        default=list,
        nullable=True,
    )
    difficulty: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    session: Mapped["InterviewSession"] = relationship(
        "InterviewSession",
        back_populates="questions",
    )
    response: Mapped[Optional["InterviewResponse"]] = relationship(
        "InterviewResponse",
        back_populates="question",
        cascade="all, delete-orphan",
        uselist=False,
    )


class InterviewResponse(Base):
    __tablename__ = "interview_responses"

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
        index=True,
    )
    transcribed_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    audio_file_path: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )
    audio_duration_seconds: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )
    score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )
    feedback_text: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    key_strengths: Mapped[Optional[List[str]]] = mapped_column(
        JSON,
        default=list,
        nullable=True,
    )
    missing_concepts: Mapped[Optional[List[str]]] = mapped_column(
        JSON,
        default=list,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    session: Mapped["InterviewSession"] = relationship(
        "InterviewSession",
        back_populates="responses",
    )
    question: Mapped["InterviewQuestion"] = relationship(
        "InterviewQuestion",
        back_populates="response",
    )
    voice_analysis: Mapped[Optional["VoiceAnalysis"]] = relationship(
        "VoiceAnalysis",
        back_populates="response",
        cascade="all, delete-orphan",
        uselist=False,
        lazy="selectin",
    )


class InterviewFeedback(Base):
    __tablename__ = "interview_feedback"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    session_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("interview_sessions.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    overall_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    technical_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    communication_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    key_strengths: Mapped[Optional[List[str]]] = mapped_column(
        JSON,
        default=list,
        nullable=True,
    )
    areas_for_improvement: Mapped[Optional[List[str]]] = mapped_column(
        JSON,
        default=list,
        nullable=True,
    )
    actionable_recommendations: Mapped[Optional[List[str]]] = mapped_column(
        JSON,
        default=list,
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationship
    session: Mapped["InterviewSession"] = relationship(
        "InterviewSession",
        back_populates="feedback",
    )
