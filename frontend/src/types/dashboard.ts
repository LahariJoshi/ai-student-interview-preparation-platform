export interface MetricSummary {
  ats_score: number | null;
  ats_source: string | null;
  coding_solved: number;
  coding_total: number;
  coding_attempted: number;
  coding_solve_rate: number;
  coding_accuracy: number | null;
  interview_count: number;
  interview_avg_score: number | null;
  readiness_score: number;
}

export interface ProgressPeriod {
  label: string;
  period_start: string;
  period_end: string;
  coding_score: number;
  interview_score: number;
  coding_submissions_count: number;
  interview_sessions_count: number;
  peak: boolean;
  peak_value: string | null;
}

export interface ProgressChartData {
  periods: ProgressPeriod[];
  scale_max: number;
}

export interface SkillWeek {
  label: string;
  week_start: string;
  week_end: string;
  coding_proficiency: number;
  interview_fluency: number;
  coding_count: number;
  interview_count: number;
}

export interface CalendarActivityDay {
  day: number;
  date: string;
  activity_type: "mock_session" | "coding_practice" | "both";
  coding_count: number;
  interview_count: number;
}

export interface SkillCalendar {
  month_name: string;
  year: number;
  month: number;
  days_in_month: number;
  first_weekday: number;
  active_days: CalendarActivityDay[];
}

export interface SkillDevelopmentData {
  weeks: SkillWeek[];
  calendar: SkillCalendar;
}

export interface DashboardAssessmentRecord {
  id: string;
  type: "ATS Analysis" | "Coding Assessment" | "Mock Interview";
  title: string;
  date: string;
  iso_date: string;
  score: number;
  status: "Completed" | "Passed" | "Needs Review";
  link: string;
}

export interface DashboardOverviewResponse {
  metrics: MetricSummary;
  progress_chart: ProgressChartData;
  skill_development: SkillDevelopmentData;
  recent_history: DashboardAssessmentRecord[];
}
