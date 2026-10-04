"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import { InterviewSession } from "@/types/interview";
import {
  Sparkles,
  Plus,
  Play,
  CheckCircle2,
  Clock,
  Mic,
  BarChart3,
  Calendar,
  ArrowRight,
  AlertCircle,
  Loader2,
  Brain,
} from "lucide-react";

export default function InterviewDashboardPage() {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  const [sessions, setSessions] = useState<InterviewSession[]>([]);
  const [isLoadingSessions, setIsLoadingSessions] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!isLoading && !user) {
      router.push("/login");
    }
  }, [user, isLoading, router]);

  useEffect(() => {
    let isMounted = true;
    const fetchSessions = async () => {
      if (!user) return;
      try {
        setIsLoadingSessions(true);
        setError(null);
        const data = await apiFetch<InterviewSession[]>("/interview/sessions");
        if (isMounted) {
          setSessions(data || []);
        }
      } catch (err: any) {
        if (isMounted) {
          setError(err.message || "Failed to load interview history.");
        }
      } finally {
        if (isMounted) {
          setIsLoadingSessions(false);
        }
      }
    };

    if (user) {
      fetchSessions();
    }

    return () => {
      isMounted = false;
    };
  }, [user]);

  if (isLoading || !user) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="w-8 h-8 animate-spin text-sky-400" />
      </div>
    );
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "completed":
        return (
          <span className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full bg-emerald-950/80 text-emerald-400 border border-emerald-500/30">
            <CheckCircle2 className="w-3 h-3" /> Completed
          </span>
        );
      case "in_progress":
        return (
          <span className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full bg-amber-950/80 text-amber-400 border border-amber-500/30">
            <Play className="w-3 h-3" /> In Progress
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
            <Clock className="w-3 h-3" /> Ready to Start
          </span>
        );
    }
  };

  const getDifficultyBadge = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case "easy":
        return <span className="text-xs text-emerald-400 font-medium">{difficulty}</span>;
      case "medium":
        return <span className="text-xs text-amber-400 font-medium">{difficulty}</span>;
      case "hard":
        return <span className="text-xs text-rose-400 font-medium">{difficulty}</span>;
      default:
        return <span className="text-xs text-slate-400 font-medium">{difficulty}</span>;
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8 py-4">
      {/* Hero Banner */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-slate-900 via-slate-900 to-sky-950/50 border border-slate-800 p-8 md:p-10 shadow-xl">
        <div className="relative z-10 max-w-2xl">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-sky-500/10 border border-sky-500/30 text-sky-400 text-xs font-semibold mb-4">
            <Sparkles className="w-3.5 h-3.5" />
            <span>AI Interview & Voice Intelligence</span>
          </div>
          <h1 className="text-3xl md:text-4xl font-extrabold text-white tracking-tight leading-tight">
            Master Technical & HR Interviews with Real-Time AI Coaching
          </h1>
          <p className="text-slate-300 text-sm md:text-base mt-3 leading-relaxed">
            Practice realistic mock interviews tailored to your target company and role. Receive instant speech-to-text transcription, filler-word analysis, speaking rate metrics, and actionable feedback.
          </p>
          <div className="mt-6 flex flex-wrap items-center gap-4">
            <Link
              href="/interview/setup"
              className="inline-flex items-center gap-2 px-6 py-3.5 rounded-xl bg-sky-500 hover:bg-sky-400 text-white font-bold text-sm shadow-lg shadow-sky-500/25 transition"
            >
              <Plus className="w-4 h-4" />
              <span>Start New Interview</span>
            </Link>
            <Link
              href="/interview/history"
              className="inline-flex items-center gap-2 px-5 py-3.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-semibold text-sm border border-slate-700 transition"
            >
              <Clock className="w-4 h-4 text-sky-400" />
              <span>Interview History</span>
            </Link>
          </div>
        </div>

        {/* Feature Highlights Pills */}
        <div className="mt-8 pt-6 border-t border-slate-800/80 grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-slate-800/80 border border-slate-700 text-sky-400">
              <Brain className="w-5 h-5" />
            </div>
            <div>
              <div className="text-xs font-semibold text-white">Dynamic AI Questions</div>
              <div className="text-[11px] text-slate-400">Tailored to your role & seniority</div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-slate-800/80 border border-slate-700 text-indigo-400">
              <Mic className="w-5 h-5" />
            </div>
            <div>
              <div className="text-xs font-semibold text-white">Speech & Voice Analysis</div>
              <div className="text-[11px] text-slate-400">Pace, pauses & filler words</div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-slate-800/80 border border-slate-700 text-emerald-400">
              <BarChart3 className="w-5 h-5" />
            </div>
            <div>
              <div className="text-xs font-semibold text-white">Comprehensive Scoring</div>
              <div className="text-[11px] text-slate-400">Technical depth & delivery metrics</div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Sessions Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-white tracking-tight">Your Interview Sessions</h2>
            <p className="text-xs text-slate-400 mt-0.5">Track your ongoing attempts and review completed interview scores.</p>
          </div>
          <div className="flex items-center gap-3">
            <Link
              href="/interview/history"
              className="text-xs font-semibold text-slate-300 hover:text-white transition flex items-center gap-1 px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-800 border border-slate-700/60"
            >
              <span>View All History</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
            <Link
              href="/interview/setup"
              className="text-xs font-semibold text-sky-400 hover:text-sky-300 transition flex items-center gap-1"
            >
              <span>New Setup</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        </div>

        {error && (
          <div className="p-4 rounded-xl bg-rose-950/40 border border-rose-500/40 flex items-center gap-3 text-sm text-rose-200">
            <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {isLoadingSessions ? (
          <div className="p-12 rounded-2xl bg-slate-900 border border-slate-800 flex flex-col items-center justify-center gap-3">
            <Loader2 className="w-6 h-6 animate-spin text-sky-400" />
            <p className="text-xs text-slate-400">Loading your interview sessions...</p>
          </div>
        ) : sessions.length === 0 ? (
          <div className="p-12 rounded-2xl bg-slate-900/60 border border-slate-800 border-dashed text-center flex flex-col items-center justify-center">
            <div className="p-4 rounded-2xl bg-slate-800/60 text-slate-400 mb-3">
              <Mic className="w-8 h-8" />
            </div>
            <h3 className="text-base font-semibold text-white">No interview sessions yet</h3>
            <p className="text-xs text-slate-400 max-w-sm mt-1">
              Start your first AI mock interview to test your domain knowledge and communication style.
            </p>
            <Link
              href="/interview/setup"
              className="mt-5 inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs transition"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>Create First Interview</span>
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {sessions.map((session) => (
              <div
                key={session.id}
                className="rounded-2xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition p-5 flex flex-col justify-between shadow-sm"
              >
                <div>
                  <div className="flex items-center justify-between gap-2 mb-3">
                    {getStatusBadge(session.status)}
                    <div className="flex items-center gap-1.5 text-[11px] text-slate-500">
                      <Calendar className="w-3 h-3" />
                      <span>{new Date(session.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>

                  <h3 className="text-base font-bold text-white line-clamp-1">{session.target_role}</h3>
                  {session.target_company && (
                    <p className="text-xs text-sky-400 font-medium mt-0.5">{session.target_company}</p>
                  )}

                  <div className="mt-4 flex flex-wrap items-center gap-2 text-xs">
                    <span className="px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 font-medium">
                      {session.interview_type}
                    </span>
                    <span className="px-2.5 py-1 rounded-lg bg-slate-800 font-medium">
                      {getDifficultyBadge(session.difficulty)}
                    </span>
                    <span className="px-2.5 py-1 rounded-lg bg-slate-800 text-slate-400">
                      {session.question_count} Questions
                    </span>
                  </div>

                  {session.overall_score !== null && session.overall_score !== undefined && (
                    <div className="mt-4 p-3 rounded-xl bg-slate-950 border border-slate-800/80 flex items-center justify-between">
                      <span className="text-xs text-slate-400 font-medium">Overall Score</span>
                      <span className="text-base font-extrabold text-emerald-400">
                        {Math.round(session.overall_score)}/100
                      </span>
                    </div>
                  )}
                </div>

                <div className="mt-5 pt-4 border-t border-slate-800/80 flex items-center justify-end">
                  {session.status === "completed" ? (
                    <Link
                      href={`/interview/result/${session.id}`}
                      className="inline-flex items-center gap-1 text-xs font-semibold text-sky-400 hover:text-sky-300 transition"
                    >
                      <span>View Results</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  ) : (
                    <Link
                      href={`/interview/session/${session.id}`}
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-sky-600 hover:bg-sky-500 text-white text-xs font-semibold transition"
                    >
                      <Play className="w-3 h-3 fill-current" />
                      <span>{session.status === "in_progress" ? "Continue" : "Start Session"}</span>
                    </Link>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
