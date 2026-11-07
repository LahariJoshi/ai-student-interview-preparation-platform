"use client";

import React, { useEffect, useState, useCallback } from "react";
import { apiFetch } from "@/lib/api";
import { FileText, Loader2, AlertCircle, CheckCircle2 } from "lucide-react";

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

  const fetchResumes = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await apiFetch<ResumeListResponse>(`/resume/my-resumes?t=${Date.now()}`, {
        cache: "no-store",
      });
      const list = data.resumes || [];
      setResumes(list);
      if (list.length === 0) {
        onSelect("");
      } else if (!selectedResumeId || !list.some((r) => r.id === selectedResumeId)) {
        onSelect(list[0].id);
      }
    } catch (err: any) {
      setError(err.message || "Failed to load resumes.");
      setResumes([]);
      onSelect("");
    } finally {
      setIsLoading(false);
    }
  }, [selectedResumeId, onSelect]);

  useEffect(() => {
    fetchResumes();

    const handleResumesUpdated = () => {
      fetchResumes();
    };

    const handleStorageChange = (e: StorageEvent) => {
      if (e.key === "last_resume_update") {
        fetchResumes();
      }
    };

    window.addEventListener("resumes_updated", handleResumesUpdated);
    window.addEventListener("storage", handleStorageChange);
    window.addEventListener("focus", handleResumesUpdated);

    return () => {
      window.removeEventListener("resumes_updated", handleResumesUpdated);
      window.removeEventListener("storage", handleStorageChange);
      window.removeEventListener("focus", handleResumesUpdated);
    };
  }, [fetchResumes]);

  return (
    <div className="bg-white rounded-2xl p-6 shadow-card border border-[#E5E9EF] space-y-4">
      <div className="flex items-center justify-between border-b border-[#E5E9EF] pb-3">
        <div className="flex items-center gap-2">
          <FileText className="w-4 h-4 text-[#123E63]" />
          <h3 className="text-base font-bold text-[#202B38]">1. Select Resume</h3>
        </div>
        <span className="text-xs text-[#8993A0]">{resumes.length} available</span>
      </div>

      {isLoading ? (
        <div className="py-6 text-center text-[#8993A0] text-xs">Loading resumes...</div>
      ) : error ? (
        <div className="p-3 rounded-xl bg-red-50 text-red-600 text-xs">{error}</div>
      ) : resumes.length === 0 ? (
        <div className="py-6 text-center text-[#8993A0] text-xs">
          No resumes uploaded yet. Go to Resume Analysis to upload one.
        </div>
      ) : (
        <div className="space-y-2 max-h-[220px] overflow-y-auto pr-1">
          {resumes.map((resume) => {
            const isSelected = selectedResumeId === resume.id;
            return (
              <div
                key={resume.id}
                onClick={() => onSelect(resume.id)}
                className={`p-3 rounded-xl border cursor-pointer transition flex items-center justify-between text-xs ${
                  isSelected
                    ? "bg-[#FFF6E8] border-[#F5A623] shadow-xs"
                    : "bg-[#F8F9FA] border-[#E5E9EF] hover:border-[#BCD3E6]"
                }`}
              >
                <div className="flex items-center gap-2.5 truncate">
                  <FileText className={`w-4 h-4 shrink-0 ${isSelected ? "text-[#F5A623]" : "text-[#123E63]"}`} />
                  <span className="font-bold text-[#202B38] truncate">{resume.original_filename}</span>
                </div>
                {isSelected && (
                  <CheckCircle2 className="w-4 h-4 text-[#F5A623] shrink-0" />
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
