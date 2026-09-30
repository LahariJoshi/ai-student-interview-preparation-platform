import uuid
from typing import Optional, List, Dict, Any
from sqlalchemy import select, func, distinct, and_, case
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status as http_status

from app.db.models.coding import (
    CodingQuestion,
    CodingSubmission,
    CodingResult,
)


# ============================================================================
# SCORING ENGINE
# ============================================================================

def compute_submission_score(
    passed_tests: int,
    total_tests: int,
    verdict: Optional[str] = None,
) -> float:
    """
    Calculate normalized score between 0.0 and 100.0 from passed/total test cases.
    Safely handles edge cases like zero total test cases or error verdicts.
    """
    if total_tests <= 0:
        return 0.0

    if passed_tests < 0:
        passed_tests = 0

    if passed_tests > total_tests:
        passed_tests = total_tests

    raw_score = (passed_tests / total_tests) * 100.0
    return round(raw_score, 1)


def get_proficiency_label(solved: int, attempted: int, avg_score: float) -> str:
    """Helper to classify proficiency level based on problem completion and average score."""
    if attempted == 0:
        return "Not Started"
    if solved == 0 or avg_score < 40.0:
        return "Needs Practice"
    if avg_score < 70.0:
        return "Developing"
    if avg_score < 90.0:
        return "Proficient"
    return "Mastered"


# ============================================================================
# INDIVIDUAL SUBMISSION PERFORMANCE RESULT
# ============================================================================

async def get_normalized_submission_performance(
    db: AsyncSession,
    submission_id: uuid.UUID,
    user_id: uuid.UUID,
) -> Dict[str, Any]:
    """
    Return normalized coding performance result for an individual submission:
    submission_id, score, passed_tests, total_tests, topic, difficulty, execution_status, coding_metrics.
    Enforces user isolation.
    """
    stmt = (
        select(CodingSubmission)
        .options(
            selectinload(CodingSubmission.question),
            selectinload(CodingSubmission.result),
        )
        .where(CodingSubmission.id == submission_id)
    )
    res = await db.execute(stmt)
    submission = res.scalar_one_or_none()

    if not submission:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail="Coding submission not found.",
        )

    if submission.user_id != user_id:
        raise HTTPException(
            status_code=http_status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You can only view your own submission performance.",
        )

    question = submission.question
    result = submission.result

    score = result.score if result else 0.0
    passed_tests = result.passed_test_cases if result else 0
    total_tests = result.total_test_cases if result else 0
    execution_status = result.verdict if result else submission.status
    exec_time = result.execution_time_ms if result else 0.0
    mem_kb = result.memory_kb if result else 12400.0

    return {
        "submission_id": submission.id,
        "score": score,
        "passed_tests": passed_tests,
        "total_tests": total_tests,
        "topic": question.topic if question else "General",
        "difficulty": question.difficulty if question else "Medium",
        "execution_status": execution_status,
        "coding_metrics": {
            "execution_time_ms": exec_time or 0.0,
            "memory_kb": mem_kb or 12400.0,
        },
    }


# ============================================================================
# TOPIC-WISE PERFORMANCE
# ============================================================================

async def get_topic_performance(
    db: AsyncSession,
    user_id: uuid.UUID,
) -> List[Dict[str, Any]]:
    """
    Compute performance breakdown per topic for the authenticated student.
    Includes: questions_attempted, questions_solved, total_submissions,
    accuracy_percentage, average_score, and proficiency_level.
    """
    # 1. Fetch all distinct topics available in question bank
    topics_stmt = select(distinct(CodingQuestion.topic)).order_by(CodingQuestion.topic.asc())
    topics_res = await db.execute(topics_stmt)
    all_topics = [t[0] for t in topics_res.all() if t[0]]

    # 2. Fetch all user submissions with questions and results
    sub_stmt = (
        select(
            CodingQuestion.topic,
            CodingQuestion.id.label("question_id"),
            CodingResult.verdict,
            CodingResult.score,
        )
        .select_from(CodingSubmission)
        .join(CodingQuestion, CodingSubmission.question_id == CodingQuestion.id)
        .join(CodingResult, CodingSubmission.id == CodingResult.submission_id)
        .where(CodingSubmission.user_id == user_id)
    )
    sub_res = await db.execute(sub_stmt)
    rows = sub_res.all()

    # Aggregate by topic
    topic_data: Dict[str, Dict[str, Any]] = {
        t: {
            "attempted_questions": set(),
            "solved_questions": set(),
            "total_submissions": 0,
            "accepted_submissions": 0,
            "scores": [],
        }
        for t in all_topics
    }

    for topic, q_id, verdict, score in rows:
        if topic not in topic_data:
            topic_data[topic] = {
                "attempted_questions": set(),
                "solved_questions": set(),
                "total_submissions": 0,
                "accepted_submissions": 0,
                "scores": [],
            }
        topic_data[topic]["attempted_questions"].add(q_id)
        topic_data[topic]["total_submissions"] += 1
        if verdict == "Accepted":
            topic_data[topic]["solved_questions"].add(q_id)
            topic_data[topic]["accepted_submissions"] += 1
        if score is not None:
            topic_data[topic]["scores"].append(score)

    performance_list = []
    for topic in all_topics:
        d = topic_data[topic]
        attempted_count = len(d["attempted_questions"])
        solved_count = len(d["solved_questions"])
        total_subs = d["total_submissions"]
        scores = d["scores"]

        avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0
        accuracy = round((d["accepted_submissions"] / total_subs) * 100.0, 1) if total_subs > 0 else 0.0
        proficiency = get_proficiency_label(solved_count, attempted_count, avg_score)

        performance_list.append(
            {
                "topic": topic,
                "questions_attempted": attempted_count,
                "questions_solved": solved_count,
                "total_submissions": total_subs,
                "accuracy_percentage": accuracy,
                "average_score": avg_score,
                "proficiency_level": proficiency,
            }
        )

    return performance_list


# ============================================================================
# DIFFICULTY-WISE PERFORMANCE
# ============================================================================

async def get_difficulty_performance(
    db: AsyncSession,
    user_id: uuid.UUID,
) -> List[Dict[str, Any]]:
    """
    Compute performance breakdown per difficulty tier (Easy, Medium, Hard).
    Includes: total_available, questions_attempted, questions_solved,
    solve_rate_percentage, and average_score.
    """
    STANDARD_DIFFICULTIES = ["Easy", "Medium", "Hard"]

    # 1. Total available questions per difficulty in question bank
    bank_stmt = (
        select(
            CodingQuestion.difficulty,
            func.count(CodingQuestion.id).label("count"),
        )
        .group_by(CodingQuestion.difficulty)
    )
    bank_res = await db.execute(bank_stmt)
    bank_counts = {diff: count for diff, count in bank_res.all()}

    # 2. User's submissions joined with question and result
    user_stmt = (
        select(
            CodingQuestion.difficulty,
            CodingQuestion.id.label("question_id"),
            CodingResult.verdict,
            CodingResult.score,
        )
        .select_from(CodingSubmission)
        .join(CodingQuestion, CodingSubmission.question_id == CodingQuestion.id)
        .join(CodingResult, CodingSubmission.id == CodingResult.submission_id)
        .where(CodingSubmission.user_id == user_id)
    )
    user_res = await db.execute(user_stmt)
    user_rows = user_res.all()

    diff_data = {
        diff: {
            "attempted_questions": set(),
            "solved_questions": set(),
            "scores": [],
        }
        for diff in STANDARD_DIFFICULTIES
    }

    for diff, q_id, verdict, score in user_rows:
        if diff in diff_data:
            diff_data[diff]["attempted_questions"].add(q_id)
            if verdict == "Accepted":
                diff_data[diff]["solved_questions"].add(q_id)
            if score is not None:
                diff_data[diff]["scores"].append(score)

    results = []
    for diff in STANDARD_DIFFICULTIES:
        total_avail = bank_counts.get(diff, 0)
        attempted = len(diff_data[diff]["attempted_questions"])
        solved = len(diff_data[diff]["solved_questions"])
        scores = diff_data[diff]["scores"]

        solve_rate = round((solved / attempted) * 100.0, 1) if attempted > 0 else 0.0
        avg_score = round(sum(scores) / len(scores), 1) if scores else 0.0

        results.append(
            {
                "difficulty": diff,
                "total_available": total_avail,
                "questions_attempted": attempted,
                "questions_solved": solved,
                "solve_rate_percentage": solve_rate,
                "average_score": avg_score,
            }
        )

    return results


# ============================================================================
# WEAK-TOPIC IDENTIFICATION
# ============================================================================

async def get_weak_topics(
    db: AsyncSession,
    user_id: uuid.UUID,
    threshold: float = 70.0,
) -> List[Dict[str, Any]]:
    """
    Identify topics where the student struggles (average_score < threshold or accuracy < threshold).
    Returns list sorted by weakest (lowest score) first with actionable guidance.
    """
    topic_perf = await get_topic_performance(db, user_id)

    weak_list = []
    for tp in topic_perf:
        # Only evaluate topics where student has actually attempted questions
        if tp["questions_attempted"] > 0:
            if tp["average_score"] < threshold:
                topic_name = tp["topic"]
                if tp["questions_solved"] == 0:
                    focus_text = f"Priority practice required in {topic_name}: review foundational patterns and start with Easy problems."
                elif tp["average_score"] < 50.0:
                    focus_text = f"Significant difficulty observed in {topic_name}: practice corner cases, boundary inputs, and debugging."
                else:
                    focus_text = f"Reinforce {topic_name} problem-solving techniques and optimize runtime complexity."

                weak_list.append(
                    {
                        "topic": topic_name,
                        "questions_attempted": tp["questions_attempted"],
                        "questions_solved": tp["questions_solved"],
                        "accuracy_percentage": tp["accuracy_percentage"],
                        "average_score": tp["average_score"],
                        "recommended_focus": focus_text,
                    }
                )

    # Sort weakest first (lowest average_score, then lowest accuracy)
    weak_list.sort(key=lambda x: (x["average_score"], x["accuracy_percentage"]))
    return weak_list


# ============================================================================
# CODING PROGRESS & SUMMARY METRICS
# ============================================================================

async def get_student_coding_progress(
    db: AsyncSession,
    user_id: uuid.UUID,
) -> Dict[str, Any]:
    """
    Calculate comprehensive coding progress summary for the authenticated student:
    - Total questions in bank
    - Total questions attempted and solved
    - Overall solve rate and coding score
    - Breakdown across Easy, Medium, Hard
    - Top identified weak topics
    """
    # 1. Total questions in bank
    bank_total_stmt = select(func.count(CodingQuestion.id))
    bank_total_res = await db.execute(bank_total_stmt)
    total_bank = bank_total_res.scalar_one() or 0

    # 2. Difficulty performance
    diff_perf = await get_difficulty_performance(db, user_id)
    diff_map = {d["difficulty"]: d for d in diff_perf}

    easy_solved = diff_map.get("Easy", {}).get("questions_solved", 0)
    easy_total = diff_map.get("Easy", {}).get("total_available", 0)
    med_solved = diff_map.get("Medium", {}).get("questions_solved", 0)
    med_total = diff_map.get("Medium", {}).get("total_available", 0)
    hard_solved = diff_map.get("Hard", {}).get("questions_solved", 0)
    hard_total = diff_map.get("Hard", {}).get("total_available", 0)

    # 3. Solved and attempted counts
    all_user_subs_stmt = (
        select(
            CodingSubmission.question_id,
            CodingResult.verdict,
            CodingResult.score,
        )
        .select_from(CodingSubmission)
        .join(CodingResult, CodingSubmission.id == CodingResult.submission_id)
        .where(CodingSubmission.user_id == user_id)
    )
    subs_res = await db.execute(all_user_subs_stmt)
    sub_rows = subs_res.all()

    attempted_set = set()
    solved_set = set()
    scores = []

    for q_id, verdict, score in sub_rows:
        attempted_set.add(q_id)
        if verdict == "Accepted":
            solved_set.add(q_id)
        if score is not None:
            scores.append(score)

    total_attempted = len(attempted_set)
    total_solved = len(solved_set)
    total_subs = len(sub_rows)

    solve_rate = round((total_solved / total_bank) * 100.0, 1) if total_bank > 0 else 0.0
    overall_score = round(sum(scores) / len(scores), 1) if scores else 0.0

    # 4. Weak topics
    weak_topics_list = await get_weak_topics(db, user_id)
    weak_topic_names = [w["topic"] for w in weak_topics_list[:3]]

    return {
        "total_questions_in_bank": total_bank,
        "total_questions_attempted": total_attempted,
        "total_questions_solved": total_solved,
        "solve_rate_percentage": solve_rate,
        "total_submissions": total_subs,
        "overall_coding_score": overall_score,
        "easy_solved": easy_solved,
        "easy_total": easy_total,
        "medium_solved": med_solved,
        "medium_total": med_total,
        "hard_solved": hard_solved,
        "hard_total": hard_total,
        "weak_topics": weak_topic_names,
    }


# ============================================================================
# CODING HISTORY
# ============================================================================

async def get_coding_history(
    db: AsyncSession,
    user_id: uuid.UUID,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """Retrieve chronologically ordered evaluation and score history for student."""
    stmt = (
        select(
            CodingSubmission.id.label("submission_id"),
            CodingSubmission.question_id,
            CodingSubmission.language,
            CodingSubmission.created_at,
            CodingQuestion.title.label("question_title"),
            CodingQuestion.slug.label("question_slug"),
            CodingQuestion.difficulty,
            CodingQuestion.topic,
            CodingResult.verdict,
            CodingResult.score,
            CodingResult.passed_test_cases,
            CodingResult.total_test_cases,
            CodingResult.execution_time_ms,
        )
        .select_from(CodingSubmission)
        .join(CodingQuestion, CodingSubmission.question_id == CodingQuestion.id)
        .join(CodingResult, CodingSubmission.id == CodingResult.submission_id)
        .where(CodingSubmission.user_id == user_id)
        .order_by(CodingSubmission.created_at.desc())
        .limit(limit)
    )
    res = await db.execute(stmt)
    rows = res.all()

    history = []
    for r in rows:
        history.append(
            {
                "submission_id": r.submission_id,
                "question_id": r.question_id,
                "question_title": r.question_title,
                "question_slug": r.question_slug,
                "difficulty": r.difficulty,
                "topic": r.topic,
                "language": r.language,
                "verdict": r.verdict,
                "score": r.score,
                "passed_test_cases": r.passed_test_cases,
                "total_test_cases": r.total_test_cases,
                "execution_time_ms": r.execution_time_ms,
                "created_at": r.created_at,
            }
        )

    return history


# ============================================================================
# RECOMMENDATION ENGINE INTEGRATION
# ============================================================================

async def get_recommendation_context(
    db: AsyncSession,
    user_id: uuid.UUID,
) -> Dict[str, Any]:
    """
    Expose normalized coding profile consumed by the Recommendation Engine:
    - coding_score: overall normalized coding proficiency [0.0 - 100.0]
    - weak_topics: list of topics requiring targeted practice
    - difficulty_performance: mapping of performance by difficulty level
    - total_solved & total_attempted
    - overall proficiency_level
    """
    progress = await get_student_coding_progress(db, user_id)
    diff_perf = await get_difficulty_performance(db, user_id)
    weak_topics_list = await get_weak_topics(db, user_id)

    diff_summary = {
        d["difficulty"]: {
            "available": d["total_available"],
            "attempted": d["questions_attempted"],
            "solved": d["questions_solved"],
            "solve_rate": d["solve_rate_percentage"],
            "average_score": d["average_score"],
        }
        for d in diff_perf
    }

    weak_topics = [w["topic"] for w in weak_topics_list]

    # Overall proficiency label
    score = progress["overall_coding_score"]
    solved = progress["total_questions_solved"]
    if solved == 0:
        level = "Beginner"
    elif score >= 80.0 and solved >= 10:
        level = "Advanced"
    elif score >= 60.0 and solved >= 3:
        level = "Intermediate"
    else:
        level = "Beginner"

    return {
        "coding_score": score,
        "weak_topics": weak_topics,
        "difficulty_performance": diff_summary,
        "total_solved": solved,
        "total_attempted": progress["total_questions_attempted"],
        "proficiency_level": level,
    }
