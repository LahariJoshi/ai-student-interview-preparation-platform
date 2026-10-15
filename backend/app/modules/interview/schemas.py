from typing import List, Dict, Any, Optional
import uuid
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


# Request Schemas
class InterviewSessionCreate(BaseModel):
    interview_type: str = Field(default="mixed", description="technical, hr, behavioral, or mixed")
    target_role: str = Field(default="Software Developer", description="Target job title")
    experience_level: str = Field(default="Beginner", description="Beginner, Intermediate, or Advanced")
    duration_minutes: int = Field(default=15, ge=5, le=60, description="Interview duration in minutes")
    custom_skills: List[str] = Field(default_factory=list, description="Specific skills to test")
    resume_id: Optional[uuid.UUID] = Field(default=None, description="Optional resume ID for personalization")


class AnswerSubmitRequest(BaseModel):
    question_id: uuid.UUID
    answer_text: str = Field(..., min_length=1)
    is_voice_response: bool = False
    duration_seconds: Optional[float] = None
    delivery_metrics: Optional[Dict[str, Any]] = None


# Response Schemas
class QuestionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    order_index: int
    question_text: str
    category: str
    difficulty: str
    topic_or_skill: Optional[str] = None
    expected_key_points: List[str] = []
    reference_answer: Optional[str] = None


class AnswerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    question_id: uuid.UUID
    answer_text: str
    is_voice_response: bool
    score: Optional[float] = None
    relevance_score: Optional[float] = None
    technical_accuracy_score: Optional[float] = None
    completeness_score: Optional[float] = None
    clarity_score: Optional[float] = None
    detailed_feedback: Optional[str] = None
    improvement_tips: Optional[List[str]] = []
    concepts_to_revise: Optional[List[str]] = []
    delivery_metrics: Optional[Dict[str, Any]] = None
    submitted_at: datetime


class InterviewSessionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    resume_id: Optional[uuid.UUID] = None
    interview_type: str
    target_role: str
    experience_level: str
    duration_minutes: int
    custom_skills: List[str]
    status: str
    total_questions: int
    current_question_index: int
    overall_score: Optional[float] = None
    technical_score: Optional[float] = None
    communication_score: Optional[float] = None
    strengths: Optional[List[str]] = []
    weaknesses: Optional[List[str]] = []
    recommendations: Optional[List[Dict[str, Any]]] = []
    started_at: datetime
    ended_at: Optional[datetime] = None
    questions: List[QuestionOut] = []


class InterviewSessionListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    interview_type: str
    target_role: str
    experience_level: str
    duration_minutes: int
    status: str
    total_questions: int
    overall_score: Optional[float] = None
    started_at: datetime
    ended_at: Optional[datetime] = None


class InterviewHistoryResponse(BaseModel):
    total_interviews: int
    completed_interviews: int
    average_score: float
    sessions: List[InterviewSessionListItem]


class RecommendationItem(BaseModel):
    title: str
    description: str
    action_type: str
    link: str


class InterviewResultsResponse(BaseModel):
    session_id: uuid.UUID
    interview_type: str
    target_role: str
    experience_level: str
    status: str
    overall_score: float
    technical_score: float
    communication_score: float
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[RecommendationItem]
    started_at: datetime
    ended_at: Optional[datetime]
    total_questions: int
    questions: List[QuestionOut]
    answers: List[AnswerOut]


class AudioUploadResponse(BaseModel):
    transcript: str
    duration_seconds: float
    delivery_metrics: Dict[str, Any]
