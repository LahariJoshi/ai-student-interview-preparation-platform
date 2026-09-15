from uuid import UUID
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class JobDescriptionCreate(BaseModel):
    title: str
    company_name: Optional[str] = None
    description_text: str


class JobDescriptionOut(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    company_name: Optional[str] = None
    description_text: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class JobDescriptionListOut(BaseModel):
    job_descriptions: List[JobDescriptionOut]
    total_count: int


class MessageResponse(BaseModel):
    message: str