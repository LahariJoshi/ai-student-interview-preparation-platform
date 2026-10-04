from datetime import datetime
from enum import Enum
from typing import Optional, List, Any, Dict
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator


# ==========================================
# Enumerations for Setup Configuration
# ==========================================
class InterviewType(str, Enum):
    TECHNICAL = "Technical"
    BEHAVIORAL = "Behavioral"
    HR = "HR"
    MIXED = "Mixed"

    @classmethod
    def _missing_(cls, value: object):
        if isinstance(value, str):
            val_lower = value.strip().lower()
            for member in cls:
                if member.value.lower() == val_lower:
                    return member
        return None


class ExperienceLevel(str, Enum):
    FRESHER = "Fresher"
    BEGINNER = "Beginner"
    INTERMEDIATE = "Intermediate"

    @classmethod
    def _missing_(cls, value: object):
        if isinstance(value, str):
            val_lower = value.strip().lower()
            for member in cls:
                if member.value.lower() == val_lower:
                    return member
        return None


class DifficultyLevel(str, Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

    @classmethod
    def _missing_(cls, value: object):
        if isinstance(value, str):
            val_lower = value.strip().lower()
            for member in cls:
                if member.value.lower() == val_lower:
                    return member
        return None


class AnswerMode(str, Enum):
    VOICE = "Voice"
    TEXT = "Text"
    VOICE_AND_TEXT = "Voice + Text"

    @classmethod
    def _missing_(cls, value: object):
        if isinstance(value, str):
            val_normalized = value.strip().lower().replace("and", "+")
            for member in cls:
                if member.value.lower().replace("and", "+") == val_normalized:
                    return member
        return None


# ==========================================
# Session Request & Response Schemas
# ==========================================
class InterviewSessionCreate(BaseModel):
    target_role: Optional[str] = Field(None, min_length=2, max_length=100, description="Target job role")
    role: Optional[str] = Field(None, min_length=2, max_length=100, description="Alias for target_role")
    interview_type: InterviewType = Field(default=InterviewType.MIXED, description="Technical, Behavioral, HR, Mixed")
    experience_level: ExperienceLevel = Field(default=ExperienceLevel.FRESHER, description="Fresher, Beginner, Intermediate")
    difficulty: DifficultyLevel = Field(default=DifficultyLevel.MEDIUM, description="Easy, Medium, Hard")
    question_count: int = Field(default=5, ge=1, le=20, description="Number of questions (1-20)")
    answer_mode: AnswerMode = Field(default=AnswerMode.VOICE_AND_TEXT, description="Voice, Text, Voice + Text")
    target_company: Optional[str] = Field(default=None, max_length=255, description="Target company name (optional)")

    @field_validator("target_role", mode="before")
    @classmethod
    def validate_target_role(cls, v: Any, info) -> Any:
        return v

    def get_role(self) -> str:
        role = self.target_role or self.role
        if not role or not role.strip():
            raise ValueError("target_role is required")
        return role.strip()


class InterviewSessionUpdate(BaseModel):
    status: Optional[str] = None
    current_question_index: Optional[int] = None
    overall_score: Optional[float] = None
    technical_score: Optional[float] = None
    communication_score: Optional[float] = None
    completed_at: Optional[datetime] = None


class InterviewSessionOut(BaseModel):
    id: UUID
    user_id: UUID
    target_role: str
    interview_type: str
    experience_level: str
    difficulty: str
    answer_mode: str
    question_count: int
    target_company: Optional[str] = None
    status: str
    current_question_index: int
    overall_score: Optional[float] = None
    technical_score: Optional[float] = None
    communication_score: Optional[float] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Question Schemas
# ==========================================
class InterviewQuestionBase(BaseModel):
    category: str = Field(default="technical", description="Question category: technical, behavioral, situational")
    topic: Optional[str] = Field(default=None, description="Topic or skill area")
    question_text: str = Field(..., description="The interview question text")
    expected_points: Optional[List[str]] = Field(default_factory=list, description="Key concepts expected in good answers")
    difficulty: Optional[str] = Field(default="Medium", description="Difficulty level")


class InterviewQuestionCreate(InterviewQuestionBase):
    session_id: UUID
    question_order: int


class InterviewQuestionOut(InterviewQuestionBase):
    id: UUID
    session_id: UUID
    question_order: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Response Schemas
# ==========================================
class InterviewResponseBase(BaseModel):
    transcribed_text: str = Field(..., description="Student's answer text")
    audio_file_path: Optional[str] = Field(default=None, description="Path to recorded audio file")
    audio_duration_seconds: Optional[float] = Field(default=None, description="Audio duration in seconds")


class InterviewResponseCreate(InterviewResponseBase):
    question_id: UUID


class AnswerSubmitRequest(BaseModel):
    question_id: UUID
    transcribed_text: Optional[str] = None
    answer_text: Optional[str] = None

    def get_text(self) -> str:
        text = self.transcribed_text or self.answer_text or ""
        return text.strip()


class InterviewResponseCreateRequest(BaseModel):
    question_id: UUID
    answer_text: str = Field(..., description="Student's answer text")
    allow_retry: bool = Field(default=False, description="Explicitly allow updating existing answer")

    @field_validator("answer_text")
    @classmethod
    def validate_answer_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Answer text cannot be empty or whitespace only.")
        return v.strip()


class InterviewResponseOut(InterviewResponseBase):
    id: UUID
    session_id: UUID
    question_id: UUID
    score: Optional[float] = None
    feedback_text: Optional[str] = None
    key_strengths: Optional[List[str]] = Field(default_factory=list)
    missing_concepts: Optional[List[str]] = Field(default_factory=list)
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Feedback Schemas
# ==========================================
class InterviewFeedbackBase(BaseModel):
    overall_score: float = Field(..., ge=0.0, le=100.0)
    technical_score: float = Field(..., ge=0.0, le=100.0)
    communication_score: float = Field(..., ge=0.0, le=100.0)
    summary: str
    key_strengths: Optional[List[str]] = Field(default_factory=list)
    areas_for_improvement: Optional[List[str]] = Field(default_factory=list)
    actionable_recommendations: Optional[List[str]] = Field(default_factory=list)


class InterviewFeedbackCreate(InterviewFeedbackBase):
    session_id: UUID


class InterviewFeedbackOut(InterviewFeedbackBase):
    id: UUID
    session_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InterviewSessionDetailOut(InterviewSessionOut):
    questions: List[InterviewQuestionOut] = []
    responses: List[InterviewResponseOut] = []
    feedback: Optional[InterviewFeedbackOut] = None

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Answer Analysis & Evaluation Schemas
# ==========================================
class AnswerAnalysisResult(BaseModel):
    score: float = Field(..., ge=0.0, le=100.0, description="Overall answer score (0-100)")
    technical_score: float = Field(..., ge=0.0, le=100.0, description="Technical correctness score (0-100)")
    relevance_score: float = Field(..., ge=0.0, le=100.0, description="Relevance to question score (0-100)")
    clarity_score: float = Field(..., ge=0.0, le=100.0, description="Clarity and structure score (0-100)")
    strengths: List[str] = Field(default_factory=list, description="Key strengths identified in the answer")
    weaknesses: List[str] = Field(default_factory=list, description="Weaknesses or omissions identified")
    feedback: List[str] = Field(default_factory=list, description="Constructive feedback points")
    improvements: List[str] = Field(default_factory=list, description="Specific suggestions for improvement")

    @field_validator("score", "technical_score", "relevance_score", "clarity_score", mode="before")
    @classmethod
    def clamp_score(cls, v: Any) -> float:
        try:
            val = float(v)
            return max(0.0, min(100.0, round(val, 1)))
        except (ValueError, TypeError):
            return 50.0

    @field_validator("strengths", "weaknesses", "feedback", "improvements", mode="before")
    @classmethod
    def ensure_string_list(cls, v: Any) -> List[str]:
        if isinstance(v, list):
            return [str(item).strip() for item in v if str(item).strip()]
        elif isinstance(v, str) and v.strip():
            return [v.strip()]
        return []

    model_config = ConfigDict(from_attributes=True)


class EvaluateAnswerRequest(BaseModel):
    response_id: Optional[UUID] = None
    question_id: Optional[UUID] = None
    answer_text: Optional[str] = None


# ==========================================
# Final Interview Result Schemas
# ==========================================

class QuestionPerformanceOut(BaseModel):
    question_id: UUID
    question_order: int
    question_text: str
    category: str
    difficulty: Optional[str] = None
    topic: Optional[str] = None
    candidate_answer: Optional[str] = None
    score: Optional[float] = None
    feedback: Optional[str] = None
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    audio_duration_seconds: Optional[float] = None
    speaking_rate_wpm: Optional[float] = None
    filler_word_count: Optional[int] = None
    clarity_score: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class AggregateVoiceMetricsOut(BaseModel):
    has_voice_data: bool = False
    average_speaking_rate_wpm: float = 0.0
    total_filler_word_count: int = 0
    filler_words_detected: Dict[str, int] = Field(default_factory=dict)
    average_clarity_score: float = 0.0
    total_pause_count: int = 0
    total_pause_duration_seconds: float = 0.0
    tone_evaluation: Optional[str] = None
    communication_feedback: List[str] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class InterviewResultOut(BaseModel):
    session_id: UUID
    target_role: str
    interview_type: str
    experience_level: str
    difficulty: str
    status: str
    interview_score: float = Field(..., ge=0.0, le=100.0, description="Overall blended interview score")
    technical_score: float = Field(..., ge=0.0, le=100.0, description="Technical correctness & depth score")
    communication_score: float = Field(..., ge=0.0, le=100.0, description="Communication clarity & delivery score")
    total_questions: int
    answered_questions: int
    interview_duration_seconds: float
    formatted_duration: str
    summary: str
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    answer_feedback: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    voice_metrics: AggregateVoiceMetricsOut
    question_performance: List[QuestionPerformanceOut] = Field(default_factory=list)
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class InterviewHistoryItemOut(BaseModel):
    id: UUID
    date: datetime = Field(..., description="Date of interview session creation")
    created_at: datetime
    completed_at: Optional[datetime] = None
    target_role: str
    interview_type: str
    experience_level: Optional[str] = None
    difficulty: Optional[str] = None
    status: str
    number_of_questions: int
    question_count: int
    overall_score: Optional[float] = None
    technical_score: Optional[float] = None
    communication_score: Optional[float] = None
    duration: str = Field(default="0s", description="Human-readable duration")
    formatted_duration: str = Field(default="0s", description="Human-readable duration")
    duration_seconds: float = 0.0

    model_config = ConfigDict(from_attributes=True)


class InterviewHistoryPaginationOut(BaseModel):
    items: List[InterviewHistoryItemOut]
    total: int
    skip: int
    limit: int
    page: int
    total_pages: int

    model_config = ConfigDict(from_attributes=True)
