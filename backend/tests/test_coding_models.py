import uuid
import pytest
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User
from app.db.models.coding import (
    CodingQuestion,
    CodingTestCase,
    CodingSubmission,
    CodingResult,
)


@pytest.mark.asyncio
async def test_coding_models_lifecycle_and_relationships(db_session: AsyncSession):
    # 1. Create a User
    user = User(
        email="test_coder@example.com",
        password_hash="fakehash123",
        full_name="Test Coder",
        role="student",
    )
    db_session.add(user)
    await db_session.flush()

    # 2. Create a CodingQuestion
    question = CodingQuestion(
        title="Two Sum",
        slug="two-sum",
        description="# Two Sum\nGiven an array of integers `nums`...",
        difficulty="Easy",
        topic="Arrays",
        constraints="2 <= nums.length <= 10^4",
        hints=["Use a hash map to look up complements in O(1) time."],
        starter_code={
            "python": "def two_sum(nums, target):\n    pass",
            "javascript": "function twoSum(nums, target) {\n}",
        },
    )
    db_session.add(question)
    await db_session.flush()

    assert question.id is not None
    assert question.slug == "two-sum"

    # 3. Add Test Cases (Sample + Hidden)
    tc_sample = CodingTestCase(
        question_id=question.id,
        input_data="[2, 7, 11, 15]\n9",
        expected_output="[0, 1]",
        is_sample=True,
        explanation="2 + 7 = 9",
        order_index=1,
    )
    tc_hidden = CodingTestCase(
        question_id=question.id,
        input_data="[3, 2, 4]\n6",
        expected_output="[1, 2]",
        is_sample=False,
        order_index=2,
    )
    db_session.add_all([tc_sample, tc_hidden])
    await db_session.commit()

    # Verify question test cases with selectinload
    result = await db_session.execute(
        select(CodingQuestion)
        .options(selectinload(CodingQuestion.test_cases))
        .where(CodingQuestion.id == question.id)
    )
    q_fetched = result.scalar_one()
    assert len(q_fetched.test_cases) == 2
    assert q_fetched.test_cases[0].is_sample is True
    assert q_fetched.test_cases[1].is_sample is False

    # 4. Create CodingSubmission
    submission = CodingSubmission(
        user_id=user.id,
        question_id=question.id,
        language="python",
        code="def two_sum(nums, target):\n    return [0, 1]",
        status="completed",
    )
    db_session.add(submission)
    await db_session.flush()

    assert submission.id is not None
    assert submission.user_id == user.id
    assert submission.question_id == question.id

    # 5. Create CodingResult
    coding_result = CodingResult(
        submission_id=submission.id,
        verdict="Accepted",
        score=100.0,
        passed_test_cases=2,
        total_test_cases=2,
        execution_time_ms=15.4,
        memory_kb=1024.0,
        test_case_results_json=[
            {"test_case_id": str(tc_sample.id), "passed": True},
            {"test_case_id": str(tc_hidden.id), "passed": True},
        ],
    )
    db_session.add(coding_result)
    await db_session.commit()

    # 6. Verify full query and relationships with selectinload
    sub_query = await db_session.execute(
        select(CodingSubmission)
        .options(
            selectinload(CodingSubmission.result),
            selectinload(CodingSubmission.question),
            selectinload(CodingSubmission.user),
        )
        .where(CodingSubmission.id == submission.id)
    )
    sub_fetched = sub_query.scalar_one()
    assert sub_fetched.result is not None
    assert sub_fetched.result.verdict == "Accepted"
    assert sub_fetched.result.score == 100.0
    assert sub_fetched.question.title == "Two Sum"
    assert sub_fetched.user.full_name == "Test Coder"

    # User relationship
    user_query = await db_session.execute(
        select(User)
        .options(selectinload(User.coding_submissions))
        .where(User.id == user.id)
    )
    user_fetched = user_query.scalar_one()
    assert len(user_fetched.coding_submissions) == 1

    # 7. Test Cascade Delete: deleting submission deletes result
    await db_session.delete(sub_fetched)
    await db_session.commit()

    res_check = await db_session.execute(
        select(CodingResult).where(CodingResult.submission_id == submission.id)
    )
    assert res_check.scalar_one_or_none() is None
