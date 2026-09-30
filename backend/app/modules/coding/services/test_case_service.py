import uuid
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.db.models.coding import CodingQuestion, CodingTestCase
from app.modules.coding.schemas import (
    TestCaseCreate,
    TestCaseUpdate,
    TestCaseReorderItem,
)


def normalize_io_text(text: str) -> str:
    """Normalize line endings and whitespace for cross-platform execution compatibility."""
    if not text:
        return ""
    # Normalize CRLF to LF and strip trailing line whitespace
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return normalized.strip()


async def get_test_cases_for_question(
    db: AsyncSession,
    question_id: uuid.UUID,
    sample_only: bool = False,
) -> List[CodingTestCase]:
    """Retrieve test cases for a question ordered by order_index."""
    # Verify question exists
    q_check = await db.execute(
        select(CodingQuestion.id).where(CodingQuestion.id == question_id)
    )
    if not q_check.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coding question not found.",
        )

    stmt = select(CodingTestCase).where(CodingTestCase.question_id == question_id)
    if sample_only:
        stmt = stmt.where(CodingTestCase.is_sample == True)

    stmt = stmt.order_by(CodingTestCase.order_index, CodingTestCase.created_at)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_test_case_by_id(
    db: AsyncSession,
    test_case_id: uuid.UUID,
) -> CodingTestCase:
    """Retrieve an individual test case by ID."""
    result = await db.execute(
        select(CodingTestCase).where(CodingTestCase.id == test_case_id)
    )
    test_case = result.scalar_one_or_none()
    if not test_case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test case not found.",
        )
    return test_case


async def create_single_test_case(
    db: AsyncSession,
    question_id: uuid.UUID,
    data: TestCaseCreate,
) -> CodingTestCase:
    """Create a single test case associated with a question."""
    q_check = await db.execute(
        select(CodingQuestion.id).where(CodingQuestion.id == question_id)
    )
    if not q_check.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coding question not found.",
        )

    # Determine order index if 0
    order_idx = data.order_index
    if order_idx == 0:
        count_res = await db.execute(
            select(func.count(CodingTestCase.id)).where(
                CodingTestCase.question_id == question_id
            )
        )
        order_idx = count_res.scalar_one() + 1

    test_case = CodingTestCase(
        id=uuid.uuid4(),
        question_id=question_id,
        input_data=normalize_io_text(data.input_data),
        expected_output=normalize_io_text(data.expected_output),
        is_sample=data.is_sample,
        explanation=data.explanation,
        order_index=order_idx,
    )
    db.add(test_case)
    await db.commit()
    await db.refresh(test_case)
    return test_case


async def create_batch_test_cases(
    db: AsyncSession,
    question_id: uuid.UUID,
    items: List[TestCaseCreate],
) -> List[CodingTestCase]:
    """Bulk-add test cases to a question."""
    q_check = await db.execute(
        select(CodingQuestion.id).where(CodingQuestion.id == question_id)
    )
    if not q_check.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coding question not found.",
        )

    # Get current count for sequential indexing
    count_res = await db.execute(
        select(func.count(CodingTestCase.id)).where(
            CodingTestCase.question_id == question_id
        )
    )
    current_count = count_res.scalar_one()

    created_cases = []
    for idx, item in enumerate(items):
        order_idx = item.order_index if item.order_index != 0 else current_count + idx + 1
        tc = CodingTestCase(
            id=uuid.uuid4(),
            question_id=question_id,
            input_data=normalize_io_text(item.input_data),
            expected_output=normalize_io_text(item.expected_output),
            is_sample=item.is_sample,
            explanation=item.explanation,
            order_index=order_idx,
        )
        db.add(tc)
        created_cases.append(tc)

    await db.commit()
    for tc in created_cases:
        await db.refresh(tc)
    return created_cases


async def update_test_case(
    db: AsyncSession,
    test_case_id: uuid.UUID,
    data: TestCaseUpdate,
) -> CodingTestCase:
    """Update existing test case attributes."""
    test_case = await get_test_case_by_id(db, test_case_id)

    update_dict = data.model_dump(exclude_unset=True)
    if "input_data" in update_dict and update_dict["input_data"] is not None:
        update_dict["input_data"] = normalize_io_text(update_dict["input_data"])
    if "expected_output" in update_dict and update_dict["expected_output"] is not None:
        update_dict["expected_output"] = normalize_io_text(update_dict["expected_output"])

    for field, val in update_dict.items():
        setattr(test_case, field, val)

    await db.commit()
    await db.refresh(test_case)
    return test_case


async def delete_test_case(
    db: AsyncSession,
    test_case_id: uuid.UUID,
) -> bool:
    """Delete a test case by ID."""
    test_case = await get_test_case_by_id(db, test_case_id)
    await db.delete(test_case)
    await db.commit()
    return True


async def reorder_test_cases(
    db: AsyncSession,
    question_id: uuid.UUID,
    reorder_items: List[TestCaseReorderItem],
) -> List[CodingTestCase]:
    """Update order_index across multiple test cases of a question."""
    q_check = await db.execute(
        select(CodingQuestion.id).where(CodingQuestion.id == question_id)
    )
    if not q_check.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coding question not found.",
        )

    # Fetch test cases belonging to this question
    tc_ids = [item.id for item in reorder_items]
    result = await db.execute(
        select(CodingTestCase).where(
            and_(
                CodingTestCase.question_id == question_id,
                CodingTestCase.id.in_(tc_ids),
            )
        )
    )
    cases_by_id = {tc.id: tc for tc in result.scalars().all()}

    for item in reorder_items:
        if item.id in cases_by_id:
            cases_by_id[item.id].order_index = item.order_index

    await db.commit()
    return await get_test_cases_for_question(db, question_id, sample_only=False)
