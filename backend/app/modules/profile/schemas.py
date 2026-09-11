from uuid import UUID
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, HttpUrl, ConfigDict


class ProfileOut(BaseModel):
    id: UUID
    user_id: UUID
    target_role: Optional[str] = None
    experience_level: Optional[str] = None
    target_companies: List[str] = []
    tech_skills: List[str] = []
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProfileUpdate(BaseModel):
    target_role: Optional[str] = None
    experience_level: Optional[str] = None
    target_companies: Optional[List[str]] = None
    tech_skills: Optional[List[str]] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
