export type Difficulty = 'Easy' | 'Medium' | 'Hard';

export type SolveStatus = 'all' | 'solved' | 'unsolved';

export type SortField = 'created_at' | 'title' | 'difficulty';

export type SortOrder = 'asc' | 'desc';

export interface CodingTestCaseSample {
  id: string;
  input_data: string;
  expected_output: string;
  is_sample: boolean;
  explanation?: string | null;
  order_index: number;
}

export interface CodingTestCase extends CodingTestCaseSample {
  created_at: string;
}

export interface CodingQuestionSummary {
  id: string;
  title: string;
  slug: string;
  difficulty: Difficulty;
  topic: string;
  sample_test_case_count: number;
  is_solved?: boolean | null;
  created_at: string;
}

export interface CodingQuestionDetail {
  id: string;
  title: string;
  slug: string;
  description: string;
  difficulty: Difficulty;
  topic: string;
  constraints?: string | null;
  hints?: string[];
  starter_code: Record<string, string>;
  sample_test_cases: CodingTestCaseSample[];
  is_solved?: boolean | null;
  created_at: string;
  updated_at: string;
}

export interface QuestionListResponse {
  total_count: number;
  page: number;
  limit: number;
  total_pages: number;
  questions: CodingQuestionSummary[];
}

export interface TopicSummary {
  topic: string;
  question_count: number;
  easy_count: number;
  medium_count: number;
  hard_count: number;
}

export interface DifficultySummary {
  difficulty: Difficulty;
  question_count: number;
}

export interface QuestionFilterParams {
  topic?: string;
  difficulty?: Difficulty;
  search?: string;
  status?: SolveStatus;
  sort_by?: SortField;
  sort_order?: SortOrder;
  page?: number;
  limit?: number;
  skip?: number;
}

export type ProgrammingLanguage = 'python' | 'javascript' | 'typescript' | 'java' | 'cpp';

export type SubmissionStatus = 'pending' | 'running' | 'completed' | 'failed';

export interface SubmissionCreateRequest {
  question_id: string;
  language: ProgrammingLanguage | string;
  code: string;
}

export interface TestCaseRunResult {
  test_case_id: string;
  order_index: number;
  is_sample: boolean;
  passed: boolean;
  verdict: string;
  execution_time_ms?: number | null;
  actual_output?: string | null;
  expected_output?: string | null;
  input_data?: string | null;
  error_message?: string | null;
}

export interface SubmissionResultSummary {
  id: string;
  verdict: string;
  score: number;
  passed_test_cases: number;
  total_test_cases: number;
  execution_time_ms?: number | null;
  memory_kb?: number | null;
  error_message?: string | null;
  test_case_results?: TestCaseRunResult[] | null;
}

export interface CodeRunRequest {
  language: ProgrammingLanguage | string;
  code: string;
}

export interface CodeRunResponse {
  verdict: string;
  passed_test_cases: number;
  total_test_cases: number;
  execution_time_ms: number;
  error_message?: string | null;
  test_cases: TestCaseRunResult[];
}

export interface CodingSubmissionDetail {
  id: string;
  user_id: string;
  question_id: string;
  language: string;
  code: string;
  status: SubmissionStatus;
  created_at: string;
  question_title?: string | null;
  question_slug?: string | null;
  question_difficulty?: Difficulty | null;
  question_topic?: string | null;
  result?: SubmissionResultSummary | null;
}

export interface CodingSubmissionListItem {
  id: string;
  user_id: string;
  question_id: string;
  language: string;
  status: SubmissionStatus;
  created_at: string;
  question_title?: string | null;
  question_slug?: string | null;
  question_difficulty?: Difficulty | null;
  question_topic?: string | null;
  score?: number | null;
  verdict?: string | null;
  passed_test_cases?: number | null;
  total_test_cases?: number | null;
}

export interface SubmissionListResponse {
  total_count: number;
  page: number;
  limit: number;
  total_pages: number;
  submissions: CodingSubmissionListItem[];
}

export interface CodingMetrics {
  execution_time_ms: number;
  memory_kb: number;
}

export interface NormalizedPerformanceResult {
  submission_id: string;
  score: number;
  passed_tests: number;
  total_tests: number;
  topic: string;
  difficulty: Difficulty | string;
  execution_status: string;
  coding_metrics: CodingMetrics;
}

export interface TopicPerformance {
  topic: string;
  questions_attempted: number;
  questions_solved: number;
  total_submissions: number;
  accuracy_percentage: number;
  average_score: number;
  proficiency_level: string;
}

export interface DifficultyPerformance {
  difficulty: Difficulty | string;
  total_available: number;
  questions_attempted: number;
  questions_solved: number;
  solve_rate_percentage: number;
  average_score: number;
}

export interface WeakTopic {
  topic: string;
  questions_attempted: number;
  questions_solved: number;
  accuracy_percentage: number;
  average_score: number;
  recommended_focus: string;
}

export interface CodingHistoryItem {
  submission_id: string;
  question_id: string;
  question_title: string;
  question_slug: string;
  difficulty: Difficulty | string;
  topic: string;
  language: string;
  verdict: string;
  score: number;
  passed_test_cases: number;
  total_test_cases: number;
  execution_time_ms?: number | null;
  created_at: string;
}

export interface CodingProgressSummary {
  total_questions_in_bank: number;
  total_questions_attempted: number;
  total_questions_solved: number;
  solve_rate_percentage: number;
  total_submissions: number;
  overall_coding_score: number;
  easy_solved: number;
  easy_total: number;
  medium_solved: number;
  medium_total: number;
  hard_solved: number;
  hard_total: number;
  weak_topics: string[];
}

export interface RecommendationContext {
  coding_score: number;
  weak_topics: string[];
  difficulty_performance: Record<
    string,
    {
      available: number;
      attempted: number;
      solved: number;
      solve_rate: number;
      average_score: number;
    }
  >;
  total_solved: number;
  total_attempted: number;
  proficiency_level: string;
}
