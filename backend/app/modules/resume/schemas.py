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


# ── Milestone 3 + Milestone 4: Resume Analysis Schemas ──────────────────────

class ResumeAnalysisOut(BaseModel):
    id: UUID
    resume_id: UUID
    user_id: UUID

    analysis_status: str

    # Final M4 advanced quality score
    quality_score: Optional[float] = None

    # M3 structural analysis
    sections_json: Optional[Dict[str, bool]] = None

    # Detected skills by category
    skills_json: Optional[Dict[str, List[str]]] = None

    # Evidence-based improvement gaps
    gaps_json: Optional[List[Dict[str, str]]] = None

    # Contains both M3 and M4 quality analysis
    #
    # Example:
    # {
    #     "m3_structural": {...},
    #     "m4_advanced": {...}
    # }
    quality_details_json: Optional[Dict[str, Any]] = None

    analyzed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AnalysisTriggerResponse(BaseModel):
    message: str
    resume_id: UUID
    analysis_status: str