from uuid import UUID
from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict


class ResumeOut(BaseModel):
    id: UUID
    user_id: UUID
    original_filename: str
    file_size: int
    mime_type: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResumeListOut(BaseModel):
    resumes: List[ResumeOut]
    total_count: int


class MessageResponse(BaseModel):
    message: str
