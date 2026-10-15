"use client";

import React, { useState, useEffect } from "react";
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
  Briefcase,
  Sliders,
  CheckCircle2,
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
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push("/login");
      return;
    }

    if (user) {
      loadResumes();
    }
  }, [user, authLoading]);

  const loadResumes = async () => {
    setIsLoadingResumes(true);
    try {
      const data = await apiFetch<ResumeItem[]>("/resume");
      setResumes(data || []);
      if (data && data.length > 0) {
        setSelectedResumeId(data[0].id);
      }
    } catch (e) {
      // Non-fatal if student has not uploaded a resume yet
    } finally {
      setIsLoadingResumes(false);
    }
  };

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
      <div className="py-20 text-center text-slate-400">
        <div className="w-8 h-8 border-2 border-sky-400 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
        Checking credentials...
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto py-4 space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-sky-950/80 border border-sky-800 text-sky-300 text-xs font-semibold mb-2">
            <Sparkles className="w-3.5 h-3.5 text-sky-400" />
            AI Placement Preparation
          </div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">
            AI Mock Interview Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Configure your personalized mock interview session tailored to your target role, difficulty, and resume.
          </p>
        </div>

        <Link
          href="/interview/history"
          className="inline-flex items-center gap-2 px-4 py-2 bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 text-sm font-medium rounded-xl transition"
        >
          <History className="w-4 h-4 text-sky-400" />
          <span>Past Sessions & Trends</span>
        </Link>
      </div>

      {errorMsg && (
        <div className="p-4 rounded-xl bg-rose-950/50 border border-rose-800 text-rose-300 flex items-start gap-3 text-sm">
          <AlertCircle className="w-5 h-5 flex-shrink-0 mt-0.5" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Configuration Form */}
      <form onSubmit={handleStartInterview} className="space-y-6">
        <div className="glass-card p-6 md:p-8 space-y-6">
          <h2 className="text-lg font-bold text-white flex items-center gap-2 border-b border-slate-800 pb-3">
            <Sliders className="w-5 h-5 text-sky-400" />
            Interview Parameters
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Target Role */}
            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-300">
                Target Role / Job Title
              </label>
              <select
                value={targetRole}
                onChange={(e) => setTargetRole(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-sky-500 text-sm"
              >
                <option value="Software Developer">Software Developer (General SDE)</option>
                <option value="Python Developer">Python Developer</option>
                <option value="Java Developer">Java Developer</option>
                <option value="AI/ML Engineer">AI / ML Engineer</option>
                <option value="Frontend Developer">Frontend Developer</option>
                <option value="Full Stack Developer">Full Stack Developer</option>
              </select>
            </div>

            {/* Interview Type */}
            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-300">
                Interview Type
              </label>
              <select
                value={interviewType}
                onChange={(e) => setInterviewType(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-sky-500 text-sm"
              >
                <option value="mixed">Mixed (Technical + Behavioral + Project)</option>
                <option value="technical">Technical Only (Core CS & Architecture)</option>
                <option value="behavioral">Behavioral (STAR Method & Collaboration)</option>
                <option value="hr">HR & Cultural Fit</option>
              </select>
            </div>

            {/* Experience Level */}
            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-300">
                Experience Level
              </label>
              <select
                value={experienceLevel}
                onChange={(e) => setExperienceLevel(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-sky-500 text-sm"
              >
                <option value="Beginner">Beginner (College Student / Fresher)</option>
                <option value="Intermediate">Intermediate (1-2 Years / Internships)</option>
                <option value="Advanced">Advanced (Senior / Deep Problem Solving)</option>
              </select>
            </div>

            {/* Duration */}
            <div className="space-y-2">
              <label className="text-sm font-medium text-slate-300">
                Interview Duration
              </label>
              <select
                value={durationMinutes}
                onChange={(e) => setDurationMinutes(Number(e.target.value))}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-sky-500 text-sm"
              >
                <option value={10}>10 Minutes (Quick 3-Question Practice)</option>
                <option value={15}>15 Minutes (Standard 5-Question Session)</option>
                <option value={30}>30 Minutes (Deep Dive 8-Question Session)</option>
              </select>
            </div>
          </div>

          {/* Custom Skills */}
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-300">
              Focus Skills or Technologies (Optional, comma-separated)
            </label>
            <input
              type="text"
              placeholder="e.g. React, PostgreSQL, Docker, FastApi, System Design"
              value={skillsInput}
              onChange={(e) => setSkillsInput(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500 text-sm"
            />
          </div>

          {/* Optional Resume Linkage */}
          <div className="space-y-3 pt-2 border-t border-slate-800">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                  <FileText className="w-4 h-4 text-sky-400" />
                  Personalize with Uploaded Resume
                </h3>
                <p className="text-xs text-slate-400">
                  When selected, questions will directly incorporate projects and technical proficiencies from your resume.
                </p>
              </div>
            </div>

            {resumes.length > 0 ? (
              <select
                value={selectedResumeId}
                onChange={(e) => setSelectedResumeId(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:border-sky-500"
              >
                <option value="">Do not use resume (Generic Questions)</option>
                {resumes.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.original_filename} (Uploaded: {new Date(r.created_at).toLocaleDateString()})
                  </option>
                ))}
              </select>
            ) : (
              <div className="p-3 bg-slate-900/60 rounded-lg border border-slate-800 text-xs text-slate-400 flex items-center justify-between">
                <span>No uploaded resume found.</span>
                <Link href="/resume" className="text-sky-400 hover:underline">
                  Upload Resume &rarr;
                </Link>
              </div>
            )}
          </div>
        </div>

        {/* Submit */}
        <div className="flex justify-end">
          <button
            type="submit"
            disabled={isSubmitting}
            className="flex items-center gap-2 bg-sky-600 hover:bg-sky-500 text-white font-medium px-8 py-3 rounded-xl transition shadow-lg shadow-sky-950 disabled:opacity-50"
          >
            {isSubmitting ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                <span>Generating Interview Room...</span>
              </>
            ) : (
              <>
                <span>Begin Mock Interview</span>
                <ArrowRight className="w-5 h-5" />
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
