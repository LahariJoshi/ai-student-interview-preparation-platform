"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import {
  Sparkles,
  History,
  ArrowRight,
  Award,
  Calendar,
  Clock,
  Briefcase,
  Play,
  RotateCcw,
} from "lucide-react";
import { InterviewHistoryResponse, InterviewSessionListItem } from "@/types/interview";

export default function InterviewHistoryPage() {
  const router = useRouter();
  const { user, isLoading: authLoading } = useAuth();

  const [history, setHistory] = useState<InterviewHistoryResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push("/login");
      return;
    }

    if (user) {
      fetchHistory();
    }
  }, [user, authLoading]);

  const fetchHistory = async () => {
    setIsLoading(true);
    try {
      const data = await apiFetch<InterviewHistoryResponse>("/interviews/history");
      setHistory(data);
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to load interview history.");
    } finally {
      setIsLoading(false);
    }
  };

  if (authLoading || isLoading) {
    return (
      <div className="py-24 text-center text-slate-400">
        <div className="w-8 h-8 border-2 border-sky-400 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <p className="text-sm">Retrieving your mock interview history...</p>
      </div>
    );
  }

  const getScoreBadgeColor = (score?: number | null) => {
    if (!score) return "text-slate-400 border-slate-700 bg-slate-800";
    if (score >= 80) return "text-emerald-400 border-emerald-500/40 bg-emerald-950/50";
    if (score >= 60) return "text-sky-400 border-sky-500/40 bg-sky-950/50";
    return "text-amber-400 border-amber-500/40 bg-amber-950/50";
  };

  return (
    <div className="max-w-4xl mx-auto py-4 space-y-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-sky-950/80 border border-sky-800 text-sky-300 text-xs font-semibold mb-2">
            <History className="w-3.5 h-3.5 text-sky-400" />
            Interview Journey & Tracking
          </div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">
            Your Mock Interview History
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Review past mock interview performances, question evaluations, and track placement readiness over time.
          </p>
        </div>

        <Link
          href="/interview"
          className="flex items-center gap-2 px-5 py-2.5 bg-sky-600 hover:bg-sky-500 text-white text-sm font-medium rounded-xl transition shadow-lg shadow-sky-950 self-start md:self-auto"
        >
          <RotateCcw className="w-4 h-4" />
          <span>New Mock Session</span>
        </Link>
      </div>

      {/* Analytics Summary Banner */}
      {history && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="glass-card p-5 text-center space-y-1">
            <span className="text-xs uppercase font-semibold text-slate-400">Total Interviews</span>
            <div className="text-3xl font-extrabold text-white">{history.total_interviews}</div>
            <p className="text-xs text-slate-500">Practice sessions initiated</p>
          </div>

          <div className="glass-card p-5 text-center space-y-1">
            <span className="text-xs uppercase font-semibold text-slate-400">Completed Sessions</span>
            <div className="text-3xl font-extrabold text-emerald-400">{history.completed_interviews}</div>
            <p className="text-xs text-slate-500">Fully evaluated mock tests</p>
          </div>

          <div className="glass-card p-5 text-center space-y-1">
            <span className="text-xs uppercase font-semibold text-slate-400">Average Performance</span>
            <div className="text-3xl font-extrabold text-sky-400">
              {Math.round(history.average_score)}<span className="text-lg font-normal text-slate-400">/100</span>
            </div>
            <p className="text-xs text-slate-500">Across completed interviews</p>
          </div>
        </div>
      )}

      {/* History List */}
      <div className="space-y-4">
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <span>Previous Interview Attempts</span>
        </h2>

        {history && history.sessions.length > 0 ? (
          <div className="space-y-3">
            {history.sessions.map((sess) => (
              <div
                key={sess.id}
                className="glass-card p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:border-slate-700 transition"
              >
                <div className="space-y-1.5">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="font-semibold text-white text-base">
                      {sess.target_role}
                    </span>
                    <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-sky-400 border border-slate-700">
                      {sess.interview_type.toUpperCase()}
                    </span>
                    <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                      {sess.experience_level}
                    </span>
                  </div>

                  <div className="flex items-center gap-4 text-xs text-slate-400 flex-wrap">
                    <span className="flex items-center gap-1">
                      <Calendar className="w-3.5 h-3.5 text-slate-500" />
                      {new Date(sess.started_at).toLocaleDateString()} {new Date(sess.started_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                    <span className="flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5 text-slate-500" />
                      {sess.duration_minutes} mins ({sess.total_questions} Questions)
                    </span>
                    <span>
                      Status:{" "}
                      <strong className={sess.status === "completed" ? "text-emerald-400" : "text-amber-400"}>
                        {sess.status}
                      </strong>
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-4">
                  {sess.overall_score !== null && sess.overall_score !== undefined ? (
                    <div className={`px-3 py-1.5 rounded-xl border text-sm font-bold text-center ${getScoreBadgeColor(sess.overall_score)}`}>
                      {Math.round(sess.overall_score)}<span className="text-xs font-normal opacity-80">/100</span>
                    </div>
                  ) : null}

                  {sess.status === "completed" ? (
                    <Link
                      href={`/interview/${sess.id}/results`}
                      className="flex items-center gap-1.5 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg text-xs font-semibold border border-slate-700 transition"
                    >
                      <span>View Rubric</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  ) : (
                    <Link
                      href={`/interview/${sess.id}`}
                      className="flex items-center gap-1.5 px-4 py-2 bg-sky-600 hover:bg-sky-500 text-white rounded-lg text-xs font-semibold transition"
                    >
                      <Play className="w-3.5 h-3.5 fill-current" />
                      <span>Resume</span>
                    </Link>
                  )}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="glass-card p-12 text-center space-y-4">
            <div className="w-12 h-12 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center text-slate-500 mx-auto">
              <History className="w-6 h-6" />
            </div>
            <h3 className="text-base font-bold text-white">No Mock Interviews Yet</h3>
            <p className="text-slate-400 text-sm max-w-sm mx-auto">
              You haven't practiced any mock interviews so far. Configure your first personalized interview to test your placement readiness.
            </p>
            <Link
              href="/interview"
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-sky-600 hover:bg-sky-500 text-white rounded-xl text-sm font-medium transition"
            >
              <span>Start Your First Interview</span>
              <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
