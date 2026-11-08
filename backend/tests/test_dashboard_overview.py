import uuid
from datetime import datetime, timezone, timedelta
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models.user import User
from app.db.models.resume import Resume
from app.db.models.job_description import JobDescription
from app.db.models.ats_analysis import ATSAnalysis
from app.db.models.coding import CodingQuestion, CodingSubmission, CodingResult
from app.db.models.interview import InterviewSession

pytestmark = pytest.mark.asyncio


async def get_student_cookies(
    async_client: AsyncClient,
    email: str = "dashstudent@example.com",
) -> dict:
    """Helper to register and obtain auth session cookie for a student."""
    reg_payload = {
        "email": email,
        "password": "Password123!",
        "full_name": "Dashboard Student",
    }
    response = await async_client.post("/api/v1/auth/register", json=reg_payload)
    assert response.status_code == 201
    return dict(response.cookies)


async def test_dashboard_overview_unauthorized(async_client: AsyncClient):
    """Accessing /api/v1/dashboard/overview without authentication must return 401."""
    res = await async_client.get("/api/v1/dashboard/overview")
    assert res.status_code == 401
    assert "token missing" in res.json()["detail"].lower()


async def test_dashboard_overview_empty_student(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """
    A brand new student with zero assessments must receive a clean, 200 OK overview.
    No arbitrary 20% or 45% baselines should be applied. Missing values must be None.
    """
    cookies = await get_student_cookies(async_client, "new_student@example.com")
    res = await async_client.get("/api/v1/dashboard/overview", cookies=cookies)
    assert res.status_code == 200

    data = res.json()
    metrics = data["metrics"]

    # 1. Verification of missing vs zero distinctions
    assert metrics["ats_score"] is None
    assert metrics["ats_source"] is None
    assert metrics["coding_solved"] == 0
    assert metrics["coding_attempted"] == 0
    assert metrics["coding_solve_rate"] == 0.0
    assert metrics["coding_accuracy"] is None  # None because attempted == 0
    assert metrics["interview_count"] == 0
    assert metrics["interview_avg_score"] is None
    # Readiness must be strictly 0.0 (no arbitrary baseline)
    assert metrics["readiness_score"] == 0.0

    # 2. Charts must have valid structure with zeroed values (no runtime errors)
    progress = data["progress_chart"]
    assert len(progress["periods"]) == 8
    for p in progress["periods"]:
        assert p["coding_score"] == 0.0
        assert p["interview_score"] == 0.0
        assert p["peak"] is False

    skill_dev = data["skill_development"]
    assert len(skill_dev["weeks"]) == 4
    for w in skill_dev["weeks"]:
        assert w["coding_proficiency"] == 0.0
        assert w["interview_fluency"] == 0.0

    calendar = skill_dev["calendar"]
    assert calendar["days_in_month"] >= 28
    assert calendar["active_days"] == []

    # 3. History must be an empty list
    assert data["recent_history"] == []


async def test_dashboard_overview_coding_and_duplicate_prevention(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """
    Verify that solving the same question multiple times only counts once for solve_rate
    and coding_solved, while accurately calculating coding accuracy and time periods.
    """
    cookies = await get_student_cookies(async_client, "coding_pro@example.com")
    user_res = await db_session.execute(
        select(User).where(User.email == "coding_pro@example.com")
    )
    user = user_res.scalar_one()

    # Create 2 questions
    q1 = CodingQuestion(
        title="Two Sum",
        slug="two-sum-dash-test",
        description="Find two numbers",
        difficulty="Easy",
        topic="Array",
        starter_code={"python": "pass"},
    )
    q2 = CodingQuestion(
        title="Valid Parentheses",
        slug="valid-parentheses-dash-test",
        description="Check matching brackets",
        difficulty="Easy",
        topic="Stack",
        starter_code={"python": "pass"},
    )
    db_session.add_all([q1, q2])
    await db_session.commit()
    await db_session.refresh(q1)
    await db_session.refresh(q2)

    now = datetime.now(timezone.utc)

    # Question 1: Submission 1 (Accepted, 100)
    sub1 = CodingSubmission(
        user_id=user.id,
        question_id=q1.id,
        language="python",
        code="def solve(): pass",
        status="completed",
        created_at=now - timedelta(days=2),
    )
    db_session.add(sub1)
    await db_session.commit()
    await db_session.refresh(sub1)

    res1 = CodingResult(
        submission_id=sub1.id,
        verdict="Accepted",
        score=100.0,
        passed_test_cases=3,
        total_test_cases=3,
        evaluated_at=now - timedelta(days=2),
    )
    db_session.add(res1)

    # Question 1: Submission 2 (Duplicate attempt on same question, Accepted, 100)
    sub2 = CodingSubmission(
        user_id=user.id,
        question_id=q1.id,
        language="python",
        code="def solve(): pass # better",
        status="completed",
        created_at=now - timedelta(days=1),
    )
    db_session.add(sub2)
    await db_session.commit()
    await db_session.refresh(sub2)

    res2 = CodingResult(
        submission_id=sub2.id,
        verdict="Accepted",
        score=100.0,
        passed_test_cases=3,
        total_test_cases=3,
        evaluated_at=now - timedelta(days=1),
    )
    db_session.add(res2)

    # Question 2: Submission 3 (Wrong Answer, 0.0)
    sub3 = CodingSubmission(
        user_id=user.id,
        question_id=q2.id,
        language="python",
        code="def solve(): pass # wrong",
        status="completed",
        created_at=now - timedelta(hours=3),
    )
    db_session.add(sub3)
    await db_session.commit()
    await db_session.refresh(sub3)

    res3 = CodingResult(
        submission_id=sub3.id,
        verdict="Wrong Answer",
        score=0.0,
        passed_test_cases=0,
        total_test_cases=3,
        evaluated_at=now - timedelta(hours=3),
    )
    db_session.add(res3)
    await db_session.commit()

    # Query overview
    res = await async_client.get("/api/v1/dashboard/overview", cookies=cookies)
    assert res.status_code == 200
    data = res.json()
    metrics = data["metrics"]

    # Even though there are 2 Accepted submissions for Q1, distinct solved is 1!
    assert metrics["coding_solved"] == 1
    assert metrics["coding_attempted"] == 2  # Q1 and Q2
    # Accuracy: 1 solved out of 2 attempted = 50.0%
    assert metrics["coding_accuracy"] == 50.0
    # Solve rate: 1 solved out of 2 bank questions = 50.0%
    assert metrics["coding_solve_rate"] == 50.0

    # Readiness score: Coding contribution is 50.0 * 0.35 = 17.5
    assert metrics["readiness_score"] == 17.5

    # Check calendar has coding practice recorded
    active_days = data["skill_development"]["calendar"]["active_days"]
    assert len(active_days) >= 1
    assert any(ad["activity_type"] in ("coding_practice", "both") for ad in active_days)


async def test_dashboard_overview_interview_and_ats_integration(
    async_client: AsyncClient,
    db_session: AsyncSession,
):
    """
    Verify ATS score integration, completed interview calculations,
    and history records aggregation.
    """
    cookies = await get_student_cookies(async_client, "full_prep@example.com")
    user_res = await db_session.execute(
        select(User).where(User.email == "full_prep@example.com")
    )
    user = user_res.scalar_one()

    now = datetime.now(timezone.utc)

    # 1. Add Resume and Job Description for ATS
    resume = Resume(
        user_id=user.id,
        original_filename="resume.pdf",
        stored_filename="stored_resume.pdf",
        file_path="uploads/stored_resume.pdf",
        file_size=1024,
        mime_type="application/pdf",
        extraction_status="completed",
        raw_text="Experienced Software Engineer in Python, FastAPI, React.",
    )
    jd = JobDescription(
        user_id=user.id,
        title="Full Stack Engineer",
        company_name="TechCorp",
        description_text="Looking for a Python and FastAPI backend developer.",
    )
    db_session.add_all([resume, jd])
    await db_session.commit()
    await db_session.refresh(resume)
    await db_session.refresh(jd)

    ats = ATSAnalysis(
        user_id=user.id,
        resume_id=resume.id,
        job_description_id=jd.id,
        analysis_status="completed",
        ats_score=80.0,
        formatting_score=90.0,
        keyword_match_score=80.0,
        semantic_similarity_score=75.0,
        created_at=now - timedelta(days=3),
    )
    db_session.add(ats)

    # 2. Add Completed Mock Interview Session
    sess1 = InterviewSession(
        user_id=user.id,
        target_role="Full Stack Engineer",
        interview_type="technical",
        status="completed",
        overall_score=85.0,
        technical_score=90.0,
        communication_score=80.0,
        started_at=now - timedelta(days=1),
        ended_at=now - timedelta(days=1, minutes=15),
        created_at=now - timedelta(days=1),
    )
    # Add In-progress interview session (should NOT count towards average score or completed count)
    sess2 = InterviewSession(
        user_id=user.id,
        target_role="Full Stack Engineer",
        interview_type="behavioral",
        status="in_progress",
        overall_score=None,
        started_at=now - timedelta(hours=2),
        created_at=now - timedelta(hours=2),
    )
    db_session.add_all([sess1, sess2])
    await db_session.commit()

    # Query overview
    res = await async_client.get("/api/v1/dashboard/overview", cookies=cookies)
    assert res.status_code == 200
    data = res.json()
    metrics = data["metrics"]

    assert metrics["ats_score"] == 80.0
    assert metrics["ats_source"] == "ats_analysis"
    assert metrics["interview_count"] == 1  # only completed session
    assert metrics["interview_avg_score"] == 85.0

    # Readiness score:
    # ATS: 80 * 0.30 = 24.0
    # Coding: 0.0
    # Interview: 85 * 0.35 = 29.75
    # Total readiness: round(24.0 + 29.75, 1) = 53.8
    assert metrics["readiness_score"] == 53.8

    # History verification: ATS and interview sessions should be in recent_history
    history = data["recent_history"]
    assert len(history) >= 2
    types = [h["type"] for h in history]
    assert "ATS Analysis" in types
    assert "Mock Interview" in types

    # Verify chronological sorting (newest first)
    dates = [h["iso_date"] for h in history]
    assert dates == sorted(dates, reverse=True)
