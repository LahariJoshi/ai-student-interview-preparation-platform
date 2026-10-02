import re
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator



# ============================================================================
# TEST CASE SCHEMAS
# ============================================================================

class TestCaseBase(BaseModel):
    input_data: str = Field(..., description="Standard input or arguments")
    expected_output: str = Field(..., description="Expected output string")
    is_sample: bool = Field(False, description="Whether test case is visible as sample")
    explanation: Optional[str] = Field(None, description="Optional explanation for sample case")
    order_index: int = Field(0, description="Display order index")


class TestCaseCreate(TestCaseBase):
    pass


class TestCaseUpdate(BaseModel):
    input_data: Optional[str] = None
    expected_output: Optional[str] = None
    is_sample: Optional[bool] = None
    explanation: Optional[str] = None
    order_index: Optional[int] = None


class TestCaseSampleOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    input_data: str
    expected_output: str
    is_sample: bool
    explanation: Optional[str] = None
    order_index: int


class TestCaseOut(TestCaseSampleOut):
    created_at: datetime


class TestCaseBatchCreate(BaseModel):
    test_cases: List[TestCaseCreate] = Field(..., min_length=1)


class TestCaseReorderItem(BaseModel):
    id: UUID
    order_index: int


class TestCaseReorderRequest(BaseModel):
    items: List[TestCaseReorderItem] = Field(..., min_length=1)


class TestCaseListOut(BaseModel):
    total_count: int
    sample_count: int
    hidden_count: int
    test_cases: List[TestCaseOut]


# ============================================================================
# CODING QUESTION SCHEMAS
# ============================================================================

ALLOWED_DIFFICULTIES = {"Easy", "Medium", "Hard"}
ALLOWED_STATUSES = {"all", "solved", "unsolved"}
ALLOWED_SORT_FIELDS = {"created_at", "title", "difficulty"}
ALLOWED_SORT_ORDERS = {"asc", "desc"}
ALLOWED_LANGUAGES = {"python", "javascript", "typescript", "java", "cpp"}
ALLOWED_SUBMISSION_STATUSES = {"pending", "running", "completed", "failed"}


class TopicSummaryOut(BaseModel):
    topic: str
    question_count: int
    easy_count: int = 0
    medium_count: int = 0
    hard_count: int = 0


class DifficultySummaryOut(BaseModel):
    difficulty: str
    question_count: int


class QuestionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    slug: Optional[str] = Field(None, max_length=255)
    description: str = Field(..., min_length=1)
    difficulty: str = Field(..., description="Easy, Medium, or Hard")
    topic: str = Field(..., min_length=1, max_length=100)
    constraints: Optional[str] = None
    hints: Optional[List[str]] = Field(default_factory=list)
    starter_code: Dict[str, str] = Field(default_factory=dict)

    @field_validator("difficulty")
    @classmethod
    def validate_difficulty(cls, v: str) -> str:
        formatted = v.strip().capitalize()
        if formatted not in ALLOWED_DIFFICULTIES:
            raise ValueError(f"Difficulty must be one of: {', '.join(sorted(ALLOWED_DIFFICULTIES))}")
        return formatted


class QuestionCreate(QuestionBase):
    test_cases: Optional[List[TestCaseCreate]] = Field(default_factory=list)

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: Optional[str]) -> Optional[str]:
        if v:
            clean = re.sub(r"[^\w-]", "", v.lower().strip().replace(" ", "-"))
            return clean
        return None


class QuestionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    slug: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, min_length=1)
    difficulty: Optional[str] = None
    topic: Optional[str] = Field(None, min_length=1, max_length=100)
    constraints: Optional[str] = None
    hints: Optional[List[str]] = None
    starter_code: Optional[Dict[str, str]] = None

    @field_validator("difficulty")
    @classmethod
    def validate_difficulty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            formatted = v.strip().capitalize()
            if formatted not in ALLOWED_DIFFICULTIES:
                raise ValueError(f"Difficulty must be one of: {', '.join(sorted(ALLOWED_DIFFICULTIES))}")
            return formatted
        return None


class QuestionListItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    slug: str
    difficulty: str
    topic: str
    sample_test_case_count: int = 0
    is_solved: Optional[bool] = None
    created_at: datetime


class QuestionListOut(BaseModel):
    total_count: int
    page: int = 1
    limit: int = 50
    total_pages: int = 1
    questions: List[QuestionListItemOut]


class QuestionDetailOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    slug: str
    description: str
    difficulty: str
    topic: str
    constraints: Optional[str] = None
    hints: Optional[List[str]] = Field(default_factory=list)
    starter_code: Dict[str, str] = Field(default_factory=dict)
    sample_test_cases: List[TestCaseSampleOut] = Field(default_factory=list)
    is_solved: Optional[bool] = None
    created_at: datetime
    updated_at: datetime


class QuestionAdminDetailOut(QuestionDetailOut):
    all_test_cases: List[TestCaseOut] = Field(default_factory=list)


# ============================================================================
# CODING SUBMISSION SCHEMAS
# ============================================================================

class SubmissionCreate(BaseModel):
    question_id: Any = Field(..., description="UUID or slug of question being solved")
    language: str = Field(..., description="Programming language (e.g. python, javascript, typescript, java, cpp)")
    code: str = Field(..., min_length=1, max_length=65536, description="Submitted source code")

    @field_validator("language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        clean = v.strip().lower()
        if clean not in ALLOWED_LANGUAGES:
            raise ValueError(
                f"Language '{v}' is not supported. Supported languages: {', '.join(sorted(ALLOWED_LANGUAGES))}"
            )
        return clean

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Submitted code cannot be empty or pure whitespace.")
        return v


class SubmissionStatusUpdate(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        clean = v.strip().lower()
        if clean not in ALLOWED_SUBMISSION_STATUSES:
            raise ValueError(
                f"Status must be one of: {', '.join(sorted(ALLOWED_SUBMISSION_STATUSES))}"
            )
        return clean


class TestCaseRunResultOut(BaseModel):
    test_case_id: UUID
    order_index: int
    is_sample: bool
    passed: bool
    verdict: str
    execution_time_ms: float = 0.0
    actual_output: Optional[str] = None
    expected_output: Optional[str] = None
    input_data: Optional[str] = None
    error_message: Optional[str] = None


class CodeRunRequest(BaseModel):
    question_id: Optional[Any] = Field(None, description="UUID or slug of question being run")
    language: str = Field(..., description="Programming language (e.g. python, javascript, typescript, java, cpp)")
    code: str = Field(..., min_length=1, max_length=65536, description="Source code to run")

    @field_validator("language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        clean = v.strip().lower()
        if clean not in ALLOWED_LANGUAGES:
            raise ValueError(
                f"Language '{v}' is not supported. Supported languages: {', '.join(sorted(ALLOWED_LANGUAGES))}"
            )
        return clean

    @field_validator("code")
    @classmethod
    def validate_code(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Code cannot be empty or pure whitespace.")
        return v


class CodeRunResponse(BaseModel):
    verdict: str
    passed_test_cases: int
    total_test_cases: int
    execution_time_ms: float = 0.0
    error_message: Optional[str] = None
    test_cases: List[TestCaseRunResultOut]


class SubmissionResultSummaryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    verdict: str
    score: float
    passed_test_cases: int
    total_test_cases: int
    execution_time_ms: Optional[float] = None
    memory_kb: Optional[float] = None
    error_message: Optional[str] = None
    test_case_results: Optional[List[Dict[str, Any]]] = None


class SubmissionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    question_id: UUID
    language: str
    code: str
    status: str
    created_at: datetime
    question_title: Optional[str] = None
    question_slug: Optional[str] = None
    question_difficulty: Optional[str] = None
    question_topic: Optional[str] = None
    result: Optional[SubmissionResultSummaryOut] = None


class SubmissionListItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    question_id: UUID
    language: str
    status: str
    created_at: datetime
    question_title: Optional[str] = None
    question_slug: Optional[str] = None
    question_difficulty: Optional[str] = None
    question_topic: Optional[str] = None
    score: Optional[float] = None
    verdict: Optional[str] = None
    passed_test_cases: Optional[int] = None
    total_test_cases: Optional[int] = None


class SubmissionListOut(BaseModel):
    total_count: int
    page: int = 1
    limit: int = 50
    total_pages: int = 1
    submissions: List[SubmissionListItemOut]


# ============================================================================
# GENERIC MESSAGE RESPONSE
# ============================================================================

class MessageResponse(BaseModel):
    message: str


# ============================================================================
# SCORING & PERFORMANCE ANALYTICS SCHEMAS
# ============================================================================

class CodingMetricsOut(BaseModel):
    execution_time_ms: float = 0.0
    memory_kb: float = 12400.0


class NormalizedPerformanceResultOut(BaseModel):
    submission_id: UUID
    score: float
    passed_tests: int
    total_tests: int
    topic: str
    difficulty: str
    execution_status: str
    coding_metrics: CodingMetricsOut


class TopicPerformanceOut(BaseModel):
    topic: str
    questions_attempted: int
    questions_solved: int
    total_submissions: int
    accuracy_percentage: float
    average_score: float
    proficiency_level: str


class DifficultyBreakdownOut(BaseModel):
    difficulty: str
    total_available: int
    questions_attempted: int
    questions_solved: int
    solve_rate_percentage: float
    average_score: float


class WeakTopicOut(BaseModel):
    topic: str
    questions_attempted: int
    questions_solved: int
    accuracy_percentage: float
    average_score: float
    recommended_focus: str


class CodingHistoryItemOut(BaseModel):
    submission_id: UUID
    question_id: UUID
    question_title: str
    question_slug: str
    difficulty: str
    topic: str
    language: str
    verdict: str
    score: float
    passed_test_cases: int
    total_test_cases: int
    execution_time_ms: Optional[float] = None
    created_at: datetime


class CodingProgressSummaryOut(BaseModel):
    total_questions_in_bank: int
    total_questions_attempted: int
    total_questions_solved: int
    solve_rate_percentage: float
    total_submissions: int
    overall_coding_score: float
    easy_solved: int
    easy_total: int
    medium_solved: int
    medium_total: int
    hard_solved: int
    hard_total: int
    weak_topics: List[str]


class RecommendationContextOut(BaseModel):
    coding_score: float
    weak_topics: List[str]
    difficulty_performance: Dict[str, Dict[str, Any]]
    total_solved: int
    total_attempted: int
    proficiency_level: str

