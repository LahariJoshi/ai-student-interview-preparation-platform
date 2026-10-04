import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional, Dict

from sqlalchemy import String, DateTime, UUID, ForeignKey, Float, Integer, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.modules.interview.models import InterviewResponse


class VoiceAnalysis(Base):
    __tablename__ = "voice_analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    response_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("interview_responses.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    audio_url: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True,
    )
    speaking_rate_wpm: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    filler_word_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    filler_words_detected: Mapped[Optional[Dict[str, int]]] = mapped_column(
        JSON,
        default=dict,
        nullable=True,
    )
    pause_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )
    total_pause_duration_seconds: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    clarity_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    confidence_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    tone_evaluation: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )
    communication_feedback: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationship
    response: Mapped["InterviewResponse"] = relationship(
        "InterviewResponse",
        back_populates="voice_analysis",
    )
