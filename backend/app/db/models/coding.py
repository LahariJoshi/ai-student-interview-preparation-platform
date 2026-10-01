import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional, List, Dict, Any

from sqlalchemy import String, DateTime, UUID, ForeignKey, Text, Boolean, Integer, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.user import User


class CodingQuestion(Base):
    __tablename__ = "coding_questions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    difficulty: Mapped[str] = mapped_column(
        String(50),
        index=True,
        nullable=False,
    )

    topic: Mapped[str] = mapped_column(
        String(100),
        index=True,
        nullable=False,
    )

    constraints: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    hints: Mapped[Optional[List[str]]] = mapped_column(
        JSON,
        default=list,
        nullable=True,
    )

    starter_code: Mapped[Dict[str, str]] = mapped_column(
        JSON,
        nullable=False,
        default=dict,
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
    test_cases: Mapped[List["CodingTestCase"]] = relationship(
        "CodingTestCase",
        back_populates="question",
        cascade="all, delete-orphan",
        order_by="CodingTestCase.order_index",
    )

    submissions: Mapped[List["CodingSubmission"]] = relationship(
        "CodingSubmission",
        back_populates="question",
        cascade="all, delete-orphan",
    )


class CodingTestCase(Base):
    __tablename__ = "coding_test_cases"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("coding_questions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    input_data: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    expected_output: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    is_sample: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    explanation: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    order_index: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationship
    question: Mapped["CodingQuestion"] = relationship(
        "CodingQuestion",
        back_populates="test_cases",
    )


class CodingSubmission(Base):
    __tablename__ = "coding_submissions"

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

    question_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("coding_questions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    language: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship(
        "User",
        back_populates="coding_submissions",
    )

    question: Mapped["CodingQuestion"] = relationship(
        "CodingQuestion",
        back_populates="submissions",
    )

    result: Mapped[Optional["CodingResult"]] = relationship(
        "CodingResult",
        back_populates="submission",
        uselist=False,
        cascade="all, delete-orphan",
    )


class CodingResult(Base):
    __tablename__ = "coding_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    submission_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("coding_submissions.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    verdict: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )

    passed_test_cases: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    total_test_cases: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    execution_time_ms: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    memory_kb: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    test_case_results_json: Mapped[Optional[List[Dict[str, Any]]]] = mapped_column(
        JSON,
        nullable=True,
    )

    evaluated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationship
    submission: Mapped["CodingSubmission"] = relationship(
        "CodingSubmission",
        back_populates="result",
    )
