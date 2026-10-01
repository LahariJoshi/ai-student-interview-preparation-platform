"use client";

import React, { useState, useEffect, useCallback } from "react";
import Link from "next/link";
import { apiFetch } from "@/lib/api";
import {
  CodingProgressSummary,
  TopicPerformance,
  WeakTopic,
  CodingHistoryItem,
} from "@/types/coding";
import {
  Trophy,
  CheckCircle2,
  Target,
  TrendingUp,
  AlertTriangle,
  History,
  Layers,
  RefreshCw,
  ArrowRight,
  Code2,
  Calendar,
  Sparkles,
} from "lucide-react";

export default function CodingProgress() {
  const [progress, setProgress] = useState<CodingProgressSummary | null>(null);
  const [topics, setTopics] = useState<TopicPerformance[]>([]);
  const [weakTopics, setWeakTopics] = useState<WeakTopic[]>([]);
  const [history, setHistory] = useState<CodingHistoryItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProgressData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [progData, topicData, weakData, histData] = await Promise.all([
        apiFetch<CodingProgressSummary>("/coding/progress"),
        apiFetch<TopicPerformance[]>("/coding/performance/topics"),
        apiFetch<WeakTopic[]>("/coding/performance/weak-topics"),
        apiFetch<CodingHistoryItem[]>("/coding/performance/history?limit=10"),
      ]);

      setProgress(progData);
      setTopics(topicData);
      setWeakTopics(weakData);
      setHistory(histData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load coding analytics.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchProgressData();
  }, [fetchProgressData]);

  const getProficiencyBadge = (level: string) => {
    switch (level) {
      case "Mastered":
        return (
          <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            Mastered
          </span>
        );
      case "Proficient":
        return (
          <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-sky-500/10 text-sky-400 border border-sky-500/20">
            Proficient
          </span>
        );
      case "Developing":
        return (
          <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">
            Developing
          </span>
        );
      default:
        return (
          <span className="px-2 py-0.5 rounded-full text-[11px] font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20">
            Needs Practice
          </span>
        );
    }
  };

  if (loading) {
    return (
      <div className="glass-card p-12 text-center space-y-3">
        <RefreshCw className="w-8 h-8 text-sky-400 animate-spin mx-auto" />
        <h4 className="text-sm font-semibold text-white">Loading Coding Analytics...</h4>
        <p className="text-xs text-slate-400">Aggregating your submission performance and progress.</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="glass-card p-8 text-center space-y-4">
        <p className="text-sm text-rose-400">{error}</p>
        <button
          onClick={fetchProgressData}
          className="px-4 py-2 bg-slate-800 text-xs text-slate-200 hover:text-white rounded-lg border border-slate-700"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!progress || progress.total_questions_attempted === 0) {
    return (
      <div className="glass-card p-12 text-center space-y-4">
        <Code2 className="w-12 h-12 text-sky-500 mx-auto opacity-70" />
        <div className="space-y-1">
          <h3 className="text-base font-bold text-white">No Coding Submissions Yet</h3>
          <p className="text-xs text-slate-400 max-w-md mx-auto">
            You have not attempted any coding problems yet. Select a problem from the Question List to start practicing and build your analytics!
          </p>
        </div>
      </div>
    );
  }

  // Calculate percentages for difficulty progress bars
  const easyPct = progress.easy_total > 0 ? (progress.easy_solved / progress.easy_total) * 100 : 0;
  const medPct = progress.medium_total > 0 ? (progress.medium_solved / progress.medium_total) * 100 : 0;
  const hardPct = progress.hard_total > 0 ? (progress.hard_solved / progress.hard_total) * 100 : 0;

  return (
    <div className="space-y-6">
      {/* Top Header with Refresh */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Trophy className="w-5 h-5 text-amber-400" />
            <span>Coding Performance & Progress</span>
          </h2>
          <p className="text-xs text-slate-400">
            Real-time analytics computed from verified test-case executions.
          </p>
        </div>
        <button
          onClick={fetchProgressData}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-lg text-xs font-medium transition"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh</span>
        </button>
      </div>

      {/* Core KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {/* Overall Score */}
        <div className="glass-card p-4 space-y-1 border-t-2 border-t-sky-500">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1">
            <Sparkles className="w-3.5 h-3.5 text-sky-400" />
            Overall Score
          </div>
          <div className="text-2xl font-extrabold text-white">
            <span className="text-sky-400">{progress.overall_coding_score.toFixed(1)}</span>
            <span className="text-xs text-slate-500 font-normal"> / 100</span>
          </div>
          <div className="text-[11px] text-slate-400">
            Across evaluated submissions
          </div>
        </div>

        {/* Problems Solved */}
        <div className="glass-card p-4 space-y-1 border-t-2 border-t-emerald-500">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
            Problems Solved
          </div>
          <div className="text-2xl font-extrabold text-white">
            <span className="text-emerald-400">{progress.total_questions_solved}</span>
            <span className="text-xs text-slate-500 font-normal"> / {progress.total_questions_in_bank}</span>
          </div>
          <div className="text-[11px] text-slate-400">
            {progress.total_questions_attempted} attempted
          </div>
        </div>

        {/* Solve Rate */}
        <div className="glass-card p-4 space-y-1 border-t-2 border-t-indigo-500">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1">
            <TrendingUp className="w-3.5 h-3.5 text-indigo-400" />
            Solve Rate
          </div>
          <div className="text-2xl font-extrabold text-white">
            <span className="text-indigo-400">{progress.solve_rate_percentage.toFixed(1)}%</span>
          </div>
          <div className="text-[11px] text-slate-400">
            Solved vs attempted
          </div>
        </div>

        {/* Submissions */}
        <div className="glass-card p-4 space-y-1 border-t-2 border-t-amber-500">
          <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider flex items-center gap-1">
            <Target className="w-3.5 h-3.5 text-amber-400" />
            Submissions
          </div>
          <div className="text-2xl font-extrabold text-white">
            <span className="text-amber-400">{progress.total_submissions}</span>
          </div>
          <div className="text-[11px] text-slate-400">
            Total code evaluations
          </div>
        </div>
      </div>

      {/* Difficulty Breakdown & Weak Areas */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Difficulty Breakdown Progress Bars */}
        <div className="glass-card p-5 space-y-4">
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Layers className="w-4 h-4 text-sky-400" />
            <span>Difficulty Breakdown</span>
          </h3>

          <div className="space-y-4 text-xs">
            {/* Easy */}
            <div className="space-y-1.5">
              <div className="flex justify-between items-center text-slate-300">
                <span className="font-semibold text-emerald-400">Easy</span>
                <span>
                  <strong>{progress.easy_solved}</strong> / {progress.easy_total} solved ({easyPct.toFixed(0)}%)
                </span>
              </div>
              <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden border border-slate-800">
                <div
                  className="bg-emerald-500 h-full rounded-full transition-all duration-500"
                  style={{ width: `${Math.min(easyPct, 100)}%` }}
                />
              </div>
            </div>

            {/* Medium */}
            <div className="space-y-1.5">
              <div className="flex justify-between items-center text-slate-300">
                <span className="font-semibold text-amber-400">Medium</span>
                <span>
                  <strong>{progress.medium_solved}</strong> / {progress.medium_total} solved ({medPct.toFixed(0)}%)
                </span>
              </div>
              <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden border border-slate-800">
                <div
                  className="bg-amber-500 h-full rounded-full transition-all duration-500"
                  style={{ width: `${Math.min(medPct, 100)}%` }}
                />
              </div>
            </div>

            {/* Hard */}
            <div className="space-y-1.5">
              <div className="flex justify-between items-center text-slate-300">
                <span className="font-semibold text-rose-400">Hard</span>
                <span>
                  <strong>{progress.hard_solved}</strong> / {progress.hard_total} solved ({hardPct.toFixed(0)}%)
                </span>
              </div>
              <div className="w-full bg-slate-900 rounded-full h-2 overflow-hidden border border-slate-800">
                <div
                  className="bg-rose-500 h-full rounded-full transition-all duration-500"
                  style={{ width: `${Math.min(hardPct, 100)}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Weak Topics & Practice Recommendations */}
        <div className="glass-card p-5 space-y-4">
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-amber-400" />
            <span>Targeted Focus Areas</span>
          </h3>

          {weakTopics.length === 0 ? (
            <div className="p-6 text-center space-y-2 rounded-lg bg-emerald-950/20 border border-emerald-800/40">
              <CheckCircle2 className="w-8 h-8 text-emerald-400 mx-auto" />
              <p className="text-xs font-semibold text-emerald-300">Strong Performance Across All Topics</p>
              <p className="text-[11px] text-slate-400">
                No weak problem areas detected below the proficiency threshold. Keep up the high standard!
              </p>
            </div>
          ) : (
            <div className="space-y-3">
              {weakTopics.slice(0, 3).map((wt) => (
                <div
                  key={wt.topic}
                  className="p-3 bg-slate-900/90 border border-amber-900/40 rounded-lg space-y-1.5"
                >
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-bold text-white">{wt.topic}</span>
                    <span className="text-amber-400 font-semibold">{wt.average_score.toFixed(1)}% Avg</span>
                  </div>
                  <p className="text-[11px] text-slate-400 leading-normal">
                    {wt.recommended_focus}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Topic-Wise Performance Table */}
      {topics.length > 0 && (
        <div className="glass-card overflow-hidden">
          <div className="px-5 py-4 border-b border-slate-800">
            <h3 className="text-sm font-bold text-white">Topic Proficiency Breakdown</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-900/80 text-slate-400 uppercase text-[11px] font-semibold border-b border-slate-800">
                <tr>
                  <th className="px-5 py-3">Topic</th>
                  <th className="px-5 py-3">Solved / Attempted</th>
                  <th className="px-5 py-3">Submissions</th>
                  <th className="px-5 py-3">Accuracy</th>
                  <th className="px-5 py-3">Avg Score</th>
                  <th className="px-5 py-3 text-right">Proficiency</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 text-slate-200">
                {topics.map((t) => (
                  <tr key={t.topic} className="hover:bg-slate-800/40 transition">
                    <td className="px-5 py-3 font-semibold text-white">{t.topic}</td>
                    <td className="px-5 py-3">
                      {t.questions_solved} / {t.questions_attempted}
                    </td>
                    <td className="px-5 py-3">{t.total_submissions}</td>
                    <td className="px-5 py-3 text-sky-400">{t.accuracy_percentage.toFixed(1)}%</td>
                    <td className="px-5 py-3">{t.average_score.toFixed(1)}</td>
                    <td className="px-5 py-3 text-right">{getProficiencyBadge(t.proficiency_level)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Recent Activity Table */}
      {history.length > 0 && (
        <div className="glass-card overflow-hidden">
          <div className="px-5 py-4 border-b border-slate-800 flex items-center justify-between">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <History className="w-4 h-4 text-sky-400" />
              <span>Recent Submissions</span>
            </h3>
            <Link
              href="/coding/results"
              className="text-xs text-sky-400 hover:text-sky-300 font-medium inline-flex items-center gap-1"
            >
              <span>View All History</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-900/80 text-slate-400 uppercase text-[11px] font-semibold border-b border-slate-800">
                <tr>
                  <th className="px-5 py-3">Problem</th>
                  <th className="px-5 py-3">Difficulty</th>
                  <th className="px-5 py-3">Language</th>
                  <th className="px-5 py-3">Verdict</th>
                  <th className="px-5 py-3">Score</th>
                  <th className="px-5 py-3 text-right">Date</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 text-slate-200">
                {history.map((h) => {
                  const isAccepted = h.verdict.toLowerCase().includes("accepted");
                  return (
                    <tr key={h.submission_id} className="hover:bg-slate-800/40 transition">
                      <td className="px-5 py-3 font-medium text-white">
                        <Link href={`/coding/${h.question_id}`} className="hover:text-sky-400 transition">
                          {h.question_title}
                        </Link>
                      </td>
                      <td className="px-5 py-3 text-slate-400">{h.difficulty}</td>
                      <td className="px-5 py-3 font-mono text-[11px] text-slate-300">{h.language}</td>
                      <td className="px-5 py-3">
                        <span
                          className={`font-semibold ${
                            isAccepted ? "text-emerald-400" : "text-rose-400"
                          }`}
                        >
                          {h.verdict}
                        </span>
                      </td>
                      <td className="px-5 py-3 font-bold text-white">{h.score.toFixed(1)}</td>
                      <td className="px-5 py-3 text-right text-slate-400 text-[11px]">
                        {new Date(h.created_at).toLocaleDateString()}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
