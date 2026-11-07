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
      setTopics(topicData || []);
      setWeakTopics(weakData || []);
      setHistory(histData || []);
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
          <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
            Mastered
          </span>
        );
      case "Proficient":
        return (
          <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#F0F5FA] text-[#123E63] border border-[#BCD3E6]">
            Proficient
          </span>
        );
      case "Developing":
        return (
          <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#FFF6E8] text-[#F5A623] border border-[#F5A623]/30">
            Developing
          </span>
        );
      default:
        return (
          <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-red-50 text-red-600 border border-red-200">
            Needs Practice
          </span>
        );
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-2xl p-12 text-center space-y-3 shadow-card border border-[#E5E9EF]">
        <RefreshCw className="w-8 h-8 text-[#123E63] animate-spin mx-auto" />
        <h4 className="text-sm font-bold text-[#202B38]">Loading Coding Analytics...</h4>
        <p className="text-xs text-[#8993A0]">Aggregating submission benchmarks and test evaluations.</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-2xl p-8 text-center space-y-4 shadow-card border border-[#E5E9EF]">
        <p className="text-xs font-bold text-red-600">{error}</p>
        <button
          onClick={fetchProgressData}
          className="px-4 py-2 bg-[#123E63] text-xs font-bold text-white rounded-xl shadow-sm"
        >
          Retry
        </button>
      </div>
    );
  }

  if (!progress || progress.total_questions_attempted === 0) {
    return (
      <div className="bg-white rounded-2xl p-12 text-center space-y-4 shadow-card border border-[#E5E9EF]">
        <Code2 className="w-12 h-12 text-[#123E63] mx-auto opacity-70" />
        <div className="space-y-1">
          <h3 className="text-base font-bold text-[#202B38]">No Coding Submissions Yet</h3>
          <p className="text-xs text-[#8993A0] max-w-md mx-auto">
            You have not submitted solutions to any coding problems yet. Select a problem from the Problem Bank to start practicing!
          </p>
        </div>
      </div>
    );
  }

  const easyPct = progress.easy_total > 0 ? (progress.easy_solved / progress.easy_total) * 100 : 0;
  const medPct = progress.medium_total > 0 ? (progress.medium_solved / progress.medium_total) * 100 : 0;
  const hardPct = progress.hard_total > 0 ? (progress.hard_solved / progress.hard_total) * 100 : 0;

  return (
    <div className="space-y-6">
      {/* 4 Summary Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {/* Overall Score */}
        <div className="rounded-2xl bg-[#123E63] text-white p-5 shadow-navy-card">
          <span className="text-[11px] font-semibold text-[#BCD3E6] uppercase tracking-wider block">
            Overall Coding Score
          </span>
          <div className="text-3xl font-extrabold mt-1">
            {progress.overall_coding_score.toFixed(1)}
            <span className="text-xs text-[#BCD3E6] font-normal ml-1">/ 100</span>
          </div>
          <p className="text-[11px] text-[#BCD3E6] mt-1">Across verified submissions</p>
        </div>

        {/* Problems Solved */}
        <div className="bg-white rounded-2xl p-5 shadow-card border border-[#E5E9EF]">
          <span className="text-[11px] font-bold text-[#8993A0] uppercase tracking-wider block">
            Problems Solved
          </span>
          <div className="text-3xl font-extrabold text-[#202B38] mt-1">
            {progress.total_questions_solved}
            <span className="text-xs text-[#8993A0] font-normal ml-1">/ {progress.total_questions_in_bank}</span>
          </div>
          <p className="text-[11px] text-[#8993A0] mt-1">{progress.total_questions_attempted} attempted</p>
        </div>

        {/* Solve Rate */}
        <div className="bg-white rounded-2xl p-5 shadow-card border border-[#E5E9EF]">
          <span className="text-[11px] font-bold text-[#8993A0] uppercase tracking-wider block">
            Solve Accuracy
          </span>
          <div className="text-3xl font-extrabold text-[#202B38] mt-1">
            {progress.solve_rate_percentage.toFixed(1)}%
          </div>
          <p className="text-[11px] text-[#8993A0] mt-1">Pass rate on first submission</p>
        </div>

        {/* Submissions */}
        <div className="bg-white rounded-2xl p-5 shadow-card border border-[#E5E9EF]">
          <span className="text-[11px] font-bold text-[#8993A0] uppercase tracking-wider block">
            Total Runs
          </span>
          <div className="text-3xl font-extrabold text-[#F5A623] mt-1">
            {progress.total_submissions}
          </div>
          <p className="text-[11px] text-[#8993A0] mt-1">Evaluated code runs</p>
        </div>
      </div>

      {/* Difficulty Breakdown & Weak Areas */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Difficulty Breakdown */}
        <div className="bg-white rounded-2xl p-6 shadow-card border border-[#E5E9EF] space-y-4">
          <h3 className="text-sm font-bold text-[#202B38] flex items-center gap-2">
            <Layers className="w-4 h-4 text-[#123E63]" />
            <span>Difficulty Breakdown</span>
          </h3>

          <div className="space-y-4 text-xs">
            <div className="space-y-1.5">
              <div className="flex justify-between items-center text-[#202B38]">
                <span className="font-bold text-emerald-600">Easy</span>
                <span>
                  <strong>{progress.easy_solved}</strong> / {progress.easy_total} ({easyPct.toFixed(0)}%)
                </span>
              </div>
              <div className="w-full bg-[#F1F3F6] rounded-full h-2 overflow-hidden">
                <div
                  className="bg-emerald-500 h-full rounded-full transition-all duration-500"
                  style={{ width: `${Math.min(easyPct, 100)}%` }}
                />
              </div>
            </div>

            <div className="space-y-1.5">
              <div className="flex justify-between items-center text-[#202B38]">
                <span className="font-bold text-[#F5A623]">Medium</span>
                <span>
                  <strong>{progress.medium_solved}</strong> / {progress.medium_total} ({medPct.toFixed(0)}%)
                </span>
              </div>
              <div className="w-full bg-[#F1F3F6] rounded-full h-2 overflow-hidden">
                <div
                  className="bg-[#F5A623] h-full rounded-full transition-all duration-500"
                  style={{ width: `${Math.min(medPct, 100)}%` }}
                />
              </div>
            </div>

            <div className="space-y-1.5">
              <div className="flex justify-between items-center text-[#202B38]">
                <span className="font-bold text-red-600">Hard</span>
                <span>
                  <strong>{progress.hard_solved}</strong> / {progress.hard_total} ({hardPct.toFixed(0)}%)
                </span>
              </div>
              <div className="w-full bg-[#F1F3F6] rounded-full h-2 overflow-hidden">
                <div
                  className="bg-red-500 h-full rounded-full transition-all duration-500"
                  style={{ width: `${Math.min(hardPct, 100)}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Weak Topics */}
        <div className="bg-white rounded-2xl p-6 shadow-card border border-[#E5E9EF] space-y-4">
          <h3 className="text-sm font-bold text-[#202B38] flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-[#F5A623]" />
            <span>Targeted Focus Areas</span>
          </h3>

          {weakTopics.length === 0 ? (
            <div className="p-6 text-center space-y-2 rounded-xl bg-emerald-50 border border-emerald-200">
              <CheckCircle2 className="w-8 h-8 text-emerald-600 mx-auto" />
              <p className="text-xs font-bold text-emerald-800">Balanced Proficiency Across All Topics</p>
              <p className="text-[11px] text-[#8993A0]">
                All attempted problem categories meet the benchmark threshold.
              </p>
            </div>
          ) : (
            <div className="space-y-2.5">
              {weakTopics.slice(0, 3).map((wt) => (
                <div
                  key={wt.topic}
                  className="p-3 bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl space-y-1"
                >
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-bold text-[#202B38]">{wt.topic}</span>
                    <span className="text-[#F5A623] font-bold">{wt.average_score.toFixed(1)}% Avg</span>
                  </div>
                  <p className="text-[11px] text-[#8993A0]">
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
        <div className="bg-white rounded-2xl shadow-card border border-[#E5E9EF] overflow-hidden">
          <div className="px-5 py-4 border-b border-[#E5E9EF]">
            <h3 className="text-sm font-bold text-[#202B38]">Topic Proficiency Breakdown</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-[#F8F9FA] text-[#8993A0] uppercase text-[10px] font-bold border-b border-[#E5E9EF]">
                <tr>
                  <th className="px-5 py-3">Topic</th>
                  <th className="px-5 py-3">Solved / Attempted</th>
                  <th className="px-5 py-3">Submissions</th>
                  <th className="px-5 py-3">Accuracy</th>
                  <th className="px-5 py-3">Avg Score</th>
                  <th className="px-5 py-3 text-right">Proficiency</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E5E9EF] text-[#202B38]">
                {topics.map((t) => (
                  <tr key={t.topic} className="hover:bg-[#F8F9FA] transition">
                    <td className="px-5 py-3 font-bold">{t.topic}</td>
                    <td className="px-5 py-3 text-[#8993A0]">
                      {t.questions_solved} / {t.questions_attempted}
                    </td>
                    <td className="px-5 py-3 text-[#8993A0]">{t.total_submissions}</td>
                    <td className="px-5 py-3 text-[#123E63] font-bold">{t.accuracy_percentage.toFixed(1)}%</td>
                    <td className="px-5 py-3 font-bold">{t.average_score.toFixed(1)}</td>
                    <td className="px-5 py-3 text-right">{getProficiencyBadge(t.proficiency_level)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
