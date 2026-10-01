import uuid
from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy import select, func, distinct, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.db.models.coding import (
    CodingQuestion,
    CodingSubmission,
    CodingResult,
)
from app.modules.coding.schemas import (
    SubmissionCreate,
    ALLOWED_SUBMISSION_STATUSES,
)


def format_submission_dict(submission: CodingSubmission) -> Dict[str, Any]:
    """Helper to convert a CodingSubmission model to an API-friendly dictionary."""
    question = submission.question
    result = submission.result

    result_data = None
    if result:
        result_data = {
            "id": result.id,
            "verdict": result.verdict,
            "score": result.score,
            "passed_test_cases": result.passed_test_cases,
            "total_test_cases": result.total_test_cases,
            "execution_time_ms": result.execution_time_ms,
            "memory_kb": result.memory_kb,
            "error_message": result.error_message,
            "test_case_results": result.test_case_results_json,
        }

    return {
        "id": submission.id,
        "user_id": submission.user_id,
        "question_id": submission.question_id,
        "language": submission.language,
        "code": submission.code,
        "status": submission.status,
        "created_at": submission.created_at,
        "question_title": question.title if question else None,
        "question_slug": question.slug if question else None,
        "question_difficulty": question.difficulty if question else None,
        "question_topic": question.topic if question else None,
        "result": result_data,
    }


def format_submission_list_item(submission: CodingSubmission) -> Dict[str, Any]:
    """Helper to convert a CodingSubmission model to a list-friendly summary dictionary."""
    question = submission.question
    result = submission.result

    return {
        "id": submission.id,
        "user_id": submission.user_id,
        "question_id": submission.question_id,
        "language": submission.language,
        "status": submission.status,
        "created_at": submission.created_at,
        "question_title": question.title if question else None,
        "question_slug": question.slug if question else None,
        "question_difficulty": question.difficulty if question else None,
        "question_topic": question.topic if question else None,
        "score": result.score if result else None,
        "verdict": result.verdict if result else None,
        "passed_test_cases": result.passed_test_cases if result else None,
        "total_test_cases": result.total_test_cases if result else None,
    }


async def create_submission(
    db: AsyncSession,
    user_id: uuid.UUID,
    data: SubmissionCreate,
) -> Dict[str, Any]:
    """
    Validate question existence, create a new submission in 'pending' status,
    and persist to database.
    """
    # 1. Verify question exists
    q_stmt = select(CodingQuestion).where(CodingQuestion.id == data.question_id)
    q_res = await db.execute(q_stmt)
    question = q_res.scalar_one_or_none()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coding question not found.",
        )

    # 2. Create submission record
    submission = CodingSubmission(
        id=uuid.uuid4(),
        user_id=user_id,
        question_id=data.question_id,
        language=data.language.strip().lower(),
        code=data.code,
        status="pending",
    )
    db.add(submission)
    await db.commit()

    # 3. Reload with question relationship eager loaded
    stmt = (
        select(CodingSubmission)
        .options(
            selectinload(CodingSubmission.question),
            selectinload(CodingSubmission.result),
        )
        .where(CodingSubmission.id == submission.id)
    )
    result = await db.execute(stmt)
    loaded_submission = result.scalar_one()

    return format_submission_dict(loaded_submission)


async def get_submission_by_id(
    db: AsyncSession,
    submission_id: uuid.UUID,
    user_id: Optional[uuid.UUID] = None,
) -> Optional[Dict[str, Any]]:
    """
    Retrieve submission by ID with strict user isolation.
    Returns None if submission not found or user is not authorized.
    """
    stmt = (
        select(CodingSubmission)
        .options(
            selectinload(CodingSubmission.question),
            selectinload(CodingSubmission.result),
        )
        .where(CodingSubmission.id == submission_id)
    )
    result = await db.execute(stmt)
    submission = result.scalar_one_or_none()

    if not submission:
        return None

    # User isolation check
    if user_id and submission.user_id != user_id:
        return None

    return format_submission_dict(submission)


async def get_user_submissions(
    db: AsyncSession,
    user_id: uuid.UUID,
    question_id: Optional[uuid.UUID] = None,
    status_filter: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
) -> Tuple[List[Dict[str, Any]], int]:
    """Retrieve paginated list of submissions belonging to a specific student."""
    stmt = (
        select(CodingSubmission)
        .options(
            selectinload(CodingSubmission.question),
            selectinload(CodingSubmission.result),
        )
        .where(CodingSubmission.user_id == user_id)
    )
    count_stmt = select(func.count(distinct(CodingSubmission.id))).where(
        CodingSubmission.user_id == user_id
    )

    filters = []
    if question_id:
        filters.append(CodingSubmission.question_id == question_id)

    if status_filter:
        clean_status = status_filter.strip().lower()
        if clean_status not in ALLOWED_SUBMISSION_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status filter: '{status_filter}'. Allowed values are: {', '.join(sorted(ALLOWED_SUBMISSION_STATUSES))}.",
            )
        filters.append(CodingSubmission.status == clean_status)

    if filters:
        stmt = stmt.where(and_(*filters))
        count_stmt = count_stmt.where(and_(*filters))

    # Total count
    total_res = await db.execute(count_stmt)
    total_count = total_res.scalar_one()

    # Paginated items
    stmt = stmt.order_by(CodingSubmission.created_at.desc()).offset(skip).limit(limit)
    res = await db.execute(stmt)
    submissions = res.scalars().all()

    formatted_items = [format_submission_list_item(sub) for sub in submissions]
    return formatted_items, total_count


async def update_submission_status(
    db: AsyncSession,
    submission_id: uuid.UUID,
    new_status: str,
) -> CodingSubmission:
    """
    Update submission execution lifecycle status (pending -> running -> completed/failed).
    Prepared for code execution and evaluation pipeline.
    """
    clean_status = new_status.strip().lower()
    if clean_status not in ALLOWED_SUBMISSION_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid submission status: '{new_status}'. Allowed statuses: {', '.join(sorted(ALLOWED_SUBMISSION_STATUSES))}.",
        )

    stmt = select(CodingSubmission).where(CodingSubmission.id == submission_id)
    res = await db.execute(stmt)
    submission = res.scalar_one_or_none()
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coding submission not found.",
        )

    submission.status = clean_status
    await db.commit()
    await db.refresh(submission)
    return submission
