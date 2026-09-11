import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional, List
from sqlalchemy import String, DateTime, UUID, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.user import User


class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    target_role: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    experience_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    target_companies: Mapped[Optional[List[str]]] = mapped_column(JSON, default=list, nullable=True)
    tech_skills: Mapped[Optional[List[str]]] = mapped_column(JSON, default=list, nullable=True)
    github_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user: Mapped["User"] = relationship("User", back_populates="profile")
