"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";
import {
  InterviewSession,
  InterviewType,
  ExperienceLevel,
  DifficultyLevel,
  AnswerMode,
} from "@/types/interview";
import {
  Sparkles,
  Briefcase,
  Code2,
  Users,
  Building2,
  Mic,
  FileText,
  Radio,
  Layers,
  Flame,
  AlertCircle,
  Loader2,
  ArrowRight,
  ShieldCheck,
} from "lucide-react";

interface ProfileData {
  target_role?: string;
  experience_level?: string;
}

export default function InterviewSetup() {
  const router = useRouter();

  // Form State
  const [targetRole, setTargetRole] = useState("");
  const [targetCompany, setTargetCompany] = useState("");
  const [interviewType, setInterviewType] = useState<InterviewType>("Technical");
  const [experienceLevel, setExperienceLevel] = useState<ExperienceLevel>("Fresher");
  const [difficulty, setDifficulty] = useState<DifficultyLevel>("Medium");
  const [questionCount, setQuestionCount] = useState<number>(5);
  const [answerMode, setAnswerMode] = useState<AnswerMode>("Voice + Text");

  // UX State
  const [isLoadingProfile, setIsLoadingProfile] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [validationError, setValidationError] = useState<string | null>(null);
  const [apiError, setApiError] = useState<string | null>(null);

  // Attempt to pre-fill from user's profile
  useEffect(() => {
    let isMounted = true;
    const loadProfile = async () => {
      try {
        setIsLoadingProfile(true);
        const profile = await apiFetch<ProfileData>("/profile");
        if (isMounted && profile) {
          if (profile.target_role) {
            setTargetRole((prev) => prev || profile.target_role || "");
          }
          if (profile.experience_level) {
            const exp = profile.experience_level.toLowerCase();
            if (exp.includes("fresher") || exp.includes("0-1")) {
              setExperienceLevel("Fresher");
            } else if (exp.includes("beginner") || exp.includes("1-2")) {
              setExperienceLevel("Beginner");
            } else if (exp.includes("mid") || exp.includes("intermediate") || exp.includes("3+")) {
              setExperienceLevel("Intermediate");
            }
          }
        }
      } catch {
        // Non-critical: profile might be empty, ignore error
      } finally {
        if (isMounted) {
          setIsLoadingProfile(false);
        }
      }
    };
    loadProfile();
    return () => {
      isMounted = false;
    };
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isSubmitting) return;

    setValidationError(null);
    setApiError(null);

    // Form Validation
    const trimmedRole = targetRole.trim();
    if (!trimmedRole) {
      setValidationError("Please enter your target role (e.g., Frontend Engineer, Data Analyst).");
      return;
    }
    if (trimmedRole.length < 2) {
      setValidationError("Target role must be at least 2 characters.");
      return;
    }

    try {
      setIsSubmitting(true);

      const session = await apiFetch<InterviewSession>("/interview/sessions", {
        method: "POST",
        body: JSON.stringify({
          target_role: trimmedRole,
          target_company: targetCompany.trim() || undefined,
          interview_type: interviewType,
          experience_level: experienceLevel,
          difficulty: difficulty,
          question_count: questionCount,
          answer_mode: answerMode,
        }),
      });

      // Redirect to the interview session page
      router.push(`/interview/session/${session.id}`);
    } catch (err: any) {
      setApiError(err.message || "Failed to create interview session. Please try again.");
      setIsSubmitting(false);
    }
  };

  const interviewTypes: { type: InterviewType; label: string; desc: string; icon: any }[] = [
    {
      type: "Technical",
      label: "Technical",
      desc: "Coding fundamentals, system design, and architecture",
      icon: Code2,
    },
    {
      type: "Behavioral",
      label: "Behavioral",
      desc: "STAR format, workplace scenarios, and team collaboration",
      icon: Users,
    },
    {
      type: "HR",
      label: "HR & Culture",
      desc: "Cultural fit, career goals, and workplace values",
      icon: Briefcase,
    },
    {
      type: "Mixed",
      label: "Mixed Round",
      desc: "Combination of technical deep-dive and behavioral questions",
      icon: Sparkles,
    },
  ];

  const experienceLevels: { level: ExperienceLevel; label: string; sub: string }[] = [
    { level: "Fresher", label: "Fresher", sub: "0 years / College Grad" },
    { level: "Beginner", label: "Beginner", sub: "1–2 years experience" },
    { level: "Intermediate", label: "Intermediate", sub: "3–5 years experience" },
  ];

  const difficulties: { diff: DifficultyLevel; label: string; color: string }[] = [
    { diff: "Easy", label: "Easy", color: "text-emerald-400 border-emerald-500/30" },
    { diff: "Medium", label: "Medium", color: "text-amber-400 border-amber-500/30" },
    { diff: "Hard", label: "Hard", color: "text-rose-400 border-rose-500/30" },
  ];

  const questionCounts = [5, 10, 15];

  const answerModes: { mode: AnswerMode; label: string; icon: any; note: string }[] = [
    {
      mode: "Voice",
      label: "Voice",
      icon: Mic,
      note: "Speak answers via microphone with live speech analysis",
    },
    {
      mode: "Text",
      label: "Text",
      icon: FileText,
      note: "Type your responses directly in the text editor",
    },
    {
      mode: "Voice + Text",
      label: "Voice + Text",
      icon: Radio,
      note: "Full AI voice recording plus editable transcription",
    },
  ];

  return (
    <div className="max-w-3xl mx-auto py-6 px-4">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center gap-2 text-sky-400 text-sm font-semibold mb-2">
          <Sparkles className="w-4 h-4" />
          <span>AI Interview Simulation</span>
        </div>
        <h1 className="text-3xl font-extrabold text-white tracking-tight">Configure Your Interview</h1>
        <p className="text-slate-400 text-sm mt-1">
          Customize the role, difficulty, and format to simulate real placement rounds.
        </p>
      </div>

      {/* Error Banners */}
      {validationError && (
        <div className="mb-6 p-4 rounded-xl bg-amber-950/40 border border-amber-500/40 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-amber-400 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-amber-200">{validationError}</div>
        </div>
      )}

      {apiError && (
        <div className="mb-6 p-4 rounded-xl bg-rose-950/40 border border-rose-500/40 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-rose-400 flex-shrink-0 mt-0.5" />
          <div className="text-sm text-rose-200">{apiError}</div>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-8">
        {/* 1. Target Role & Company */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
            <Briefcase className="w-5 h-5 text-sky-400" />
            Target Role & Company
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label htmlFor="target-role" className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                Target Role <span className="text-rose-400">*</span>
              </label>
              <input
                id="target-role"
                type="text"
                value={targetRole}
                onChange={(e) => setTargetRole(e.target.value)}
                placeholder="e.g. Fullstack Engineer, Data Analyst"
                disabled={isSubmitting}
                className="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500 transition text-sm"
              />
              {isLoadingProfile && (
                <p className="text-xs text-slate-500 mt-1 flex items-center gap-1">
                  <Loader2 className="w-3 h-3 animate-spin" /> Loading from profile...
                </p>
              )}
            </div>

            <div>
              <label htmlFor="target-company" className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
                Target Company <span className="text-slate-500 font-normal">(Optional)</span>
              </label>
              <div className="relative">
                <Building2 className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
                <input
                  id="target-company"
                  type="text"
                  value={targetCompany}
                  onChange={(e) => setTargetCompany(e.target.value)}
                  placeholder="e.g. Google, Amazon, Startup"
                  disabled={isSubmitting}
                  className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500 transition text-sm"
                />
              </div>
            </div>
          </div>
        </div>

        {/* 2. Interview Type */}
        <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-sm">
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-4">
            Interview Type <span className="text-rose-400">*</span>
          </label>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {interviewTypes.map(({ type, label, desc, icon: Icon }) => {
              const isSelected = interviewType === type;
              return (
                <button
                  type="button"
                  key={type}
                  onClick={() => setInterviewType(type)}
                  disabled={isSubmitting}
                  className={`text-left p-4 rounded-xl border transition flex items-start gap-3 ${
                    isSelected
                      ? "bg-sky-950/40 border-sky-500/80 ring-1 ring-sky-500"
                      : "bg-slate-950/60 border-slate-800 hover:border-slate-700 text-slate-300"
                  }`}
                >
                  <div
                    className={`p-2 rounded-lg ${
                      isSelected ? "bg-sky-500/20 text-sky-400" : "bg-slate-800 text-slate-400"
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                  </div>
                  <div>
                    <div className={`font-semibold text-sm ${isSelected ? "text-sky-300" : "text-white"}`}>
                      {label}
                    </div>
                    <div className="text-xs text-slate-400 mt-1 leading-relaxed">{desc}</div>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* 3. Experience Level & Difficulty */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Experience Level */}
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-sm">
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-3 flex items-center gap-1.5">
              <Layers className="w-4 h-4 text-sky-400" />
              Experience Level
            </label>
            <div className="space-y-2">
              {experienceLevels.map(({ level, label, sub }) => {
                const isSelected = experienceLevel === level;
                return (
                  <button
                    type="button"
                    key={level}
                    onClick={() => setExperienceLevel(level)}
                    disabled={isSubmitting}
                    className={`w-full text-left px-4 py-3 rounded-xl border transition flex items-center justify-between ${
                      isSelected
                        ? "bg-sky-950/40 border-sky-500/80 text-white"
                        : "bg-slate-950/60 border-slate-800 hover:border-slate-700 text-slate-300"
                    }`}
                  >
                    <div>
                      <div className="font-semibold text-sm">{label}</div>
                      <div className="text-xs text-slate-400">{sub}</div>
                    </div>
                    <div
                      className={`w-4 h-4 rounded-full border flex items-center justify-center ${
                        isSelected ? "border-sky-400 bg-sky-400" : "border-slate-600"
                      }`}
                    >
                      {isSelected && <div className="w-1.5 h-1.5 rounded-full bg-slate-950" />}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Difficulty */}
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-sm">
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-3 flex items-center gap-1.5">
              <Flame className="w-4 h-4 text-sky-400" />
              Difficulty Level
            </label>
            <div className="space-y-2">
              {difficulties.map(({ diff, label, color }) => {
                const isSelected = difficulty === diff;
                return (
                  <button
                    type="button"
                    key={diff}
                    onClick={() => setDifficulty(diff)}
                    disabled={isSubmitting}
                    className={`w-full text-left px-4 py-3 rounded-xl border transition flex items-center justify-between ${
                      isSelected
                        ? `bg-slate-800/90 ${color} ring-1 ring-current`
                        : "bg-slate-950/60 border-slate-800 hover:border-slate-700 text-slate-300"
                    }`}
                  >
                    <span className="font-semibold text-sm">{label}</span>
                    <div
                      className={`w-4 h-4 rounded-full border flex items-center justify-center ${
                        isSelected ? "border-current bg-current" : "border-slate-600"
                      }`}
                    >
                      {isSelected && <div className="w-1.5 h-1.5 rounded-full bg-slate-950" />}
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* 4. Question Count & Answer Mode */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Question Count */}
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-sm">
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-3">
              Number of Questions
            </label>
            <div className="grid grid-cols-3 gap-3">
              {questionCounts.map((count) => {
                const isSelected = questionCount === count;
                return (
                  <button
                    type="button"
                    key={count}
                    onClick={() => setQuestionCount(count)}
                    disabled={isSubmitting}
                    className={`py-3 rounded-xl border font-bold text-center transition ${
                      isSelected
                        ? "bg-sky-600 border-sky-500 text-white shadow-lg shadow-sky-600/30"
                        : "bg-slate-950/60 border-slate-800 hover:border-slate-700 text-slate-300"
                    }`}
                  >
                    <div className="text-lg">{count}</div>
                    <div className="text-xs font-normal text-slate-400">Questions</div>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Answer Mode */}
          <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-sm">
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-3 flex items-center gap-1.5">
              <Radio className="w-4 h-4 text-sky-400" />
              Answer Mode
            </label>
            <div className="space-y-2">
              {answerModes.map(({ mode, label, icon: Icon, note }) => {
                const isSelected = answerMode === mode;
                return (
                  <button
                    type="button"
                    key={mode}
                    onClick={() => setAnswerMode(mode)}
                    disabled={isSubmitting}
                    className={`w-full text-left px-3.5 py-2.5 rounded-xl border transition flex items-center justify-between ${
                      isSelected
                        ? "bg-sky-950/40 border-sky-500 text-white"
                        : "bg-slate-950/60 border-slate-800 hover:border-slate-700 text-slate-300"
                    }`}
                  >
                    <div className="flex items-center gap-2.5">
                      <Icon className={`w-4 h-4 ${isSelected ? "text-sky-400" : "text-slate-400"}`} />
                      <div>
                        <div className="font-semibold text-xs">{label}</div>
                        <div className="text-[11px] text-slate-400">{note}</div>
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <div className="pt-2">
          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full py-4 px-6 rounded-xl bg-gradient-to-r from-sky-600 to-indigo-600 hover:from-sky-500 hover:to-indigo-500 text-white font-bold text-base shadow-lg shadow-sky-600/25 transition flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
          >
            {isSubmitting ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Creating Interview Session...</span>
              </>
            ) : (
              <>
                <span>Start Interview Setup</span>
                <ArrowRight className="w-5 h-5" />
              </>
            )}
          </button>
          <p className="text-center text-xs text-slate-500 mt-3 flex items-center justify-center gap-1.5">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            AI generates customized questions dynamically based on your target role and parameters.
          </p>
        </div>
      </form>
    </div>
  );
}
