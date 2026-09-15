import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, Integer, DateTime, UUID, ForeignKey, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.resume import Resume
    from app.db.models.user import User


class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    resume_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("resumes.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Analysis status: "pending" | "completed" | "failed"
    analysis_status: Mapped[str] = mapped_column(
        String(50), default="pending", nullable=False
    )

    # Overall quality score 0–100 (nullable until analysis runs)
    quality_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # JSON columns storing structured analysis results
    sections_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    skills_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    gaps_json: Mapped[Optional[list]] = mapped_column(JSON, nullable=True)
    quality_details_json: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)

    analyzed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
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
    resume: Mapped["Resume"] = relationship("Resume", back_populates="analysis")
    user: Mapped["User"] = relationship("User", back_populates="resume_analyses")
