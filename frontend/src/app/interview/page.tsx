"use client";

import React, { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import {
  Sparkles,
  ArrowRight,
  History,
  FileText,
  AlertCircle,
  Sliders,
  CheckCircle2,
  Mic,
} from "lucide-react";
import { InterviewSessionOut } from "@/types/interview";

interface ResumeItem {
  id: string;
  original_filename: string;
  created_at: string;
}

export default function InterviewSetupPage() {
  const router = useRouter();
  const { user, isLoading: authLoading } = useAuth();

  const [interviewType, setInterviewType] = useState<string>("mixed");
  const [targetRole, setTargetRole] = useState<string>("Software Developer");
  const [experienceLevel, setExperienceLevel] = useState<string>("Beginner");
  const [durationMinutes, setDurationMinutes] = useState<number>(15);
  const [skillsInput, setSkillsInput] = useState<string>("");
  const [resumes, setResumes] = useState<ResumeItem[]>([]);
  const [selectedResumeId, setSelectedResumeId] = useState<string>("");

  const [isLoadingResumes, setIsLoadingResumes] = useState<boolean>(false);
  const [resumeError, setResumeError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const loadResumes = useCallback(async () => {
    setIsLoadingResumes(true);
    setResumeError(null);
    try {
      const data = await apiFetch<any>(`/resume/my-resumes?t=${Date.now()}`, {
        cache: "no-store",
      });
      const list: ResumeItem[] = Array.isArray(data) ? data : data?.resumes || [];
      setResumes(list);

      // Re-evaluate selected resume against the fresh list
      setSelectedResumeId((prev) => {
        if (!prev) {
          return list.length > 0 ? list[0].id : "";
        }
        const exists = list.some((r) => r.id === prev);
        if (exists) {
          return prev;
        }
        return list.length > 0 ? list[0].id : "";
      });
    } catch (err: any) {
      setResumeError(err.message || "Failed to load active resumes.");
      setResumes([]);
      setSelectedResumeId("");
    } finally {
      setIsLoadingResumes(false);
    }
  }, []);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push("/login");
      return;
    }

    if (user) {
      loadResumes();

      // Cross-component and cross-tab immediate synchronization
      const handleResumesUpdated = () => {
        loadResumes();
      };

      const handleStorageChange = (e: StorageEvent) => {
        if (e.key === "last_resume_update") {
          loadResumes();
        }
      };

      const handleVisibilityChange = () => {
        if (document.visibilityState === "visible") {
          loadResumes();
        }
      };

      window.addEventListener("resumes_updated", handleResumesUpdated);
      window.addEventListener("storage", handleStorageChange);
      window.addEventListener("focus", handleResumesUpdated);
      document.addEventListener("visibilitychange", handleVisibilityChange);

      return () => {
        window.removeEventListener("resumes_updated", handleResumesUpdated);
        window.removeEventListener("storage", handleStorageChange);
        window.removeEventListener("focus", handleResumesUpdated);
        document.removeEventListener("visibilitychange", handleVisibilityChange);
      };
    } else {
      setResumes([]);
      setSelectedResumeId("");
    }
  }, [user, authLoading, loadResumes, router]);

  const handleStartInterview = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setErrorMsg(null);

    const skills = skillsInput
      .split(",")
      .map((s) => s.trim())
      .filter((s) => s.length > 0);

    try {
      const session = await apiFetch<InterviewSessionOut>("/interviews/sessions", {
        method: "POST",
        body: JSON.stringify({
          interview_type: interviewType,
          target_role: targetRole,
          experience_level: experienceLevel,
          duration_minutes: Number(durationMinutes),
          custom_skills: skills,
          resume_id: selectedResumeId ? selectedResumeId : null,
        }),
      });

      router.push(`/interview/${session.id}`);
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to initialize interview session.");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (authLoading) {
    return (
      <div className="py-20 text-center text-[#8993A0]">
        <div className="w-8 h-8 border-2 border-[#123E63] border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <p className="text-xs font-semibold">Authenticating student session...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Header */}
      <div className="bg-white rounded-2xl p-6 sm:p-7 shadow-card border border-[#E5E9EF] flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#123E63]/10 border border-[#123E63]/20 text-[#123E63] text-xs font-semibold mb-2">
            <Mic className="w-3.5 h-3.5 text-[#F5A623]" />
            AI Mock Interview Studio
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-[#202B38] tracking-tight">
            Interview Simulation Configuration
          </h2>
          <p className="text-xs sm:text-sm text-[#8993A0] mt-1">
            Simulate realistic technical and behavioral interview rounds with automated speech analysis and instant scoring.
          </p>
        </div>

        <Link
          href="/interview/history"
          className="px-4 py-2.5 rounded-xl bg-[#F8F9FA] hover:bg-[#EAEFF5] text-[#123E63] border border-[#E5E9EF] text-xs font-bold transition flex items-center gap-1.5 self-start sm:self-auto shrink-0"
        >
          <History className="w-3.5 h-3.5 text-[#F5A623]" />
          <span>Past Sessions</span>
        </Link>
      </div>

      {errorMsg && (
        <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 flex items-start gap-2.5 text-xs font-semibold">
          <AlertCircle className="w-4 h-4 shrink-0 text-red-500 mt-0.5" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Configuration Form */}
      <form onSubmit={handleStartInterview} className="space-y-6">
        <div className="bg-white rounded-2xl p-6 sm:p-7 shadow-card border border-[#E5E9EF] space-y-6">
          <div className="flex items-center gap-2 border-b border-[#E5E9EF] pb-3">
            <Sliders className="w-4 h-4 text-[#123E63]" />
            <h3 className="text-base font-bold text-[#202B38]">Session Parameters</h3>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <label className="text-[11px] font-bold text-[#8993A0] uppercase tracking-wider block">
                Target Role / Track
              </label>
              <select
                value={targetRole}
                onChange={(e) => setTargetRole(e.target.value)}
                className="w-full bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl px-3.5 py-2.5 text-xs font-medium text-[#202B38] focus:outline-none focus:border-[#123E63]"
              >
                <option value="Software Developer">Software Developer (General SDE)</option>
                <option value="Python Developer">Python Developer</option>
                <option value="Java Developer">Java Developer</option>
                <option value="AI/ML Engineer">AI / ML Engineer</option>
                <option value="Frontend Developer">Frontend Developer</option>
                <option value="Full Stack Developer">Full Stack Developer</option>
              </select>
            </div>

            <div className="space-y-1.5">
              <label className="text-[11px] font-bold text-[#8993A0] uppercase tracking-wider block">
                Interview Type
              </label>
              <select
                value={interviewType}
                onChange={(e) => setInterviewType(e.target.value)}
                className="w-full bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl px-3.5 py-2.5 text-xs font-medium text-[#202B38] focus:outline-none focus:border-[#123E63]"
              >
                <option value="mixed">Mixed (Technical + Behavioral + Project)</option>
                <option value="technical">Technical Only (Data Structures & Systems)</option>
                <option value="behavioral">Behavioral (STAR Method & Problem Solving)</option>
                <option value="hr">HR & Cultural Fit</option>
              </select>
            </div>

            <div className="space-y-1.5">
              <label className="text-[11px] font-bold text-[#8993A0] uppercase tracking-wider block">
                Candidate Level
              </label>
              <select
                value={experienceLevel}
                onChange={(e) => setExperienceLevel(e.target.value)}
                className="w-full bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl px-3.5 py-2.5 text-xs font-medium text-[#202B38] focus:outline-none focus:border-[#123E63]"
              >
                <option value="Beginner">Beginner (College Student / Fresher)</option>
                <option value="Intermediate">Intermediate (1-2 Years / Internships)</option>
                <option value="Advanced">Advanced (Senior / Deep Problem Solving)</option>
              </select>
            </div>

            <div className="space-y-1.5">
              <label className="text-[11px] font-bold text-[#8993A0] uppercase tracking-wider block">
                Session Length
              </label>
              <select
                value={durationMinutes}
                onChange={(e) => setDurationMinutes(Number(e.target.value))}
                className="w-full bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl px-3.5 py-2.5 text-xs font-medium text-[#202B38] focus:outline-none focus:border-[#123E63]"
              >
                <option value={10}>10 Minutes (Quick 3-Question Practice)</option>
                <option value={15}>15 Minutes (Standard 5-Question Session)</option>
                <option value={30}>30 Minutes (Deep Dive 8-Question Session)</option>
              </select>
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="text-[11px] font-bold text-[#8993A0] uppercase tracking-wider block">
              Focus Skills (Optional, comma-separated)
            </label>
            <input
              type="text"
              placeholder="e.g. React, PostgreSQL, Docker, FastApi, System Design"
              value={skillsInput}
              onChange={(e) => setSkillsInput(e.target.value)}
              className="w-full bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl px-3.5 py-2.5 text-xs font-medium text-[#202B38] focus:outline-none focus:border-[#123E63]"
            />
          </div>

          <div className="space-y-2 pt-3 border-t border-[#E5E9EF]">
            <div className="flex items-center justify-between">
              <label className="text-[11px] font-bold text-[#8993A0] uppercase tracking-wider flex items-center gap-1.5">
                <FileText className="w-3.5 h-3.5 text-[#123E63]" />
                Personalize with Uploaded Resume
              </label>
              {isLoadingResumes && (
                <span className="text-[11px] text-[#8993A0] flex items-center gap-1">
                  <span className="w-3 h-3 border-2 border-[#123E63] border-t-transparent rounded-full animate-spin inline-block" />
                  Syncing resumes...
                </span>
              )}
            </div>
            <p className="text-[11px] text-[#8993A0]">
              When selected, questions will directly reference projects and technical experience from your resume.
            </p>

            {resumeError && (
              <div className="p-2.5 rounded-xl bg-red-50 border border-red-200 text-red-600 text-xs flex items-center gap-2">
                <AlertCircle className="w-4 h-4 shrink-0" />
                <span>{resumeError}</span>
              </div>
            )}

            <select
              value={selectedResumeId}
              onChange={(e) => setSelectedResumeId(e.target.value)}
              disabled={isLoadingResumes}
              className="w-full bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl px-3.5 py-2.5 text-xs font-medium text-[#202B38] focus:outline-none focus:border-[#123E63] disabled:opacity-60"
            >
              <option value="">Do not use resume (Generic Questions)</option>
              {resumes.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.original_filename} (Uploaded: {new Date(r.created_at).toLocaleDateString()})
                </option>
              ))}
            </select>

            {resumes.length === 0 && !isLoadingResumes && (
              <div className="p-3 bg-[#F8F9FA] rounded-xl border border-[#E5E9EF] text-xs text-[#8993A0] flex items-center justify-between">
                <span>No active resumes uploaded in your account.</span>
                <Link href="/resume" className="text-[#123E63] font-bold hover:underline">
                  Upload Resume &rarr;
                </Link>
              </div>
            )}
          </div>
        </div>

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isSubmitting}
            className="flex items-center gap-2 bg-[#F5A623] hover:bg-[#E09212] text-white font-bold px-8 py-3 rounded-xl transition shadow-md disabled:opacity-50 text-xs"
          >
            {isSubmitting ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                <span>Generating AI Session...</span>
              </>
            ) : (
              <>
                <span>Begin Mock Interview</span>
                <ArrowRight className="w-4 h-4" />
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
