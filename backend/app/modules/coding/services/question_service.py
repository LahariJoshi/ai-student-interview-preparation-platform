import re
import uuid
from typing import Optional, List, Tuple, Dict, Any
from sqlalchemy import select, func, distinct, and_, or_, case
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.db.models.coding import (
    CodingQuestion,
    CodingTestCase,
    CodingSubmission,
    CodingResult,
)
from app.modules.coding.schemas import (
    QuestionCreate,
    QuestionUpdate,
    TestCaseCreate,
    ALLOWED_DIFFICULTIES,
    ALLOWED_STATUSES,
    ALLOWED_SORT_FIELDS,
    ALLOWED_SORT_ORDERS,
)


def slugify(text: str) -> str:
    """Generate a clean URL-friendly slug from text."""
    slug = text.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_-]+", "-", slug)
    slug = slug.strip("-")
    return slug or "coding-question"


async def create_question(
    db: AsyncSession,
    data: QuestionCreate,
) -> CodingQuestion:
    """Create a new coding question with optional test cases."""
    slug_val = data.slug or slugify(data.title)

    # Check for slug collision
    existing = await db.execute(
        select(CodingQuestion).where(CodingQuestion.slug == slug_val)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A question with the slug '{slug_val}' already exists.",
        )

    question = CodingQuestion(
        id=uuid.uuid4(),
        title=data.title,
        slug=slug_val,
        description=data.description,
        difficulty=data.difficulty,
        topic=data.topic,
        constraints=data.constraints,
        hints=data.hints or [],
        starter_code=data.starter_code or {},
    )
    db.add(question)
    await db.flush()

    # Add associated test cases if provided
    if data.test_cases:
        for idx, tc in enumerate(data.test_cases):
            test_case = CodingTestCase(
                id=uuid.uuid4(),
                question_id=question.id,
                input_data=tc.input_data,
                expected_output=tc.expected_output,
                is_sample=tc.is_sample,
                explanation=tc.explanation,
                order_index=tc.order_index if tc.order_index != 0 else idx + 1,
            )
            db.add(test_case)

    await db.commit()

    # Reload with test cases eager loaded
    result = await db.execute(
        select(CodingQuestion)
        .options(selectinload(CodingQuestion.test_cases))
        .where(CodingQuestion.id == question.id)
    )
    return result.scalar_one()


async def get_questions(
    db: AsyncSession,
    user_id: Optional[uuid.UUID] = None,
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    search: Optional[str] = None,
    status_filter: Optional[str] = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    skip: int = 0,
    limit: int = 50,
) -> Tuple[List[Dict[str, Any]], int]:
    """
    Retrieve questions with optional filtering (topic, difficulty, search keyword,
    solved/unsolved status), sorting, pagination, sample test case count,
    and authenticated user solve status.
    """
    stmt = select(CodingQuestion)
    count_stmt = select(func.count(distinct(CodingQuestion.id)))

    filters = []
    if topic:
        filters.append(func.lower(CodingQuestion.topic) == topic.lower().strip())

    if difficulty:
        formatted_diff = difficulty.strip().capitalize()
        if formatted_diff not in ALLOWED_DIFFICULTIES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid difficulty: '{difficulty}'. Allowed values are: {', '.join(sorted(ALLOWED_DIFFICULTIES))}.",
            )
        filters.append(CodingQuestion.difficulty == formatted_diff)

    if search:
        term = f"%{search.strip()}%"
        filters.append(
            or_(
                CodingQuestion.title.ilike(term),
                CodingQuestion.description.ilike(term),
                CodingQuestion.topic.ilike(term),
            )
        )

    if status_filter:
        status_clean = status_filter.strip().lower()
        if status_clean not in ALLOWED_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status filter: '{status_filter}'. Allowed values are: {', '.join(sorted(ALLOWED_STATUSES))}.",
            )
        if status_clean in {"solved", "unsolved"}:
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required to filter questions by solved/unsolved status.",
                )
            solved_subq = (
                select(CodingSubmission.question_id)
                .join(CodingResult, CodingSubmission.id == CodingResult.submission_id)
                .where(
                    and_(
                        CodingSubmission.user_id == user_id,
                        CodingResult.verdict == "Accepted",
                    )
                )
            )
            if status_clean == "solved":
                filters.append(CodingQuestion.id.in_(solved_subq))
            elif status_clean == "unsolved":
                filters.append(~CodingQuestion.id.in_(solved_subq))

    if filters:
        stmt = stmt.where(and_(*filters))
        count_stmt = count_stmt.where(and_(*filters))

    # Total matching count
    total_res = await db.execute(count_stmt)
    total_count = total_res.scalar_one()

    # Sorting
    sort_clean = (sort_by or "created_at").strip().lower()
    order_clean = (sort_order or "desc").strip().lower()
    if sort_clean not in ALLOWED_SORT_FIELDS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid sort_by: '{sort_by}'. Allowed fields are: {', '.join(sorted(ALLOWED_SORT_FIELDS))}.",
        )
    if order_clean not in ALLOWED_SORT_ORDERS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid sort_order: '{sort_order}'. Allowed values are: {', '.join(sorted(ALLOWED_SORT_ORDERS))}.",
        )

    if sort_clean == "title":
        col = CodingQuestion.title.asc() if order_clean == "asc" else CodingQuestion.title.desc()
        stmt = stmt.order_by(col, CodingQuestion.id.asc())
    elif sort_clean == "difficulty":
        diff_case = case(
            (CodingQuestion.difficulty == "Easy", 1),
            (CodingQuestion.difficulty == "Medium", 2),
            (CodingQuestion.difficulty == "Hard", 3),
            else_=4,
        )
        col = diff_case.asc() if order_clean == "asc" else diff_case.desc()
        stmt = stmt.order_by(col, CodingQuestion.created_at.desc(), CodingQuestion.id.asc())
    else:
        col = CodingQuestion.created_at.asc() if order_clean == "asc" else CodingQuestion.created_at.desc()
        stmt = stmt.order_by(col, CodingQuestion.id.asc())

    stmt = (
        stmt.options(selectinload(CodingQuestion.test_cases))
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    questions = result.scalars().all()

    # Solved questions for authenticated user
    solved_question_ids = set()
    if user_id and questions:
        q_ids = [q.id for q in questions]
        solved_query = (
            select(CodingSubmission.question_id)
            .join(CodingResult, CodingSubmission.id == CodingResult.submission_id)
            .where(
                and_(
                    CodingSubmission.user_id == user_id,
                    CodingSubmission.question_id.in_(q_ids),
                    CodingResult.verdict == "Accepted",
                )
            )
        )
        solved_res = await db.execute(solved_query)
        solved_question_ids = set(solved_res.scalars().all())

    formatted_items = []
    for q in questions:
        sample_count = sum(1 for tc in q.test_cases if tc.is_sample)
        formatted_items.append(
            {
                "id": q.id,
                "title": q.title,
                "slug": q.slug,
                "difficulty": q.difficulty,
                "topic": q.topic,
                "sample_test_case_count": sample_count,
                "is_solved": (q.id in solved_question_ids) if user_id else None,
                "created_at": q.created_at,
            }
        )

    return formatted_items, total_count


async def get_question_by_id_or_slug(
    db: AsyncSession,
    id_or_slug: str,
    user_id: Optional[uuid.UUID] = None,
    include_hidden_test_cases: bool = False,
) -> Optional[Dict[str, Any]]:
    """
    Retrieve question details.
    By default, hides non-sample test cases for students/public.
    """
    stmt = select(CodingQuestion).options(selectinload(CodingQuestion.test_cases))

    try:
        q_uuid = uuid.UUID(id_or_slug)
        stmt = stmt.where(CodingQuestion.id == q_uuid)
    except ValueError:
        stmt = stmt.where(CodingQuestion.slug == id_or_slug.strip().lower())

    result = await db.execute(stmt)
    question = result.scalar_one_or_none()

    if not question:
        return None

    # Check solved status
    is_solved = None
    if user_id:
        solved_check = await db.execute(
            select(CodingSubmission.id)
            .join(CodingResult, CodingSubmission.id == CodingResult.submission_id)
            .where(
                and_(
                    CodingSubmission.user_id == user_id,
                    CodingSubmission.question_id == question.id,
                    CodingResult.verdict == "Accepted",
                )
            )
            .limit(1)
        )
        is_solved = solved_check.scalar_one_or_none() is not None

    # Separate sample test cases
    sample_cases = [tc for tc in question.test_cases if tc.is_sample]

    data = {
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
        "is_solved": is_solved,
        "created_at": question.created_at,
        "updated_at": question.updated_at,
    }

    if include_hidden_test_cases:
        data["all_test_cases"] = question.test_cases

    return data


async def update_question(
    db: AsyncSession,
    question_id: uuid.UUID,
    data: QuestionUpdate,
) -> CodingQuestion:
    """Update question attributes."""
    result = await db.execute(
        select(CodingQuestion)
        .options(selectinload(CodingQuestion.test_cases))
        .where(CodingQuestion.id == question_id)
    )
    question = result.scalar_one_or_none()

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coding question not found.",
        )

    # Check slug collision if slug is updated
    if data.slug and data.slug != question.slug:
        clean_slug = slugify(data.slug)
        existing = await db.execute(
            select(CodingQuestion).where(
                and_(
                    CodingQuestion.slug == clean_slug,
                    CodingQuestion.id != question_id,
                )
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Slug '{clean_slug}' is already taken by another question.",
            )
        question.slug = clean_slug

    update_dict = data.model_dump(exclude_unset=True, exclude={"slug"})
    for field, val in update_dict.items():
        setattr(question, field, val)

    await db.commit()
    await db.refresh(question)
    return question


async def delete_question(
    db: AsyncSession,
    question_id: uuid.UUID,
) -> bool:
    """Delete a coding question and all cascade-related data."""
    result = await db.execute(
        select(CodingQuestion).where(CodingQuestion.id == question_id)
    )
    question = result.scalar_one_or_none()

    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coding question not found.",
        )

    await db.delete(question)
    await db.commit()
    return True


async def add_test_case(
    db: AsyncSession,
    question_id: uuid.UUID,
    data: TestCaseCreate,
) -> CodingTestCase:
    """Attach a test case to an existing question."""
    q_res = await db.execute(
        select(CodingQuestion.id).where(CodingQuestion.id == question_id)
    )
    if not q_res.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coding question not found.",
        )

    test_case = CodingTestCase(
        id=uuid.uuid4(),
        question_id=question_id,
        input_data=data.input_data,
        expected_output=data.expected_output,
        is_sample=data.is_sample,
        explanation=data.explanation,
        order_index=data.order_index,
    )
    db.add(test_case)
    await db.commit()
    await db.refresh(test_case)
    return test_case


async def delete_test_case(
    db: AsyncSession,
    test_case_id: uuid.UUID,
) -> bool:
    """Delete a specific test case."""
    result = await db.execute(
        select(CodingTestCase).where(CodingTestCase.id == test_case_id)
    )
    test_case = result.scalar_one_or_none()

    if not test_case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test case not found.",
        )

    await db.delete(test_case)
    await db.commit()
    return True


async def get_all_topics(db: AsyncSession) -> List[str]:
    """Retrieve all unique topics currently in the database."""
    result = await db.execute(
        select(distinct(CodingQuestion.topic)).order_by(CodingQuestion.topic)
    )
    return [row[0] for row in result.all() if row[0]]


async def get_question_by_id(
    db: AsyncSession,
    question_id: uuid.UUID,
    user_id: Optional[uuid.UUID] = None,
    include_hidden_test_cases: bool = False,
) -> Optional[Dict[str, Any]]:
    """Retrieve question details by UUID."""
    return await get_question_by_id_or_slug(
        db=db,
        id_or_slug=str(question_id),
        user_id=user_id,
        include_hidden_test_cases=include_hidden_test_cases,
    )


async def get_topic_summary(db: AsyncSession) -> List[Dict[str, Any]]:
    """
    Retrieve all topics with question counts and difficulty breakdown
    (easy, medium, hard).
    """
    stmt = (
        select(
            CodingQuestion.topic,
            func.count(CodingQuestion.id).label("question_count"),
            func.sum(case((CodingQuestion.difficulty == "Easy", 1), else_=0)).label("easy_count"),
            func.sum(case((CodingQuestion.difficulty == "Medium", 1), else_=0)).label("medium_count"),
            func.sum(case((CodingQuestion.difficulty == "Hard", 1), else_=0)).label("hard_count"),
        )
        .group_by(CodingQuestion.topic)
        .order_by(CodingQuestion.topic.asc())
    )
    result = await db.execute(stmt)
    rows = result.all()
    return [
        {
            "topic": row.topic,
            "question_count": int(row.question_count),
            "easy_count": int(row.easy_count or 0),
            "medium_count": int(row.medium_count or 0),
            "hard_count": int(row.hard_count or 0),
        }
        for row in rows
    ]


async def get_difficulty_summary(db: AsyncSession) -> List[Dict[str, Any]]:
    """Retrieve question counts grouped by standard difficulty tiers."""
    stmt = (
        select(
            CodingQuestion.difficulty,
            func.count(CodingQuestion.id).label("question_count"),
        )
        .group_by(CodingQuestion.difficulty)
    )
    result = await db.execute(stmt)
    counts = {row.difficulty.capitalize(): int(row.question_count) for row in result.all() if row.difficulty}
    return [
        {"difficulty": diff, "question_count": counts.get(diff, 0)}
        for diff in ["Easy", "Medium", "Hard"]
    ]


async def get_random_question(
    db: AsyncSession,
    user_id: Optional[uuid.UUID] = None,
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    status_filter: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Select a random coding question matching optional topic, difficulty,
    and student solve status filters.
    """
    stmt = select(CodingQuestion).options(selectinload(CodingQuestion.test_cases))
    filters = []

    if topic:
        filters.append(func.lower(CodingQuestion.topic) == topic.lower().strip())

    if difficulty:
        formatted_diff = difficulty.strip().capitalize()
        if formatted_diff not in ALLOWED_DIFFICULTIES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid difficulty: '{difficulty}'. Allowed values are: {', '.join(sorted(ALLOWED_DIFFICULTIES))}.",
            )
        filters.append(CodingQuestion.difficulty == formatted_diff)

    if status_filter:
        status_clean = status_filter.strip().lower()
        if status_clean not in ALLOWED_STATUSES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid status filter: '{status_filter}'. Allowed values are: {', '.join(sorted(ALLOWED_STATUSES))}.",
            )
        if status_clean in {"solved", "unsolved"}:
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required to filter random question by solved/unsolved status.",
                )
            solved_subq = (
                select(CodingSubmission.question_id)
                .join(CodingResult, CodingSubmission.id == CodingResult.submission_id)
                .where(
                    and_(
                        CodingSubmission.user_id == user_id,
                        CodingResult.verdict == "Accepted",
                    )
                )
            )
            if status_clean == "solved":
                filters.append(CodingQuestion.id.in_(solved_subq))
            elif status_clean == "unsolved":
                filters.append(~CodingQuestion.id.in_(solved_subq))

    if filters:
        stmt = stmt.where(and_(*filters))

    stmt = stmt.order_by(func.random()).limit(1)
    res = await db.execute(stmt)
    question = res.scalar_one_or_none()

    if not question:
        return None

    # Check solved status
    is_solved = None
    if user_id:
        solved_check = await db.execute(
            select(CodingSubmission.id)
            .join(CodingResult, CodingSubmission.id == CodingResult.submission_id)
            .where(
                and_(
                    CodingSubmission.user_id == user_id,
                    CodingSubmission.question_id == question.id,
                    CodingResult.verdict == "Accepted",
                )
            )
            .limit(1)
        )
        is_solved = solved_check.scalar_one_or_none() is not None

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
        "is_solved": is_solved,
        "created_at": question.created_at,
        "updated_at": question.updated_at,
    }
