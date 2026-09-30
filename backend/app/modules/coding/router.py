import math
import uuid
from typing import Optional, List
import jwt
from fastapi import APIRouter, Depends, HTTPException, status as http_status, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_user
from app.db.models.user import User

from app.modules.coding.schemas import (
    QuestionCreate,
    QuestionUpdate,
    QuestionListOut,
    QuestionDetailOut,
    TopicSummaryOut,
    DifficultySummaryOut,
    TestCaseCreate,
    TestCaseUpdate,
    TestCaseOut,
    TestCaseSampleOut,
    TestCaseBatchCreate,
    TestCaseReorderRequest,
    TestCaseListOut,
    SubmissionCreate,
    SubmissionOut,
    SubmissionListOut,
    SubmissionListItemOut,
    CodeRunRequest,
    CodeRunResponse,
    TestCaseRunResultOut,
    MessageResponse,
    CodingMetricsOut,
    NormalizedPerformanceResultOut,
    TopicPerformanceOut,
    DifficultyBreakdownOut,
    WeakTopicOut,
    CodingHistoryItemOut,
    CodingProgressSummaryOut,
    RecommendationContextOut,
)
import app.modules.coding.services.test_case_service as tc_service
import app.modules.coding.services.submission_service as sub_service
import app.modules.coding.services.evaluation_service as eval_service
import app.modules.coding.services.performance_service as perf_service
from app.modules.coding.services.question_service import (
    create_question,
    get_questions,
    get_question_by_id_or_slug,
    get_question_by_id,
    get_topic_summary,
    get_difficulty_summary,
    get_random_question,
    update_question,
    delete_question,
    add_test_case,
    delete_test_case,
    get_all_topics,
)

router = APIRouter(prefix="/coding", tags=["Coding"])


async def get_optional_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    """Helper to detect authenticated user without raising 401 if unauthenticated."""
    token = request.cookies.get(settings.COOKIE_NAME)
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

    if not token:
        return None

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str = payload.get("sub")
        if not user_id_str:
            return None
        user_uuid = uuid.UUID(user_id_str)
        result = await db.execute(select(User).where(User.id == user_uuid))
        return result.scalar_one_or_none()
    except Exception:
        return None


# ============================================================================
# QUESTION RETRIEVAL & FILTERING
# ============================================================================

@router.get("/questions", response_model=QuestionListOut)
async def list_coding_questions(
    topic: Optional[str] = Query(None, description="Filter by topic (e.g. Arrays, Strings)"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty (Easy, Medium, Hard)"),
    search: Optional[str] = Query(None, description="Search keyword in title, topic, or description"),
    status: Optional[str] = Query(None, description="Filter by solve status (all, solved, unsolved)"),
    sort_by: str = Query("created_at", description="Field to sort by (created_at, title, difficulty)"),
    sort_order: str = Query("desc", description="Sort order direction (asc, desc)"),
    page: Optional[int] = Query(None, ge=1, description="1-indexed page number"),
    limit: int = Query(50, ge=1, le=100, description="Items per page (max 100)"),
    skip: Optional[int] = Query(None, ge=0, description="Offset (used if page is omitted)"),
    db: AsyncSession = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    """Retrieve paginated list of coding questions with comprehensive filtering, status check, and sorting."""
    user_id = user.id if user else None

    # Handle page vs skip pagination
    if page is not None:
        effective_skip = (page - 1) * limit
        current_page = page
    elif skip is not None:
        effective_skip = skip
        current_page = (skip // limit) + 1
    else:
        effective_skip = 0
        current_page = 1

    questions, total_count = await get_questions(
        db=db,
        user_id=user_id,
        topic=topic,
        difficulty=difficulty,
        search=search,
        status_filter=status,
        sort_by=sort_by,
        sort_order=sort_order,
        skip=effective_skip,
        limit=limit,
    )

    total_pages = max(1, math.ceil(total_count / limit)) if total_count > 0 else 1

    return {
        "total_count": total_count,
        "page": current_page,
        "limit": limit,
        "total_pages": total_pages,
        "questions": questions,
    }


@router.get("/questions/random", response_model=QuestionDetailOut)
async def get_random_coding_question(
    topic: Optional[str] = Query(None, description="Filter random selection by topic"),
    difficulty: Optional[str] = Query(None, description="Filter random selection by difficulty"),
    status: Optional[str] = Query(None, description="Filter random selection by status (all, solved, unsolved)"),
    db: AsyncSession = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    """Select a random question for practice, optionally filtered by topic, difficulty, or solve status."""
    user_id = user.id if user else None
    question_data = await get_random_question(
        db=db,
        user_id=user_id,
        topic=topic,
        difficulty=difficulty,
        status_filter=status,
    )
    if not question_data:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="No questions match the requested criteria.",
        )
    return question_data


@router.get("/questions/topics", response_model=List[str])
async def list_topics(db: AsyncSession = Depends(get_db)):
    """Retrieve distinct list of problem topics available in question bank."""
    return await get_all_topics(db)


@router.get("/questions/topics/summary", response_model=List[TopicSummaryOut])
async def list_topics_summary(db: AsyncSession = Depends(get_db)):
    """Retrieve topic breakdown with total questions and difficulty counts."""
    return await get_topic_summary(db)


@router.get("/questions/difficulties", response_model=List[str])
async def list_difficulties():
    """Retrieve standard difficulty tiers."""
    return ["Easy", "Medium", "Hard"]


@router.get("/questions/difficulties/summary", response_model=List[DifficultySummaryOut])
async def list_difficulties_summary(db: AsyncSession = Depends(get_db)):
    """Retrieve problem counts grouped by standard difficulty tiers."""
    return await get_difficulty_summary(db)


@router.get("/questions/id/{question_id}", response_model=QuestionDetailOut)
async def get_question_by_id_endpoint(
    question_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    """Retrieve question details explicitly by UUID."""
    user_id = user.id if user else None
    question_data = await get_question_by_id(
        db=db,
        question_id=question_id,
        user_id=user_id,
        include_hidden_test_cases=False,
    )
    if not question_data:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Coding question not found.",
        )
    return question_data


@router.get("/questions/{id_or_slug}", response_model=QuestionDetailOut)
async def get_question_details(
    id_or_slug: str,
    db: AsyncSession = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user),
):
    """
    Retrieve question details and sample test cases by UUID or slug.
    Hidden test cases are protected and never returned by this endpoint.
    """
    user_id = user.id if user else None
    question_data = await get_question_by_id_or_slug(
        db=db,
        id_or_slug=id_or_slug,
        user_id=user_id,
        include_hidden_test_cases=False,
    )
    if not question_data:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Coding question not found.",
        )
    return question_data


# ============================================================================
# QUESTION CRUD MANAGEMENT
# ============================================================================

@router.post(
    "/questions",
    response_model=QuestionDetailOut,
    status_code=http_status.HTTP_201_CREATED,
)
async def create_new_question(
    data: QuestionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new coding question with optional test cases."""
    question = await create_question(db, data)
    # Format for response
    sample_cases = [tc for tc in question.test_cases if tc.is_sample]
    return {
        "id": question.id,
        "title": question.title,
        "slug": question.slug,
        "description": question.description,
        "difficulty": question.difficulty,
        "topic": question.topic,
        "constraints": question.constraints,
        "hints": question.hints or [],
        "starter_code": question.starter_code or {},
        "sample_test_cases": sample_cases,
        "is_solved": False,
        "created_at": question.created_at,
        "updated_at": question.updated_at,
    }


@router.put(
    "/questions/{question_id}",
    response_model=QuestionDetailOut,
)
async def update_existing_question(
    question_id: uuid.UUID,
    data: QuestionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update question metadata, description, constraints, or starter code."""
    updated = await update_question(db, question_id, data)
    sample_cases = [tc for tc in updated.test_cases if tc.is_sample]
    return {
        "id": updated.id,
        "title": updated.title,
        "slug": updated.slug,
        "description": updated.description,
        "difficulty": updated.difficulty,
        "topic": updated.topic,
        "constraints": updated.constraints,
        "hints": updated.hints or [],
        "starter_code": updated.starter_code or {},
        "sample_test_cases": sample_cases,
        "is_solved": None,
        "created_at": updated.created_at,
        "updated_at": updated.updated_at,
    }


@router.delete(
    "/questions/{question_id}",
    response_model=MessageResponse,
)
async def delete_existing_question(
    question_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a coding question and all its test cases/submissions."""
    await delete_question(db, question_id)
    return {"message": "Coding question deleted successfully."}


# ============================================================================
# TEST CASE MANAGEMENT
# ============================================================================

@router.get(
    "/questions/{question_id}/test-cases",
    response_model=TestCaseListOut,
)
async def list_question_test_cases(
    question_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    List all test cases (both sample and hidden) for a problem.
    Requires authentication.
    """
    cases = await tc_service.get_test_cases_for_question(db, question_id, sample_only=False)
    sample_count = sum(1 for c in cases if c.is_sample)
    hidden_count = len(cases) - sample_count
    return {
        "total_count": len(cases),
        "sample_count": sample_count,
        "hidden_count": hidden_count,
        "test_cases": cases,
    }


@router.get(
    "/questions/{question_id}/test-cases/samples",
    response_model=List[TestCaseSampleOut],
)
async def list_sample_test_cases(
    question_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Public endpoint to list only the visible sample test cases for a question."""
    return await tc_service.get_test_cases_for_question(db, question_id, sample_only=True)


@router.get(
    "/test-cases/{test_case_id}",
    response_model=TestCaseOut,
)
async def get_test_case_details(
    test_case_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve full details of an individual test case."""
    return await tc_service.get_test_case_by_id(db, test_case_id)


@router.post(
    "/questions/{question_id}/test-cases",
    response_model=TestCaseOut,
    status_code=http_status.HTTP_201_CREATED,
)
async def add_question_test_case(
    question_id: uuid.UUID,
    data: TestCaseCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Attach a new test case (sample or hidden) to a question."""
    return await tc_service.create_single_test_case(db, question_id, data)


@router.post(
    "/questions/{question_id}/test-cases/batch",
    response_model=List[TestCaseOut],
    status_code=http_status.HTTP_201_CREATED,
)
async def add_batch_test_cases(
    question_id: uuid.UUID,
    payload: TestCaseBatchCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Bulk-add multiple test cases to a question."""
    return await tc_service.create_batch_test_cases(db, question_id, payload.test_cases)


@router.put(
    "/test-cases/{test_case_id}",
    response_model=TestCaseOut,
)
async def update_existing_test_case(
    test_case_id: uuid.UUID,
    data: TestCaseUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update test case inputs, outputs, sample flag, explanation, or order."""
    return await tc_service.update_test_case(db, test_case_id, data)


@router.put(
    "/questions/{question_id}/test-cases/reorder",
    response_model=List[TestCaseOut],
)
async def reorder_question_test_cases(
    question_id: uuid.UUID,
    payload: TestCaseReorderRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Reorder test cases for a question."""
    return await tc_service.reorder_test_cases(db, question_id, payload.items)


@router.delete(
    "/test-cases/{test_case_id}",
    response_model=MessageResponse,
)
async def delete_existing_test_case(
    test_case_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a test case by ID."""
    await tc_service.delete_test_case(db, test_case_id)
    return {"message": "Test case deleted successfully."}


# ============================================================================
# CODING SUBMISSIONS
# ============================================================================

@router.post(
    "/submissions",
    response_model=SubmissionOut,
    status_code=http_status.HTTP_201_CREATED,
)
async def submit_code(
    payload: SubmissionCreate,
    evaluate: bool = Query(False, description="Whether to immediately evaluate the code submission"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Submit code for a coding question.
    Validates question existence, user authentication, language, and non-empty code.
    Persists submission in 'pending' status. If evaluate is True, executes code sandbox.
    """
    sub_dict = await sub_service.create_submission(
        db=db,
        user_id=current_user.id,
        data=payload,
    )
    if evaluate:
        return await eval_service.evaluate_submission(
            db=db,
            submission_id=sub_dict["id"],
            user_id=current_user.id,
        )
    return sub_dict


@router.get(
    "/submissions",
    response_model=SubmissionListOut,
)
async def list_user_submissions(
    question_id: Optional[uuid.UUID] = Query(None, description="Filter submissions by question ID"),
    status: Optional[str] = Query(None, description="Filter submissions by status"),
    page: Optional[int] = Query(None, ge=1, description="1-indexed page number"),
    limit: int = Query(50, ge=1, le=100, description="Items per page"),
    skip: Optional[int] = Query(None, ge=0, description="Offset"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve paginated list of submissions submitted by the authenticated student."""
    if page is not None:
        effective_skip = (page - 1) * limit
        current_page = page
    elif skip is not None:
        effective_skip = skip
        current_page = (skip // limit) + 1
    else:
        effective_skip = 0
        current_page = 1

    items, total_count = await sub_service.get_user_submissions(
        db=db,
        user_id=current_user.id,
        question_id=question_id,
        status_filter=status,
        skip=effective_skip,
        limit=limit,
    )

    total_pages = max(1, math.ceil(total_count / limit)) if total_count > 0 else 1

    return {
        "total_count": total_count,
        "page": current_page,
        "limit": limit,
        "total_pages": total_pages,
        "submissions": items,
    }


@router.get(
    "/submissions/{submission_id}",
    response_model=SubmissionOut,
)
async def get_submission_details(
    submission_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve details of an individual submission.
    Enforces user isolation (students can only access their own submissions).
    """
    sub_data = await sub_service.get_submission_by_id(
        db=db,
        submission_id=submission_id,
        user_id=current_user.id,
    )
    if not sub_data:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Coding submission not found.",
        )
    return sub_data


@router.get(
    "/questions/{question_id}/submissions",
    response_model=SubmissionListOut,
)
async def list_question_submissions(
    question_id: uuid.UUID,
    page: Optional[int] = Query(None, ge=1, description="1-indexed page number"),
    limit: int = Query(50, ge=1, le=100, description="Items per page"),
    skip: Optional[int] = Query(None, ge=0, description="Offset"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve all submissions made by the authenticated student for a specific question."""
    if page is not None:
        effective_skip = (page - 1) * limit
        current_page = page
    elif skip is not None:
        effective_skip = skip
        current_page = (skip // limit) + 1
    else:
        effective_skip = 0
        current_page = 1

    items, total_count = await sub_service.get_user_submissions(
        db=db,
        user_id=current_user.id,
        question_id=question_id,
        skip=effective_skip,
        limit=limit,
    )

    total_pages = max(1, math.ceil(total_count / limit)) if total_count > 0 else 1

    return {
        "total_count": total_count,
        "page": current_page,
        "limit": limit,
        "total_pages": total_pages,
        "submissions": items,
    }


# ============================================================================
# CODE EXECUTION & EVALUATION
# ============================================================================

@router.post(
    "/submissions/{submission_id}/evaluate",
    response_model=SubmissionOut,
)
async def evaluate_existing_submission(
    submission_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Evaluate an existing submission in an isolated, secure execution environment.
    Runs the code against all test cases, saves verdicts and score to coding_results,
    and returns full evaluation results with hidden test case I/O redacted.
    Enforces user isolation (students can only evaluate their own submissions).
    """
    return await eval_service.evaluate_submission(
        db=db,
        submission_id=submission_id,
        user_id=current_user.id,
    )


@router.post(
    "/questions/{question_id}/run",
    response_model=CodeRunResponse,
)
async def run_code_sample(
    question_id: uuid.UUID,
    payload: CodeRunRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Interactive 'Run Code' endpoint.
    Executes student code in an isolated sandbox against ONLY sample test cases.
    Does NOT persist submission or result in database.
    """
    return await eval_service.run_sample_code(
        db=db,
        question_id=question_id,
        language=payload.language,
        code=payload.code,
    )


# ============================================================================
# SCORING & PERFORMANCE ANALYTICS
# ============================================================================

@router.get(
    "/submissions/{submission_id}/score",
    response_model=NormalizedPerformanceResultOut,
)
async def get_submission_score_performance(
    submission_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve normalized scoring and execution performance result for a single submission.
    Includes: submission_id, score, passed_tests, total_tests, topic, difficulty,
    execution_status, and coding_metrics.
    Enforces user isolation.
    """
    return await perf_service.get_normalized_submission_performance(
        db=db,
        submission_id=submission_id,
        user_id=current_user.id,
    )


@router.get(
    "/progress",
    response_model=CodingProgressSummaryOut,
)
@router.get(
    "/performance/progress",
    response_model=CodingProgressSummaryOut,
)
async def get_coding_progress_summary(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve comprehensive coding progress summary for the authenticated student.
    Includes overall question completion, solve rate, coding score, tier breakdown, and weak topics.
    """
    return await perf_service.get_student_coding_progress(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/performance/topics",
    response_model=List[TopicPerformanceOut],
)
async def get_student_topic_performance(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve topic-wise performance breakdown for the authenticated student.
    Calculates attempted/solved counts, accuracy, average score, and proficiency level per topic.
    """
    return await perf_service.get_topic_performance(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/performance/difficulties",
    response_model=List[DifficultyBreakdownOut],
)
async def get_student_difficulty_performance(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve difficulty-wise performance breakdown (Easy, Medium, Hard).
    Includes total available in bank, attempted count, solved count, solve rate, and average score.
    """
    return await perf_service.get_difficulty_performance(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/performance/weak-topics",
    response_model=List[WeakTopicOut],
)
async def get_student_weak_topics(
    threshold: float = Query(70.0, ge=0.0, le=100.0, description="Score threshold below which topic is flagged weak"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Identify student's weak problem areas requiring focused practice.
    Returns topics with accuracy or average score below threshold, ranked from weakest to strongest.
    """
    return await perf_service.get_weak_topics(
        db=db,
        user_id=current_user.id,
        threshold=threshold,
    )


@router.get(
    "/performance/history",
    response_model=List[CodingHistoryItemOut],
)
async def get_student_coding_history(
    limit: int = Query(50, ge=1, le=200, description="Max history items to return"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve chronological history of student's evaluated submissions and scores.
    """
    return await perf_service.get_coding_history(
        db=db,
        user_id=current_user.id,
        limit=limit,
    )


@router.get(
    "/performance/recommendation-context",
    response_model=RecommendationContextOut,
)
async def get_recommendation_engine_context(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Expose normalized coding profile consumed by the team's Recommendation Engine:
    coding_score, weak_topics, and difficulty_performance.
    """
    return await perf_service.get_recommendation_context(
        db=db,
        user_id=current_user.id,
    )


