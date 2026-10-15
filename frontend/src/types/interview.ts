export interface QuestionOut {
  id: string;
  order_index: number;
  question_text: string;
  category: "technical" | "behavioral" | "hr" | "project_based" | string;
  difficulty: "Beginner" | "Intermediate" | "Advanced" | string;
  topic_or_skill?: string | null;
  expected_key_points: string[];
  reference_answer?: string | null;
}

export interface AnswerOut {
  id: string;
  question_id: string;
  answer_text: string;
  is_voice_response: boolean;
  score?: number | null;
  relevance_score?: number | null;
  technical_accuracy_score?: number | null;
  completeness_score?: number | null;
  clarity_score?: number | null;
  detailed_feedback?: string | null;
  improvement_tips?: string[];
  concepts_to_revise?: string[];
  delivery_metrics?: {
    words_count?: number;
    speaking_rate_wpm?: number;
    pacing_verdict?: string;
    filler_words?: string[];
    filler_count?: number;
    duration_seconds?: number;
  } | null;
  submitted_at: string;
}

export interface RecommendationItem {
  title: string;
  description: string;
  action_type: "coding" | "resume" | "study" | "interview" | string;
  link: string;
}

export interface InterviewSessionOut {
  id: string;
  user_id: string;
  resume_id?: string | null;
  interview_type: "technical" | "hr" | "behavioral" | "mixed" | string;
  target_role: string;
  experience_level: "Beginner" | "Intermediate" | "Advanced" | string;
  duration_minutes: number;
  custom_skills: string[];
  status: "in_progress" | "completed" | "abandoned" | string;
  total_questions: number;
  current_question_index: number;
  overall_score?: number | null;
  technical_score?: number | null;
  communication_score?: number | null;
  strengths?: string[];
  weaknesses?: string[];
  recommendations?: RecommendationItem[];
  started_at: string;
  ended_at?: string | null;
  questions: QuestionOut[];
}

export interface InterviewSessionListItem {
  id: string;
  interview_type: string;
  target_role: string;
  experience_level: string;
  duration_minutes: number;
  status: string;
  total_questions: number;
  overall_score?: number | null;
  started_at: string;
  ended_at?: string | null;
}

export interface InterviewHistoryResponse {
  total_interviews: number;
  completed_interviews: number;
  average_score: number;
  sessions: InterviewSessionListItem[];
}

export interface InterviewResultsResponse {
  session_id: string;
  interview_type: string;
  target_role: string;
  experience_level: string;
  status: string;
  overall_score: number;
  technical_score: number;
  communication_score: number;
  strengths: string[];
  weaknesses: string[];
  recommendations: RecommendationItem[];
  started_at: string;
  ended_at?: string | null;
  total_questions: number;
  questions: QuestionOut[];
  answers: AnswerOut[];
}

export interface AudioUploadResponse {
  transcript: string;
  duration_seconds: number;
  delivery_metrics: {
    words_count: number;
    speaking_rate_wpm: number;
    pacing_verdict: string;
    filler_words: string[];
    filler_count: number;
    duration_seconds: number;
  };
}
