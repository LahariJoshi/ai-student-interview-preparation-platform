"use client";

import React, { useState, useEffect, useRef } from "react";
import { apiFetch } from "@/lib/api";
import { UploadCloud, FileText, Trash2, CheckCircle2, AlertCircle, Loader2 } from "lucide-react";
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
  }, []);

  const fetchResumes = async () => {
    setIsLoadingList(true);

    try {
      const data = await apiFetch<{
        resumes: ResumeItem[];
        total_count: number;
      }>("/resume/my-resumes");

      setResumes(data.resumes);

      // Check which resumes already have an analysis
      const analysisChecks = await Promise.all(
        data.resumes.map(async (resume) => {
          try {
            await apiFetch(`/resume/${resume.id}/analysis`);
            return resume.id;
          } catch {
            // 404 means this resume has not been analyzed yet
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

    // Client-side pre-validations
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
      const response = await fetch("http://localhost:8000/api/v1/resume/upload", {
        method: "POST",
        body: formData,
        credentials: "include", // Essential for HttpOnly access_token cookie
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Upload failed.");
      }

      const uploadedResume: ResumeItem = await response.json();
      setResumes((prev) => [uploadedResume, ...prev]);
      setSuccess(`Resume '${uploadedResume.original_filename}' uploaded successfully!`);
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
      const extracted = await apiFetch<ResumeItem>(
        `/resume/${resumeId}/extract-text`,
        {
          method: "POST",
        }
      );

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
    <div className="space-y-8 max-w-2xl mx-auto">
      {/* Upload Box */}
      <div className="glass-card p-6 space-y-4">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <UploadCloud className="w-5 h-5 text-sky-400" />
          Upload Student Resume
        </h2>

        {error && (
          <div className="bg-red-950/80 border border-red-800 text-red-300 p-3 rounded-lg flex items-start gap-2 text-sm">
            <AlertCircle className="w-5 h-5 shrink-0 text-red-400 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        {success && (
          <div className="bg-emerald-950/80 border border-emerald-800 text-emerald-300 p-3 rounded-lg flex items-start gap-2 text-sm">
            <CheckCircle2 className="w-5 h-5 shrink-0 text-emerald-400 mt-0.5" />
            <span>{success}</span>
          </div>
        )}

        <div
          onDragEnter={handleDrag}
          onDragOver={handleDrag}
          onDragLeave={handleDrag}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition ${
            dragActive
              ? "border-sky-400 bg-sky-950/40"
              : "border-slate-700 bg-slate-900/50 hover:border-slate-500"
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
              <Loader2 className="w-8 h-8 text-sky-400 animate-spin" />
              <p className="text-slate-300 text-sm font-medium">Uploading & Validating Resume...</p>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center space-y-2">
              <div className="w-12 h-12 rounded-full bg-slate-800 flex items-center justify-center text-sky-400">
                <UploadCloud className="w-6 h-6" />
              </div>
              <div>
                <p className="text-white font-medium text-sm">
                  Click to upload or drag & drop file here
                </p>
                <p className="text-slate-400 text-xs mt-1">
                  Supported Formats: PDF (.pdf) or DOCX (.docx) • Max size: 5 MB
                </p>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Uploaded Resumes List */}
      <div className="glass-card p-6 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <FileText className="w-5 h-5 text-sky-400" />
            Uploaded Resumes ({resumes.length} / 5)
          </h3>
        </div>

        {isLoadingList ? (
          <div className="py-6 text-center text-slate-400 text-sm">Loading uploaded resumes...</div>
        ) : resumes.length === 0 ? (
          <div className="py-6 text-center text-slate-400 text-sm">
            No resumes uploaded yet. Upload a PDF or DOCX file to get started.
          </div>
        ) : (
          <div className="space-y-3">
            {resumes.map((resume) => (
              <div
                key={resume.id}
                className="flex items-center justify-between bg-slate-900 border border-slate-800 p-4 rounded-xl hover:border-slate-700 transition"
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-sky-950/80 border border-sky-800 flex items-center justify-center text-sky-400 shrink-0">
                    <FileText className="w-5 h-5" />
                  </div>
                  <div>
                    <p className="text-white text-sm font-medium">{resume.original_filename}</p>
                    <p className="text-slate-400 text-xs">
                      {formatBytes(resume.file_size)} • Uploaded on{" "}
                      {new Date(resume.created_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                    {resume.extraction_status === "completed" ? (
                      <span className="text-xs text-emerald-400 font-medium">
                        ✓ Text Extracted
                      </span>
                    ) : (
                      <button
                        onClick={() => handleExtractText(resume.id)}
                        disabled={extractingId === resume.id}
                        className="px-3 py-2 rounded-lg bg-sky-600 hover:bg-sky-500 disabled:opacity-50 disabled:cursor-not-allowed text-white text-xs font-medium transition"
                      >
                        {extractingId === resume.id ? (
                          <span className="flex items-center gap-1">
                            <Loader2 className="w-3 h-3 animate-spin" />
                            Extracting...
                          </span>
                        ) : (
                          "Extract Text"
                        )}
                      </button>
                    )}

                    {resume.extraction_status === "completed" && (
                      analyzedIds.has(resume.id) ? (
                        <button
                          onClick={() => setSelectedAnalysisId(resume.id)}
                          className="text-xs text-emerald-400 font-medium hover:text-emerald-300 transition"
                        >
                          ✓ View Analysis
                        </button>
                      ) : (
                        <button
                          onClick={() => handleAnalyzeResume(resume.id)}
                          disabled={analyzingId === resume.id}
                          className="px-3 py-2 rounded-lg bg-violet-600 hover:bg-violet-500 disabled:opacity-50 disabled:cursor-not-allowed text-white text-xs font-medium transition"
                        >
                          {analyzingId === resume.id ? (
                            <span className="flex items-center gap-1">
                              <Loader2 className="w-3 h-3 animate-spin" />
                              Analyzing...
                            </span>
                          ) : (
                            "Analyze Resume"
                          )}
                        </button>
                      )
                    )}

                    <button
                      onClick={() => handleDelete(resume.id)}
                      className="p-2 rounded-lg text-slate-400 hover:text-red-400 hover:bg-slate-800 transition"
                      title="Delete Resume"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
              </div>
            ))}
          </div>
        )}
      </div>
            {selectedAnalysisId && (
        <div className="glass-card p-6">
          <ResumeAnalysis resumeId={selectedAnalysisId} />

          <button
            onClick={() => setSelectedAnalysisId(null)}
            className="mt-4 px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm transition"
          >
            Close Analysis
          </button>
        </div>
      )}
    </div>
  );
}
