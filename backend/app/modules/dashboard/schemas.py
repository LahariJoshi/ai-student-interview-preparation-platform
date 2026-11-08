from typing import List, Optional
from pydantic import BaseModel, Field


class MetricSummaryOut(BaseModel):
    ats_score: Optional[float] = Field(
        None,
        description="Latest ATS match score (0-100), or None if no scan performed."
    )
    ats_source: Optional[str] = Field(
        None,
        description="'ats_analysis' or 'resume_analysis' or None."
    )
    coding_solved: int = Field(
        0,
        description="Total distinct questions successfully solved ('Accepted')."
    )
    coding_total: int = Field(
        0,
        description="Total available coding questions in the platform bank."
    )
    coding_attempted: int = Field(
        0,
        description="Total distinct questions attempted by student."
    )
    coding_solve_rate: float = Field(
        0.0,
        description="Percentage of total bank solved (solved / total * 100)."
    )
    coding_accuracy: Optional[float] = Field(
        None,
        description="Percentage of attempted questions solved (solved / attempted * 100), or None if 0 attempted."
    )
    interview_count: int = Field(
        0,
        description="Total completed mock interview sessions."
    )
    interview_avg_score: Optional[float] = Field(
        None,
        description="Average score of completed mock interviews (0-100), or None if 0 completed."
    )
    readiness_score: float = Field(
        0.0,
        description="Calculated interview readiness score (0-100) strictly from available evaluations without arbitrary baseline."
    )


class ProgressPeriodOut(BaseModel):
    label: str = Field(..., description="Short period label (e.g., 'W1', 'JAN', etc.)")
    period_start: str = Field(..., description="ISO date YYYY-MM-DD")
    period_end: str = Field(..., description="ISO date YYYY-MM-DD")
    coding_score: float = Field(..., description="Normalized coding performance on 0-50 scale")
    interview_score: float = Field(..., description="Normalized interview performance on 0-50 scale")
    coding_submissions_count: int = Field(..., description="Total submissions in this period")
    interview_sessions_count: int = Field(..., description="Total completed interviews in this period")
    peak: bool = Field(False, description="Whether this period had the highest combined performance")
    peak_value: Optional[str] = Field(None, description="Display tooltip value for peak (e.g. '82%')")


class ProgressChartOut(BaseModel):
    periods: List[ProgressPeriodOut] = Field(
        default_factory=list,
        description="Sequential assessment periods showing actual performance comparison."
    )
    scale_max: float = Field(50.0, description="Upper bound for visual bars (0-50)")


class SkillWeekOut(BaseModel):
    label: str = Field(..., description="Week label, e.g. 'Week 1'")
    week_start: str = Field(..., description="ISO date YYYY-MM-DD")
    week_end: str = Field(..., description="ISO date YYYY-MM-DD")
    coding_proficiency: float = Field(
        0.0,
        description="True average coding score in this week (0-100), 0.0 if no submissions."
    )
    interview_fluency: float = Field(
        0.0,
        description="True average mock interview score in this week (0-100), 0.0 if no interviews."
    )
    coding_count: int = Field(0, description="Number of coding submissions in this week.")
    interview_count: int = Field(0, description="Number of completed interviews in this week.")


class CalendarActivityDayOut(BaseModel):
    day: int = Field(..., description="Day number of the month (1-31)")
    date: str = Field(..., description="ISO date YYYY-MM-DD")
    activity_type: str = Field(
        ...,
        description="'mock_session' (navy) | 'coding_practice' (orange) | 'both'"
    )
    coding_count: int = Field(0, description="Submissions on this day")
    interview_count: int = Field(0, description="Completed interviews on this day")


class SkillCalendarOut(BaseModel):
    month_name: str = Field(..., description="Full month name, e.g. 'November'")
    year: int = Field(..., description="Calendar year, e.g. 2026")
    month: int = Field(..., description="Calendar month (1-12)")
    days_in_month: int = Field(..., description="Total days in this month")
    first_weekday: int = Field(..., description="Weekday of first day of month (0=Monday..6=Sunday)")
    active_days: List[CalendarActivityDayOut] = Field(
        default_factory=list,
        description="List of days in this month with verified user practice activity."
    )


class SkillDevelopmentOut(BaseModel):
    weeks: List[SkillWeekOut] = Field(
        default_factory=list,
        description="Last 4 weekly intervals with real coding proficiency and interview fluency."
    )
    calendar: SkillCalendarOut = Field(
        ...,
        description="Target calendar showing true activity markers for the current month."
    )


class AssessmentRecordOut(BaseModel):
    id: str = Field(..., description="Record unique identifier")
    type: str = Field(..., description="'ATS Analysis' | 'Coding Assessment' | 'Mock Interview'")
    title: str = Field(..., description="Record descriptive title")
    date: str = Field(..., description="Formatted date string")
    iso_date: str = Field(..., description="ISO timestamp YYYY-MM-DDTHH:MM:SSZ")
    score: float = Field(..., description="Normalized score 0-100")
    status: str = Field(..., description="'Completed' | 'Passed' | 'Needs Review'")
    link: str = Field(..., description="Navigation link to view result")


class DashboardOverviewResponse(BaseModel):
    metrics: MetricSummaryOut
    progress_chart: ProgressChartOut
    skill_development: SkillDevelopmentOut
    recent_history: List[AssessmentRecordOut]
