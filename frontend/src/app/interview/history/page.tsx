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
      <div className="py-24 text-center text-[#8993A0]">
        <div className="w-8 h-8 border-3 border-[#123E63] border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <p className="text-sm font-medium">Retrieving your mock interview history...</p>
      </div>
    );
  }

  const getScoreBadgeColor = (score?: number | null) => {
    if (!score) return "text-[#8993A0] border-[#E5E9EF] bg-[#F1F3F6]";
    if (score >= 80) return "text-emerald-700 border-emerald-200 bg-emerald-50";
    if (score >= 60) return "text-[#123E63] border-blue-200 bg-blue-50";
    return "text-amber-700 border-amber-200 bg-amber-50";
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#123E63]/10 text-[#123E63] text-xs font-semibold mb-2">
            <History className="w-3.5 h-3.5 text-[#F5A623]" />
            Interview Journey & Tracking
          </div>
          <h1 className="text-2xl font-bold text-[#202B38] tracking-tight">
            Your Mock Interview History
          </h1>
          <p className="text-[#8993A0] text-xs mt-1">
            Review past mock interview performances, question evaluations, and track placement readiness over time.
          </p>
        </div>

        <Link
          href="/interview"
          className="flex items-center gap-2 px-5 py-2.5 bg-[#F5A623] hover:bg-[#E09612] text-white text-xs font-semibold rounded-xl transition shadow-sm self-start md:self-auto"
        >
          <RotateCcw className="w-4 h-4" />
          <span>New Mock Session</span>
        </Link>
      </div>

      {/* Analytics Summary Banner */}
      {history && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-[#123E63] text-white rounded-2xl p-5 shadow-sm text-center space-y-1">
            <span className="text-[11px] uppercase font-semibold text-white/70">Total Interviews</span>
            <div className="text-3xl font-extrabold text-white">{history.total_interviews}</div>
            <p className="text-xs text-white/70">Practice sessions initiated</p>
          </div>

          <div className="bg-white border border-[#E5E9EF] rounded-2xl p-5 shadow-sm text-center space-y-1">
            <span className="text-[11px] uppercase font-semibold text-[#8993A0]">Completed Sessions</span>
            <div className="text-3xl font-extrabold text-emerald-600">{history.completed_interviews}</div>
            <p className="text-xs text-[#8993A0]">Fully evaluated mock tests</p>
          </div>

          <div className="bg-white border border-[#E5E9EF] rounded-2xl p-5 shadow-sm text-center space-y-1">
            <span className="text-[11px] uppercase font-semibold text-[#8993A0]">Average Performance</span>
            <div className="text-3xl font-extrabold text-[#F5A623]">
              {Math.round(history.average_score)}<span className="text-base font-normal text-[#8993A0]">/100</span>
            </div>
            <p className="text-xs text-[#8993A0]">Across completed interviews</p>
          </div>
        </div>
      )}

      {/* History List */}
      <div className="space-y-4">
        <h2 className="text-base font-bold text-[#202B38] flex items-center gap-2">
          <span>Previous Interview Attempts</span>
        </h2>

        {history && history.sessions.length > 0 ? (
          <div className="space-y-3">
            {history.sessions.map((sess) => (
              <div
                key={sess.id}
                className="bg-white border border-[#E5E9EF] rounded-2xl p-5 flex flex-col md:flex-row md:items-center justify-between gap-4 hover:shadow-sm transition"
              >
                <div className="space-y-1.5">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="font-bold text-[#202B38] text-sm">
                      {sess.target_role}
                    </span>
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-[#123E63]/10 text-[#123E63] font-semibold">
                      {sess.interview_type.toUpperCase()}
                    </span>
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-[#F1F3F6] text-[#8993A0] font-medium border border-[#E5E9EF]">
                      {sess.experience_level}
                    </span>
                  </div>

                  <div className="flex items-center gap-4 text-xs text-[#8993A0] flex-wrap">
                    <span className="flex items-center gap-1">
                      <Calendar className="w-3.5 h-3.5 text-[#8993A0]" />
                      {new Date(sess.started_at).toLocaleDateString()} {new Date(sess.started_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                    <span className="flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5 text-[#8993A0]" />
                      {sess.duration_minutes} mins ({sess.total_questions} Questions)
                    </span>
                    <span>
                      Status:{" "}
                      <strong className={sess.status === "completed" ? "text-emerald-600" : "text-amber-600"}>
                        {sess.status}
                      </strong>
                    </span>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  {sess.overall_score !== null && sess.overall_score !== undefined ? (
                    <div className={`px-3 py-1.5 rounded-xl border text-xs font-bold text-center ${getScoreBadgeColor(sess.overall_score)}`}>
                      {Math.round(sess.overall_score)}<span className="text-[10px] font-normal opacity-80">/100</span>
                    </div>
                  ) : null}

                  {sess.status === "completed" ? (
                    <Link
                      href={`/interview/${sess.id}/results`}
                      className="flex items-center gap-1.5 px-4 py-2 bg-[#123E63] hover:bg-[#0D3557] text-white rounded-xl text-xs font-semibold transition shadow-sm"
                    >
                      <span>View Rubric</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  ) : (
                    <Link
                      href={`/interview/${sess.id}`}
                      className="flex items-center gap-1.5 px-4 py-2 bg-[#F5A623] hover:bg-[#E09612] text-white rounded-xl text-xs font-semibold transition shadow-sm"
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
          <div className="bg-white border border-[#E5E9EF] rounded-2xl p-12 text-center space-y-4">
            <div className="w-12 h-12 rounded-full bg-[#F1F3F6] border border-[#E5E9EF] flex items-center justify-center text-[#8993A0] mx-auto">
              <History className="w-6 h-6 text-[#123E63]" />
            </div>
            <h3 className="text-sm font-bold text-[#202B38]">No Mock Interviews Yet</h3>
            <p className="text-[#8993A0] text-xs max-w-sm mx-auto">
              You haven't practiced any mock interviews so far. Configure your first personalized interview to test your placement readiness.
            </p>
            <Link
              href="/interview"
              className="inline-flex items-center gap-2 px-5 py-2.5 bg-[#123E63] hover:bg-[#0D3557] text-white rounded-xl text-xs font-semibold transition shadow-sm"
            >
              <span>Start Your First Interview</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}