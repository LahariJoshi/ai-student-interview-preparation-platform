from uuid import UUID
from datetime import datetime
from typing import Dict, List, Optional, Any

from pydantic import BaseModel, ConfigDict


class ResumeOut(BaseModel):
    id: UUID
    user_id: UUID
    original_filename: str
    file_size: int
    mime_type: str
    created_at: datetime

    extraction_status: str
    character_count: Optional[int] = None
    word_count: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class ResumeListOut(BaseModel):
    resumes: List[ResumeOut]
    total_count: int


class ResumeTextOut(BaseModel):
    id: UUID
    extraction_status: str
    raw_text: Optional[str] = None
    character_count: Optional[int] = None
    word_count: Optional[int] = None
    extracted_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    message: str


# ── Milestone 3: Resume Analysis Schemas ─────────────────────────────────────

class ResumeAnalysisOut(BaseModel):
    id: UUID
    resume_id: UUID
    user_id: UUID
    analysis_status: str
    quality_score: Optional[float] = None
    sections_json: Optional[Dict[str, bool]] = None
    skills_json: Optional[Dict[str, List[str]]] = None
    gaps_json: Optional[List[Dict[str, str]]] = None
    quality_details_json: Optional[Dict[str, Any]] = None
    analyzed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnalysisTriggerResponse(BaseModel):
    message: str
    resume_id: UUID
    analysis_status: str