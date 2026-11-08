import calendar
import uuid
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any, Tuple

from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.coding import (
    CodingQuestion,
    CodingSubmission,
    CodingResult,
)
from app.db.models.interview import InterviewSession
from app.db.models.ats_analysis import ATSAnalysis
from app.db.models.resume_analysis import ResumeAnalysis
from app.modules.dashboard.schemas import (
    MetricSummaryOut,
    ProgressPeriodOut,
    ProgressChartOut,
    SkillWeekOut,
    CalendarActivityDayOut,
    SkillCalendarOut,
    SkillDevelopmentOut,
    AssessmentRecordOut,
    DashboardOverviewResponse,
)


def ensure_utc(dt: Optional[datetime]) -> Optional[datetime]:
    """Ensure datetime is tz-aware UTC across SQLite (naive) and PostgreSQL (tz-aware)."""
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


async def get_dashboard_overview(
    db: AsyncSession,
    user_id: uuid.UUID,
) -> DashboardOverviewResponse:
    """
    Generate unified, accurate, and real-time dashboard analytics for the authenticated student.
    Uses strictly verified database records without artificial interpolation or arbitrary baselines.
    """
    now = datetime.now(timezone.utc)

    # =========================================================================
    # 1. ATS METRIC (Latest Analysis)
    # =========================================================================
    ats_score: Optional[float] = None
    ats_source: Optional[str] = None
    ats_records_for_history: List[Dict[str, Any]] = []

    # Query latest ATS analysis against target job description
    ats_stmt = (
        select(ATSAnalysis)
        .where(
            ATSAnalysis.user_id == user_id,
            ATSAnalysis.analysis_status == "completed",
        )
        .order_by(ATSAnalysis.created_at.desc())
        .limit(10)
    )
    ats_res = await db.execute(ats_stmt)
    ats_list = ats_res.scalars().all()

    if ats_list:
        latest_ats = ats_list[0]
        if latest_ats.ats_score is not None:
            ats_score = round(latest_ats.ats_score, 1)
            ats_source = "ats_analysis"

        for item in ats_list:
            ats_records_for_history.append({
                "id": str(item.id),
                "type": "ATS Analysis",
                "title": "Resume vs Target Job Description",
                "datetime": ensure_utc(item.created_at),
                "score": round(item.ats_score or 0.0, 1),
                "status": "Completed" if (item.ats_score or 0.0) >= 70.0 else "Needs Review",
                "link": "/ats",
            })
    else:
        # Fallback check for structural resume analysis if no job-specific ATS exists
        resume_stmt = (
            select(ResumeAnalysis)
            .where(
                ResumeAnalysis.user_id == user_id,
                ResumeAnalysis.analysis_status == "completed",
            )
            .order_by(ResumeAnalysis.created_at.desc())
            .limit(10)
        )
        resume_res = await db.execute(resume_stmt)
        resume_list = resume_res.scalars().all()

        if resume_list:
            latest_resume = resume_list[0]
            if latest_resume.quality_score is not None:
                ats_score = round(latest_resume.quality_score, 1)
                ats_source = "resume_analysis"

            for item in resume_list:
                ats_records_for_history.append({
                    "id": str(item.id),
                    "type": "ATS Analysis",
                    "title": "Resume Structural Quality",
                    "datetime": ensure_utc(item.created_at),
                    "score": round(item.quality_score or 0.0, 1),
                    "status": "Completed" if (item.quality_score or 0.0) >= 70.0 else "Needs Review",
                    "link": "/resume",
                })

    # =========================================================================
    # 2. CODING METRICS & SUBMISSIONS
    # =========================================================================
    # 2.1 Total coding questions available in the platform
    total_bank_stmt = select(func.count(CodingQuestion.id))
    total_bank_res = await db.execute(total_bank_stmt)
    coding_total = total_bank_res.scalar_one() or 0

    # 2.2 User submissions with associated question and result
    subs_stmt = (
        select(
            CodingSubmission.id.label("submission_id"),
            CodingSubmission.question_id,
            CodingSubmission.language,
            CodingSubmission.created_at,
            CodingQuestion.title.label("question_title"),
            CodingResult.score,
            CodingResult.verdict,
        )
        .select_from(CodingSubmission)
        .join(CodingQuestion, CodingSubmission.question_id == CodingQuestion.id)
        .join(CodingResult, CodingSubmission.id == CodingResult.submission_id)
        .where(CodingSubmission.user_id == user_id)
        .order_by(CodingSubmission.created_at.desc())
    )
    subs_res = await db.execute(subs_stmt)
    sub_rows = subs_res.all()

    attempted_q_ids = set()
    solved_q_ids = set()
    coding_records_for_history: List[Dict[str, Any]] = []

    for row in sub_rows:
        attempted_q_ids.add(row.question_id)
        if row.verdict == "Accepted":
            solved_q_ids.add(row.question_id)

        coding_records_for_history.append({
            "id": str(row.submission_id),
            "type": "Coding Assessment",
            "title": f"{row.question_title} ({row.language})",
            "datetime": ensure_utc(row.created_at),
            "score": round(row.score or 0.0, 1),
            "status": "Passed" if row.verdict == "Accepted" else "Needs Review",
            "link": f"/coding/results?submissionId={row.submission_id}",
        })

    coding_solved = len(solved_q_ids)
    coding_attempted = len(attempted_q_ids)
    coding_solve_rate = (
        round((coding_solved / coding_total) * 100.0, 1) if coding_total > 0 else 0.0
    )
    coding_accuracy = (
        round((coding_solved / coding_attempted) * 100.0, 1)
        if coding_attempted > 0
        else None
    )

    # =========================================================================
    # 3. INTERVIEW METRICS & SESSIONS
    # =========================================================================
    int_stmt = (
        select(InterviewSession)
        .where(InterviewSession.user_id == user_id)
        .order_by(InterviewSession.started_at.desc())
    )
    int_res = await db.execute(int_stmt)
    interview_sessions = int_res.scalars().all()

    completed_interviews = [
        s for s in interview_sessions
        if s.status == "completed" and s.overall_score is not None
    ]
    interview_count = len(completed_interviews)
    interview_avg_score = (
        round(sum(s.overall_score for s in completed_interviews) / interview_count, 1)
        if interview_count > 0
        else None
    )

    interview_records_for_history: List[Dict[str, Any]] = []
    for s in interview_sessions:
        dt = ensure_utc(s.started_at or s.created_at)
        score_val = round(s.overall_score or 0.0, 1)
        interview_records_for_history.append({
            "id": str(s.id),
            "type": "Mock Interview",
            "title": f"{s.target_role} ({s.interview_type})",
            "datetime": dt,
            "score": score_val,
            "status": "Completed" if s.status == "completed" else "Needs Review",
            "link": f"/interview/{s.id}/results",
        })

    # =========================================================================
    # 4. READINESS SCORE (Consistent, zero arbitrary baseline)
    # =========================================================================
    # Weights: ATS 30%, Coding Solve Rate 35%, Interview Average 35%
    ats_contrib = (ats_score * 0.30) if ats_score is not None else 0.0
    coding_contrib = (coding_solve_rate * 0.35) if coding_total > 0 else 0.0
    interview_contrib = (interview_avg_score * 0.35) if interview_avg_score is not None else 0.0

    readiness_score = round(min(100.0, ats_contrib + coding_contrib + interview_contrib), 1)

    metrics_out = MetricSummaryOut(
        ats_score=ats_score,
        ats_source=ats_source,
        coding_solved=coding_solved,
        coding_total=coding_total,
        coding_attempted=coding_attempted,
        coding_solve_rate=coding_solve_rate,
        coding_accuracy=coding_accuracy,
        interview_count=interview_count,
        interview_avg_score=interview_avg_score,
        readiness_score=readiness_score,
    )

    # =========================================================================
    # 5. PREPARATION PROGRESS COMPARISON (8 Weekly Periods)
    # =========================================================================
    # Divide the last 8 weeks (56 days) into 8 contiguous 7-day buckets
    progress_periods: List[ProgressPeriodOut] = []
    max_combined_score = -1.0
    peak_period_idx = -1

    for i in range(8):
        # Period 0 is 7-8 weeks ago; Period 7 is the current week
        period_days_ago_end = (7 - i) * 7
        period_days_ago_start = (8 - i) * 7

        p_end = now - timedelta(days=period_days_ago_end)
        p_start = now - timedelta(days=period_days_ago_start)

        label = f"W{i + 1}"

        # Submissions falling into this period
        period_subs = [
            r for r in sub_rows
            if p_start <= ensure_utc(r.created_at) < p_end
        ]
        period_sub_count = len(period_subs)
        if period_sub_count > 0:
            avg_sub_score = sum(r.score or 0.0 for r in period_subs) / period_sub_count
            # Scale 0-100 down to 0-50 for dual-bar comparison
            norm_coding = round(min(50.0, (avg_sub_score / 2.0)), 1)
        else:
            norm_coding = 0.0

        # Completed interviews falling into this period
        period_ints = [
            s for s in completed_interviews
            if p_start <= ensure_utc(s.started_at) < p_end
        ]
        period_int_count = len(period_ints)
        if period_int_count > 0:
            avg_int_score = sum(s.overall_score for s in period_ints) / period_int_count
            norm_interview = round(min(50.0, (avg_int_score / 2.0)), 1)
        else:
            norm_interview = 0.0

        combined = norm_coding + norm_interview
        if combined > max_combined_score and combined > 0.0:
            max_combined_score = combined
            peak_period_idx = i

        progress_periods.append(
            ProgressPeriodOut(
                label=label,
                period_start=p_start.strftime("%Y-%m-%d"),
                period_end=p_end.strftime("%Y-%m-%d"),
                coding_score=norm_coding,
                interview_score=norm_interview,
                coding_submissions_count=period_sub_count,
                interview_sessions_count=period_int_count,
                peak=False,
                peak_value=None,
            )
        )

    # Set peak indicator if any period had real activity
    if peak_period_idx >= 0:
        p = progress_periods[peak_period_idx]
        total_pct = round((p.coding_score + p.interview_score), 1)
        progress_periods[peak_period_idx].peak = True
        progress_periods[peak_period_idx].peak_value = f"{total_pct}"

    progress_chart_out = ProgressChartOut(
        periods=progress_periods,
        scale_max=50.0,
    )

    # =========================================================================
    # 6. SKILL DEVELOPMENT (Wave Chart Weeks + Calendar)
    # =========================================================================
    # 6.1 Last 4 Weeks (28 days) proficiency trendlines (0-100 scale)
    skill_weeks: List[SkillWeekOut] = []
    for i in range(4):
        # Week 0 is 3 weeks ago; Week 3 is current week
        days_end = (3 - i) * 7
        days_start = (4 - i) * 7

        w_end = now - timedelta(days=days_end)
        w_start = now - timedelta(days=days_start)

        w_subs = [r for r in sub_rows if w_start <= ensure_utc(r.created_at) < w_end]
        w_ints = [s for s in completed_interviews if w_start <= ensure_utc(s.started_at) < w_end]

        coding_prof = (
            round(sum(r.score or 0.0 for r in w_subs) / len(w_subs), 1)
            if w_subs
            else 0.0
        )
        interview_fluency = (
            round(sum(s.overall_score for s in w_ints) / len(w_ints), 1)
            if w_ints
            else 0.0
        )

        skill_weeks.append(
            SkillWeekOut(
                label=f"Week {i + 1}",
                week_start=w_start.strftime("%Y-%m-%d"),
                week_end=w_end.strftime("%Y-%m-%d"),
                coding_proficiency=coding_prof,
                interview_fluency=interview_fluency,
                coding_count=len(w_subs),
                interview_count=len(w_ints),
            )
        )

    # 6.2 Calendar for current UTC month
    current_year = now.year
    current_month = now.month
    month_name = calendar.month_name[current_month]
    _, days_in_month = calendar.monthrange(current_year, current_month)
    # first_weekday: calendar.weekday returns 0=Monday..6=Sunday
    first_weekday = calendar.weekday(current_year, current_month, 1)

    # Range of current month in UTC
    month_start = datetime(current_year, current_month, 1, 0, 0, 0, tzinfo=timezone.utc)
    # End of month boundary
    if current_month == 12:
        month_end = datetime(current_year + 1, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    else:
        month_end = datetime(current_year, current_month + 1, 1, 0, 0, 0, tzinfo=timezone.utc)

    # Aggregate active days
    coding_day_counts: Dict[int, int] = {}
    for r in sub_rows:
        r_dt = ensure_utc(r.created_at)
        if r_dt and month_start <= r_dt < month_end:
            day_num = r_dt.day
            coding_day_counts[day_num] = coding_day_counts.get(day_num, 0) + 1

    interview_day_counts: Dict[int, int] = {}
    for s in completed_interviews:
        s_dt = ensure_utc(s.started_at)
        if s_dt and month_start <= s_dt < month_end:
            day_num = s_dt.day
            interview_day_counts[day_num] = interview_day_counts.get(day_num, 0) + 1

    active_days: List[CalendarActivityDayOut] = []
    all_active_day_numbers = sorted(set(coding_day_counts.keys()).union(set(interview_day_counts.keys())))

    for d in all_active_day_numbers:
        c_count = coding_day_counts.get(d, 0)
        i_count = interview_day_counts.get(d, 0)

        if c_count > 0 and i_count > 0:
            act_type = "both"
        elif i_count > 0:
            act_type = "mock_session"
        else:
            act_type = "coding_practice"

        d_str = f"{current_year:04d}-{current_month:02d}-{d:02d}"
        active_days.append(
            CalendarActivityDayOut(
                day=d,
                date=d_str,
                activity_type=act_type,
                coding_count=c_count,
                interview_count=i_count,
            )
        )

    calendar_out = SkillCalendarOut(
        month_name=month_name,
        year=current_year,
        month=current_month,
        days_in_month=days_in_month,
        first_weekday=first_weekday,
        active_days=active_days,
    )

    skill_development_out = SkillDevelopmentOut(
        weeks=skill_weeks,
        calendar=calendar_out,
    )

    # =========================================================================
    # 7. RECENT ASSESSMENT HISTORY (Unified, Chronological Top 10)
    # =========================================================================
    all_history = (
        ats_records_for_history
        + coding_records_for_history
        + interview_records_for_history
    )

    # Sort all records strictly descending by ISO datetime
    all_history.sort(key=lambda x: x["datetime"], reverse=True)

    top_history: List[AssessmentRecordOut] = []
    for item in all_history[:10]:
        dt: datetime = item["datetime"]
        top_history.append(
            AssessmentRecordOut(
                id=item["id"],
                type=item["type"],
                title=item["title"],
                date=dt.strftime("%b %d, %Y"),
                iso_date=dt.isoformat(),
                score=item["score"],
                status=item["status"],
                link=item["link"],
            )
        )

    return DashboardOverviewResponse(
        metrics=metrics_out,
        progress_chart=progress_chart_out,
        skill_development=skill_development_out,
        recent_history=top_history,
    )
