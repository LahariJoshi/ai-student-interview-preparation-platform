"""
seed_coding_questions.py - Idempotent database seeder for the Member-2 Coding Assessment module.

Usage:
    python backend/seed_coding_questions.py
"""

import sys
import os
import asyncio
import uuid
from typing import Dict, Any

# Ensure backend directory is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.core.database import AsyncSessionLocal, engine
from app.db.models.coding import CodingQuestion, CodingTestCase
from datasets.bank import get_all_questions, get_bank_summary


async def seed_questions_to_session(session, questions_data=None) -> Dict[str, Any]:
    """Seed or update questions and test cases in the given SQLAlchemy async session."""
    if questions_data is None:
        questions_data = get_all_questions()

    stmt = select(CodingQuestion).options(selectinload(CodingQuestion.test_cases))
    res = await session.execute(stmt)
    existing_questions = {q.slug: q for q in res.scalars().all()}

    inserted_q_count = 0
    updated_q_count = 0
    inserted_tc_count = 0

    for q_data in questions_data:
        slug = q_data["slug"]
        q_id = uuid.uuid5(uuid.NAMESPACE_DNS, slug)
        test_cases_data = q_data.get("test_cases", [])

        if slug in existing_questions:
            # Update existing question
            q_obj = existing_questions[slug]
            q_obj.title = q_data["title"]
            q_obj.description = q_data["description"]
            q_obj.difficulty = q_data["difficulty"]
            q_obj.topic = q_data["topic"]
            q_obj.constraints = q_data.get("constraints")
            q_obj.hints = q_data.get("hints", [])
            q_obj.starter_code = q_data.get("starter_code", {})
            updated_q_count += 1

            # Check if test cases exist
            existing_tc_inputs = {tc.input_data for tc in q_obj.test_cases}
            for idx, tc_data in enumerate(test_cases_data):
                if tc_data["input_data"] not in existing_tc_inputs:
                    tc_id = uuid.uuid5(q_obj.id, f"tc_{idx}_{tc_data['input_data'][:20]}")
                    new_tc = CodingTestCase(
                        id=tc_id,
                        question_id=q_obj.id,
                        input_data=tc_data["input_data"],
                        expected_output=tc_data["expected_output"],
                        is_sample=tc_data.get("is_sample", False),
                        explanation=tc_data.get("explanation"),
                        order_index=idx,
                    )
                    session.add(new_tc)
                    inserted_tc_count += 1
        else:
            # Insert new question
            q_obj = CodingQuestion(
                id=q_id,
                title=q_data["title"],
                slug=slug,
                description=q_data["description"],
                difficulty=q_data["difficulty"],
                topic=q_data["topic"],
                constraints=q_data.get("constraints"),
                hints=q_data.get("hints", []),
                starter_code=q_data.get("starter_code", {}),
            )
            session.add(q_obj)
            inserted_q_count += 1

            # Add test cases
            for idx, tc_data in enumerate(test_cases_data):
                tc_id = uuid.uuid5(q_id, f"tc_{idx}_{tc_data['input_data'][:20]}")
                new_tc = CodingTestCase(
                    id=tc_id,
                    question_id=q_id,
                    input_data=tc_data["input_data"],
                    expected_output=tc_data["expected_output"],
                    is_sample=tc_data.get("is_sample", False),
                    explanation=tc_data.get("explanation"),
                    order_index=idx,
                )
                session.add(new_tc)
                inserted_tc_count += 1

    await session.commit()

    q_count_res = await session.execute(select(func.count(CodingQuestion.id)))
    total_in_db = q_count_res.scalar()

    tc_count_res = await session.execute(select(func.count(CodingTestCase.id)))
    total_tc_in_db = tc_count_res.scalar()

    diff_stmt = select(CodingQuestion.difficulty, func.count(CodingQuestion.id)).group_by(CodingQuestion.difficulty)
    diff_res = await session.execute(diff_stmt)
    db_diffs = dict(diff_res.all())

    return {
        "total_questions": total_in_db,
        "total_test_cases": total_tc_in_db,
        "difficulty_breakdown": db_diffs,
        "inserted_questions": inserted_q_count,
        "updated_questions": updated_q_count,
        "inserted_test_cases": inserted_tc_count,
    }


async def seed_database() -> Dict[str, Any]:
    """Seed the PostgreSQL database with the complete 220+ question bank idempotently."""
    print("=" * 70)
    print("MEMBER-2: SEEDING CODING QUESTIONS & TEST CASES TO POSTGRESQL")
    print("=" * 70)

    bank_summary = get_bank_summary()
    print(f"Loaded {bank_summary['total_questions']} questions from bank modules.")
    print(f"Distribution: {bank_summary['difficulty_counts']}")
    print(f"Total test cases to verify/seed: {bank_summary['total_test_cases']}\n")

    async with AsyncSessionLocal() as session:
        summary = await seed_questions_to_session(session)

    print(f"\n[SUCCESS] Seed transaction committed.")
    print(f" - Inserted questions: {summary['inserted_questions']}")
    print(f" - Updated questions:  {summary['updated_questions']}")
    print(f" - Inserted test cases: {summary['inserted_test_cases']}")

    print("\n" + "=" * 70)
    print("DATABASE VERIFICATION SUMMARY:")
    print(f"Total Questions in DB:  {summary['total_questions']}")
    print(f"Total Test Cases in DB: {summary['total_test_cases']}")
    print(f"Difficulty Breakdown:   {summary['difficulty_breakdown']}")
    print("=" * 70)

    return summary


if __name__ == "__main__":
    result = asyncio.run(seed_database())
