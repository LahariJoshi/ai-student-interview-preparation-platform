import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, DateTime, UUID, ForeignKey, Float, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


if TYPE_CHECKING:
    from app.db.models.user import User
    from app.db.models.resume import Resume
    from app.db.models.job_description import JobDescription


class ATSAnalysis(Base):
    __tablename__ = "ats_analyses"

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

    resume_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    job_description_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("job_descriptions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Analysis status:
    # "pending" | "completed" | "failed"
    analysis_status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False,
    )

    # Overall ATS score: 0–100
    ats_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    # ATS score components
    formatting_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    keyword_match_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    semantic_similarity_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    action_impact_score: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    # Structured matching results
    matched_skills_json: Mapped[Optional[list]] = mapped_column(
        JSON,
        nullable=True,
    )

    missing_skills_json: Mapped[Optional[list]] = mapped_column(
        JSON,
        nullable=True,
    )

    jd_requirements_json: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
    )

    analysis_details_json: Mapped[Optional[dict]] = mapped_column(
        JSON,
        nullable=True,
    )

    analyzed_at: Mapped[Optional[datetime]] = mapped_column(
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
    user: Mapped["User"] = relationship(
        "User",
        back_populates="ats_analyses",
    )

    resume: Mapped["Resume"] = relationship(
        "Resume",
    )

    job_description: Mapped["JobDescription"] = relationship(
        "JobDescription",
        back_populates="ats_analyses",
    )