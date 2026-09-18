export interface JobDescription {
  id: string;
  user_id: string;
  title: string;
  company_name: string | null;
  description_text: string;
  created_at: string;
  updated_at: string;
}

export interface JobDescriptionCreate {
  title: string;
  company_name?: string;
  description_text: string;
}

export interface JobDescriptionListResponse {
  job_descriptions: JobDescription[];
  total_count: number;
}