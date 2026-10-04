from datetime import datetime
from typing import Optional, Dict, List, Any
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.modules.interview.schemas import AnswerAnalysisResult


class VoiceAnalysisBase(BaseModel):
    speaking_rate_wpm: float = Field(default=0.0, description="Speaking rate in words per minute")
    filler_word_count: int = Field(default=0, description="Total filler words counted")
    filler_words_detected: Optional[Dict[str, int]] = Field(default_factory=dict, description="Counts per filler word")
    pause_count: int = Field(default=0, description="Number of detected pauses")
    total_pause_duration_seconds: float = Field(default=0.0, description="Total pause duration in seconds")
    clarity_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Speech clarity score 0-100")
    confidence_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Delivery confidence score 0-100")
    tone_evaluation: Optional[str] = Field(default=None, description="Tone descriptor e.g. confident, clear")
    communication_feedback: str = Field(default="", description="Qualitative communication coaching feedback")


class VoiceAnalysisCreate(VoiceAnalysisBase):
    response_id: UUID
    audio_url: Optional[str] = None


class VoiceAnalysisOut(VoiceAnalysisBase):
    id: UUID
    response_id: UUID
    audio_url: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VoiceMetricsRequest(BaseModel):
    transcribed_text: str = Field(..., description="Transcript text to calculate speech metrics on")
    duration_seconds: float = Field(..., gt=0.0, description="Recorded audio duration in seconds")


class AudioUploadOut(BaseModel):
    message: str = "Audio uploaded successfully"
    response_id: UUID
    session_id: UUID
    file_name: str
    file_size_bytes: int
    mime_type: str
    duration_seconds: Optional[float] = None
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)


class STTResultOut(BaseModel):
    transcript: str = Field(..., description="Transcribed spoken text")
    language: str = Field(default="en", description="Detected language code (e.g. en)")
    confidence: float = Field(default=0.95, ge=0.0, le=1.0, description="Confidence score between 0.0 and 1.0")

    model_config = ConfigDict(from_attributes=True)


class FillerAnalysisResult(BaseModel):
    filler_word_count: int
    filler_words: Dict[str, int] = Field(default_factory=dict)
    filler_rate: float

    model_config = ConfigDict(from_attributes=True)


class SpeakingRateResult(BaseModel):
    word_count: int
    duration_seconds: float
    speech_rate_wpm: float

    model_config = ConfigDict(from_attributes=True)


class PauseAnalysisResult(BaseModel):
    pause_count: int
    total_pause_seconds: float
    average_pause_seconds: float
    longest_pause_seconds: float
    data_availability: str = Field(
        default="unavailable",
        description="'precise' when exact audio timing data was provided, 'unavailable' otherwise",
    )
    is_estimated: bool = Field(default=True)

    model_config = ConfigDict(from_attributes=True)


class VoiceMetricsOut(BaseModel):
    filler_analysis: FillerAnalysisResult
    speaking_rate: SpeakingRateResult
    pause_analysis: PauseAnalysisResult

    model_config = ConfigDict(from_attributes=True)


class CommunicationFeedbackResult(BaseModel):
    communication_score: float = Field(..., ge=0.0, le=100.0, description="Overall communication score (0-100)")
    strengths: List[str] = Field(default_factory=list, description="Communication delivery strengths")
    areas_to_improve: List[str] = Field(default_factory=list, description="Targeted delivery areas to polish")
    feedback: List[str] = Field(default_factory=list, description="Detailed explanatory coaching feedback")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Underlying voice metrics snapshot")

    @field_validator("communication_score", mode="before")
    @classmethod
    def clamp_score(cls, v: Any) -> float:
        try:
            val = float(v)
            return max(0.0, min(100.0, round(val, 1)))
        except (ValueError, TypeError):
            return 50.0

    model_config = ConfigDict(from_attributes=True)


class VoicePipelineResultOut(BaseModel):
    response_id: UUID
    session_id: UUID
    question_id: UUID
    transcript: str
    answer_score: float
    communication_score: float
    answer_analysis: AnswerAnalysisResult
    voice_metrics: VoiceMetricsOut
    communication_feedback: CommunicationFeedbackResult
    status: str = "completed"

    model_config = ConfigDict(from_attributes=True)





