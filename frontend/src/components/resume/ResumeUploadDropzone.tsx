"use client";

import React, { useState, useEffect, useRef } from "react";
import { apiFetch, getApiBaseUrl } from "@/lib/api";
import {
  UploadCloud,
  FileText,
  Trash2,
  CheckCircle2,
  AlertCircle,
  Loader2,
  Sparkles,
  Search,
  ExternalLink,
} from "lucide-react";
import ResumeAnalysis from "./ResumeAnalysis";

export interface ResumeItem {
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

export default function ResumeUploadDropzone() {
  const [resumes, setResumes] = useState<ResumeItem[]>([]);
  const [selectedAnalysisId, setSelectedAnalysisId] = useState<string | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [extractingId, setExtractingId] = useState<string | null>(null);
  const [analyzingId, setAnalyzingId] = useState<string | null>(null);
  const [analyzedIds, setAnalyzedIds] = useState<Set<string>>(new Set());
  const [isLoadingList, setIsLoadingList] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

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
  }, []);

  const fetchResumes = async () => {
    setIsLoadingList(true);
    try {
      const data = await apiFetch<{
        resumes: ResumeItem[];
        total_count: number;
      }>(`/resume/my-resumes?t=${Date.now()}`);

      setResumes(data.resumes || []);

      const analysisChecks = await Promise.all(
        (data.resumes || []).map(async (resume) => {
          try {
            await apiFetch(`/resume/${resume.id}/analysis`);
            return resume.id;
          } catch {
            return null;
          }
        })
      );

      const completedAnalysisIds = new Set(
        analysisChecks.filter((id): id is string => id !== null)
      );

      setAnalyzedIds(completedAnalysisIds);
    } catch (err: any) {
      setError(err.message || "Failed to load resumes.");
    } finally {
      setIsLoadingList(false);
    }
  };

  const handleFile = async (file: File) => {
    setError(null);
    setSuccess(null);

    const ext = file.name.split(".").pop()?.toLowerCase();
    if (ext !== "pdf" && ext !== "docx") {
      setError("Invalid file type. Only PDF (.pdf) and DOCX (.docx) files are supported.");
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      setError("File size exceeds maximum allowed limit of 5 MB.");
      return;
    }

    if (resumes.length >= 5) {
      setError("Maximum limit of 5 uploaded resumes reached. Delete an existing resume first.");
      return;
    }

    setIsUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`${getApiBaseUrl()}/resume/upload`, {
        method: "POST",
        body: formData,
        credentials: "include",
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Upload failed.");
      }

      const uploadedResume: ResumeItem = await response.json();
      setResumes((prev) => [uploadedResume, ...prev]);
      setSuccess(`Resume '${uploadedResume.original_filename}' uploaded successfully!`);
      if (typeof window !== "undefined") {
        window.dispatchEvent(new CustomEvent("resumes_updated", { detail: { action: "upload", resume: uploadedResume } }));
        localStorage.setItem("last_resume_update", Date.now().toString());
      }
    } catch (err: any) {
      setError(err.message || "An error occurred during resume upload.");
    } finally {
      setIsUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  const handleExtractText = async (resumeId: string) => {
    setError(null);
    setSuccess(null);
    setExtractingId(resumeId);

    try {
      const extracted = await apiFetch<ResumeItem>(`/resume/${resumeId}/extract-text`, {
        method: "POST",
      });

      setResumes((prev) =>
        prev.map((resume) =>
          resume.id === resumeId
            ? {
                ...resume,
                extraction_status: extracted.extraction_status,
                character_count: extracted.character_count,
                word_count: extracted.word_count,
              }
            : resume
        )
      );

      setSuccess("Resume text extracted successfully.");
    } catch (err: any) {
      setError(err.message || "Failed to extract resume text.");
    } finally {
      setExtractingId(null);
    }
  };

  const handleAnalyzeResume = async (resumeId: string) => {
    setError(null);
    setSuccess(null);
    setAnalyzingId(resumeId);

    try {
      await apiFetch(`/resume/${resumeId}/analyze`, {
        method: "POST",
      });

      setAnalyzedIds((prev) => {
        const updated = new Set(prev);
        updated.add(resumeId);
        return updated;
      });

      setSelectedAnalysisId(resumeId);
      setSuccess("Resume analysis completed successfully.");
    } catch (err: any) {
      setError(err.message || "Failed to analyze resume.");
    } finally {
      setAnalyzingId(null);
    }
  };

  const handleDelete = async (resumeId: string) => {
    setError(null);
    setSuccess(null);
    try {
      await apiFetch(`/resume/${resumeId}`, { method: "DELETE" });
      setResumes((prev) => prev.filter((r) => r.id !== resumeId));
      if (selectedAnalysisId === resumeId) {
        setSelectedAnalysisId(null);
      }
      if (typeof window !== "undefined") {
        window.dispatchEvent(new CustomEvent("resumes_updated", { detail: { action: "delete", resumeId } }));
        localStorage.setItem("last_resume_update", Date.now().toString());
      }
      setSuccess("Resume deleted successfully.");
    } catch (err: any) {
      setError(err.message || "Failed to delete resume.");
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const formatBytes = (bytes: number) => {
    if (bytes < 1024) return bytes + " Bytes";
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / (1024 * 1024)).toFixed(2) + " MB";
  };

  return (
    <div className="space-y-6">
      {/* Upload Box */}
      <div className="bg-white rounded-2xl p-6 shadow-card border border-[#E5E9EF] space-y-4">
        <h3 className="text-base font-bold text-[#202B38] flex items-center gap-2">
          <UploadCloud className="w-5 h-5 text-[#123E63]" />
          <span>Upload Student Resume File</span>
        </h3>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 p-3.5 rounded-xl flex items-start gap-2 text-xs">
            <AlertCircle className="w-4 h-4 shrink-0 text-red-500 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        {success && (
          <div className="bg-emerald-50 border border-emerald-200 text-emerald-700 p-3.5 rounded-xl flex items-start gap-2 text-xs">
            <CheckCircle2 className="w-4 h-4 shrink-0 text-emerald-600 mt-0.5" />
            <span>{success}</span>
          </div>
        )}

        <div
          onDragEnter={handleDrag}
          onDragOver={handleDrag}
          onDragLeave={handleDrag}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`border-2 border-dashed rounded-2xl p-8 sm:p-10 text-center cursor-pointer transition ${
            dragActive
              ? "border-[#F5A623] bg-[#FFF6E8]"
              : "border-[#BCD3E6] bg-[#F8F9FA] hover:border-[#123E63] hover:bg-[#F0F5FA]"
          }`}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.docx"
            onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
            className="hidden"
          />

          {isUploading ? (
            <div className="flex flex-col items-center justify-center space-y-2 py-4">
              <Loader2 className="w-8 h-8 text-[#123E63] animate-spin" />
              <p className="text-[#202B38] text-xs font-bold">Uploading & Validating Document...</p>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center space-y-2">
              <div className="w-12 h-12 rounded-full bg-[#123E63]/10 flex items-center justify-center text-[#123E63]">
                <UploadCloud className="w-6 h-6" />
              </div>
              <div>
                <p className="text-[#202B38] font-bold text-sm">
                  Click to select or drag and drop your resume file
                </p>
                <p className="text-[#8993A0] text-xs mt-1">
                  Supported formats: PDF (.pdf) or Word (.docx) &bull; Maximum file size: 5 MB
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Uploaded Resumes List */}
      <div className="bg-white rounded-2xl p-6 shadow-card border border-[#E5E9EF] space-y-4">
        <div className="flex items-center justify-between border-b border-[#E5E9EF] pb-3">
          <h3 className="text-base font-bold text-[#202B38] flex items-center gap-2">
            <FileText className="w-4 h-4 text-[#123E63]" />
            <span>Saved Resumes ({resumes.length} / 5)</span>
          </h3>
          <span className="text-xs text-[#8993A0]">Up to 5 stored drafts</span>
        </div>

        {isLoadingList ? (
          <div className="py-6 text-center text-[#8993A0] text-xs">Loading stored resumes...</div>
        ) : resumes.length === 0 ? (
          <div className="py-8 text-center text-[#8993A0] text-xs space-y-2">
            <FileText className="w-8 h-8 text-[#BCD3E6] mx-auto" />
            <p className="font-semibold text-[#202B38]">No resumes stored yet</p>
            <p>Upload your resume above to extract text and generate ATS evaluations.</p>
          </div>
        ) : (
          <div className="space-y-3">
            {resumes.map((resume) => (
              <div
                key={resume.id}
                className="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-xl border border-[#E5E9EF] bg-[#F8F9FA] hover:bg-white hover:border-[#BCD3E6] transition gap-3"
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-[#123E63] text-white flex items-center justify-center shrink-0 shadow-xs">
                    <FileText className="w-5 h-5 text-[#F5A623]" />
                  </div>
                  <div>
                    <p className="text-[#202B38] text-xs font-bold truncate max-w-[280px]">
                      {resume.original_filename}
                    </p>
                    <p className="text-[#8993A0] text-[11px] mt-0.5">
                      {formatBytes(resume.file_size)} &bull; Uploaded{" "}
                      {new Date(resume.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2 self-end sm:self-auto">
                  {resume.extraction_status === "completed" ? (
                    <span className="text-[11px] text-emerald-600 font-bold bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-200">
                      ✓ Text Ready
                    </span>
                  ) : (
                    <button
                      onClick={() => handleExtractText(resume.id)}
                      disabled={extractingId === resume.id}
                      className="px-3 py-1.5 rounded-lg bg-[#123E63] hover:bg-[#0D3557] disabled:opacity-50 text-white text-xs font-bold transition flex items-center gap-1"
                    >
                      {extractingId === resume.id && (
                        <Loader2 className="w-3 h-3 animate-spin" />
                      )}
                      <span>Extract</span>
                    </button>
                  )}

                  {resume.extraction_status === "completed" && (
                    analyzedIds.has(resume.id) ? (
                      <button
                        onClick={() => setSelectedAnalysisId(resume.id)}
                        className="px-3 py-1.5 rounded-lg bg-[#FFF6E8] hover:bg-[#FFECC7] text-[#F5A623] border border-[#F5A623]/30 text-xs font-bold transition flex items-center gap-1"
                      >
                        <Sparkles className="w-3 h-3" />
                        <span>View Analysis</span>
                      </button>
                    ) : (
                      <button
                        onClick={() => handleAnalyzeResume(resume.id)}
                        disabled={analyzingId === resume.id}
                        className="px-3 py-1.5 rounded-lg bg-[#F5A623] hover:bg-[#E09212] disabled:opacity-50 text-white text-xs font-bold transition flex items-center gap-1 shadow-xs"
                      >
                        {analyzingId === resume.id && (
                          <Loader2 className="w-3 h-3 animate-spin" />
                        )}
                        <span>Analyze</span>
                      </button>
                    )
                  )}

                  <button
                    onClick={() => handleDelete(resume.id)}
                    className="p-1.5 rounded-lg text-[#8993A0] hover:text-red-600 hover:bg-red-50 transition"
                    title="Delete resume"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Analysis Section Details */}
      {selectedAnalysisId && (
        <div className="bg-white rounded-2xl p-6 sm:p-7 shadow-card border border-[#E5E9EF] space-y-4">
          <div className="flex items-center justify-between border-b border-[#E5E9EF] pb-3">
            <h3 className="text-base font-bold text-[#202B38] flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-[#F5A623]" />
              <span>Full Resume Structural Analysis</span>
            </h3>
            <button
              onClick={() => setSelectedAnalysisId(null)}
              className="text-xs font-semibold text-[#8993A0] hover:text-[#202B38]"
            >
              ✕ Close
            </button>
          </div>

          <ResumeAnalysis resumeId={selectedAnalysisId} />
        </div>
      )}
    </div>
  );
}
