"use client";

import React, { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import {
  FileText,
  Loader2,
  AlertCircle,
  CheckCircle2,
} from "lucide-react";

interface ResumeItem {
  id: string;
  user_id: string;
  original_filename: string;
  file_size: number;
  mime_type: string;
  created_at: string;
  extraction_status?: string;
  character_count?: number | null;
  word_count?: number | null;
}

interface ResumeListResponse {
  resumes: ResumeItem[];
  total_count: number;
}

interface ResumeSelectorProps {
  selectedResumeId: string | null;
  onSelect: (resumeId: string) => void;
}

export default function ResumeSelector({
  selectedResumeId,
  onSelect,
}: ResumeSelectorProps) {
  const [resumes, setResumes] = useState<ResumeItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchResumes();
  }, []);

  const fetchResumes = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await apiFetch<ResumeListResponse>(
        "/resume/my-resumes"
      );

      setResumes(data.resumes);
    } catch (err: any) {
      setError(err.message || "Failed to load resumes.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="glass-card p-6 space-y-4">
      <div>
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <FileText className="w-5 h-5 text-sky-400" />
          Step 1: Select Your Resume
        </h2>

        <p className="text-sm text-slate-400 mt-1">
          Choose an uploaded resume to compare against the selected job
          description.
        </p>
      </div>

      {isLoading && (
        <div className="flex items-center justify-center py-8 text-slate-400">
          <Loader2 className="w-5 h-5 animate-spin mr-2" />
          Loading your resumes...
        </div>
      )}

      {error && (
        <div className="bg-red-950/80 border border-red-800 text-red-300 p-3 rounded-lg flex items-start gap-2 text-sm">
          <AlertCircle className="w-5 h-5 shrink-0 text-red-400" />
          <span>{error}</span>
        </div>
      )}

      {!isLoading && !error && resumes.length === 0 && (
        <div className="text-center py-8 text-slate-400 text-sm">
          <p>No resumes uploaded yet.</p>
          <p className="mt-1">
            Upload a resume from the Resume page before starting ATS analysis.
          </p>
        </div>
      )}

      {!isLoading && !error && resumes.length > 0 && (
        <div className="space-y-3">
          {resumes.map((resume) => {
            const isSelected = selectedResumeId === resume.id;
            const isReady = resume.extraction_status === "completed";

            return (
              <button
                key={resume.id}
                type="button"
                disabled={!isReady}
                onClick={() => onSelect(resume.id)}
                className={`w-full text-left p-4 rounded-xl border transition ${
                  !isReady
                    ? "border-slate-800 bg-slate-900/50 opacity-60 cursor-not-allowed"
                    : isSelected
                    ? "border-sky-500 bg-sky-950/40"
                    : "border-slate-800 bg-slate-900 hover:border-slate-600"
                }`}
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex items-start gap-3">
                    <div
                      className={`w-10 h-10 rounded-lg flex items-center justify-center shrink-0 ${
                        isSelected
                          ? "bg-sky-900/60 text-sky-300"
                          : "bg-slate-800 text-sky-400"
                      }`}
                    >
                      <FileText className="w-5 h-5" />
                    </div>

                    <div>
                      <h3 className="text-white font-medium">
                        {resume.original_filename}
                      </h3>

                      <p className="text-xs text-slate-500 mt-1">
                        Uploaded on{" "}
                        {new Date(resume.created_at).toLocaleDateString()}
                      </p>

                      {isReady ? (
                        <p className="text-xs text-emerald-400 mt-2">
                          ✓ Text extracted — ready for ATS analysis
                        </p>
                      ) : (
                        <p className="text-xs text-amber-400 mt-2">
                          ⚠ Extract resume text before using ATS analysis
                        </p>
                      )}
                    </div>
                  </div>

                  {isSelected && (
                    <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
                  )}
                </div>
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}