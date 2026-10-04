export type InterviewType = "Technical" | "Behavioral" | "HR" | "Mixed";
export type ExperienceLevel = "Fresher" | "Beginner" | "Intermediate";
export type DifficultyLevel = "Easy" | "Medium" | "Hard";
export type AnswerMode = "Voice" | "Text" | "Voice + Text";

export interface InterviewSessionCreate {
  target_role: string;
  interview_type: InterviewType;
  experience_level: ExperienceLevel;
  difficulty: DifficultyLevel;
  question_count: number;
  answer_mode: AnswerMode;
  target_company?: string;
}

export interface InterviewQuestion {
  id: string;
  session_id: string;
  question_order: number;
  category: string;
  topic?: string | null;
  question_text: string;
  expected_points?: string[];
  difficulty?: string | null;
  created_at: string;
}

export interface InterviewResponse {
  id: string;
  session_id: string;
  question_id: string;
  transcribed_text: string;
  audio_file_path?: string | null;
  audio_duration_seconds?: number | null;
  score?: number | null;
  feedback_text?: string | null;
  key_strengths?: string[];
  missing_concepts?: string[];
  created_at: string;
}

export interface InterviewSession {
  id: string;
  user_id: string;
  target_role: string;
  interview_type: InterviewType;
  experience_level: ExperienceLevel;
  difficulty: DifficultyLevel;
  answer_mode: AnswerMode;
  question_count: number;
  target_company?: string | null;
  status: "pending" | "in_progress" | "completed" | "abandoned";
  current_question_index: number;
  overall_score?: number | null;
  technical_score?: number | null;
  communication_score?: number | null;
  created_at: string;
  completed_at?: string | null;
}

export interface InterviewSessionDetail extends InterviewSession {
  questions: InterviewQuestion[];
  responses: InterviewResponse[];
}

export interface VoicePipelineResult {
  response_id: string;
  session_id: string;
  question_id: string;
  transcript: string;
  answer_score: number;
  communication_score: number;
  answer_analysis: {
    score: number;
    technical_score: number;
    relevance_score: number;
    clarity_score: number;
    strengths: string[];
    weaknesses: string[];
    feedback: string[];
    improvements: string[];
  };
  voice_metrics: {
    filler_analysis: {
      filler_word_count: number;
      filler_words: Record<string, number>;
      filler_rate: number;
    };
    speaking_rate: {
      word_count: number;
      duration_seconds: number;
      speech_rate_wpm: number;
    };
    pause_analysis: {
      pause_count: number;
      total_pause_seconds: number;
      average_pause_seconds: number;
      longest_pause_seconds: number;
      data_availability: string;
      is_estimated: boolean;
    };
  };
  communication_feedback: {
    communication_score: number;
    strengths: string[];
    areas_to_improve: string[];
    feedback: string[];
    metrics: Record<string, any>;
  };
  status: string;
}

export interface QuestionPerformance {
  question_id: string;
  question_order: number;
  question_text: string;
  category: string;
  difficulty?: string | null;
  topic?: string | null;
  candidate_answer?: string | null;
  score?: number | null;
  feedback?: string | null;
  strengths: string[];
  weaknesses: string[];
  audio_duration_seconds?: number | null;
  speaking_rate_wpm?: number | null;
  filler_word_count?: number | null;
  clarity_score?: number | null;
}

export interface AggregateVoiceMetrics {
  has_voice_data: boolean;
  average_speaking_rate_wpm: number;
  total_filler_word_count: number;
  filler_words_detected: Record<string, number>;
  average_clarity_score: number;
  total_pause_count: number;
  total_pause_duration_seconds: number;
  tone_evaluation?: string | null;
  communication_feedback: string[];
}

export interface InterviewResultData {
  session_id: string;
  target_role: string;
  interview_type: string;
  experience_level: string;
  difficulty: string;
  status: string;
  interview_score: number;
  technical_score: number;
  communication_score: number;
  total_questions: number;
  answered_questions: number;
  interview_duration_seconds: number;
  formatted_duration: string;
  summary: string;
  strengths: string[];
  weaknesses: string[];
  answer_feedback: string[];
  recommendations: string[];
  voice_metrics: AggregateVoiceMetrics;
  question_performance: QuestionPerformance[];
  created_at: string;
  completed_at?: string | null;
}

export interface InterviewHistoryItem {
  id: string;
  date: string;
  created_at: string;
  completed_at?: string | null;
  target_role: string;
  interview_type: InterviewType | string;
  experience_level?: ExperienceLevel | string | null;
  difficulty?: DifficultyLevel | string | null;
  status: "pending" | "in_progress" | "completed" | "abandoned" | string;
  number_of_questions: number;
  question_count: number;
  overall_score?: number | null;
  technical_score?: number | null;
  communication_score?: number | null;
  duration?: string;
  formatted_duration: string;
  duration_seconds: number;
}

export interface InterviewHistoryPagination {
  items: InterviewHistoryItem[];
  total: number;
  skip: number;
  limit: number;
  page: number;
  total_pages: number;
}


