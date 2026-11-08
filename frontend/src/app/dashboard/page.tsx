"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import MetricCards, { MetricData } from "@/components/dashboard/MetricCards";
import PreparationProgressChart from "@/components/dashboard/PreparationProgressChart";
import SkillDevelopmentChart from "@/components/dashboard/SkillDevelopmentChart";
import ReadinessSidePanel from "@/components/dashboard/ReadinessSidePanel";
import {
  DashboardOverviewResponse,
  DashboardAssessmentRecord,
} from "@/types/dashboard";
import {
  BarChart2,
  TrendingUp,
  Award,
  CheckCircle2,
  Clock,
  ExternalLink,
  Filter,
  RefreshCw,
  FileText,
  Code2,
  Mic,
} from "lucide-react";

export default function PerformanceDashboardPage() {
  const router = useRouter();
  const { user, isLoading: authLoading } = useAuth();

  useEffect(() => {
    if (!authLoading && !user) {
      router.push("/login");
    }
  }, [user, authLoading, router]);

  const [metrics, setMetrics] = useState<MetricData>({
    atsScore: null,
    codingSolved: 0,
    codingTotal: 222,
    codingAccuracy: 0,
    interviewCount: 0,
    interviewAvgScore: null,
    readinessScore: 0,
  });

  const [overview, setOverview] = useState<DashboardOverviewResponse | null>(null);
  const [history, setHistory] = useState<DashboardAssessmentRecord[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [filterType, setFilterType] = useState<string>("all");

  useEffect(() => {
    async function fetchPerformanceData() {
      setLoading(true);
      try {
        // Fetch unified dashboard overview from backend API
        const data = await apiFetch<DashboardOverviewResponse>("/dashboard/overview");
        setOverview(data);

        setMetrics({
          atsScore: data.metrics.ats_score,
          codingSolved: data.metrics.coding_solved,
          codingTotal: data.metrics.coding_total,
          codingAccuracy: data.metrics.coding_accuracy !== null ? data.metrics.coding_accuracy : 0,
          interviewCount: data.metrics.interview_count,
          interviewAvgScore: data.metrics.interview_avg_score,
          readinessScore: data.metrics.readiness_score,
        });

        setHistory(data.recent_history || []);
      } catch (e) {
        console.error("Dashboard overview error:", e);
      } finally {
        setLoading(false);
      }
    }

    if (user) {
      fetchPerformanceData();
    } else if (!authLoading) {
      setLoading(false);
    }
  }, [user, authLoading]);

  const filteredHistory = history.filter((item) => {
    if (filterType === "all") return true;
    if (filterType === "ats") return item.type === "ATS Analysis";
    if (filterType === "coding") return item.type === "Coding Assessment";
    if (filterType === "interview") return item.type === "Mock Interview";
    return true;
  });

  return (
    <div className="space-y-6">
      {/* Top Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-[#202B38] tracking-tight">
            Performance Dashboard
          </h2>
          <p className="text-xs sm:text-sm text-[#8993A0] mt-0.5">
            Real-time analytics across your ATS resume score, coding assessments, and AI mock interviews
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Link
            href="/recommendations"
            className="px-4 py-2 rounded-xl bg-[#F5A623] hover:bg-[#E09212] text-white text-xs font-bold transition shadow-sm flex items-center gap-1.5"
          >
            <span>Improve My Score</span>
          </Link>
        </div>
      </div>

      {/* 1. Four Top Summary Cards matching reference proportions */}
      <MetricCards data={metrics} isLoading={loading && authLoading} />

      {/* 2. Main Performance Center-Left Grid + Right Side Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Center-Left Main Visual Area (8 cols) */}
        <div className="lg:col-span-8 space-y-6">
          {/* Main Performance Comparison Bar Chart */}
          <PreparationProgressChart
            data={overview?.progress_chart}
            isLoading={loading}
          />

          {/* Skill Progress Dual-Wave Area Chart */}
          <SkillDevelopmentChart
            data={overview?.skill_development}
            isLoading={loading}
          />
        </div>

        {/* Right-Side Performance Panel (4 cols) */}
        <div className="lg:col-span-4">
          <ReadinessSidePanel
            score={metrics.readinessScore}
            atsScore={metrics.atsScore}
            codingAccuracy={metrics.codingAccuracy}
            interviewScore={metrics.interviewAvgScore}
          />
        </div>
      </div>

      {/* 3. Assessment History Table */}
      <section className="bg-white rounded-2xl p-5 sm:p-6 shadow-card border border-[#E5E9EF]">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-5">
          <div>
            <h3 className="text-base font-bold text-[#202B38] tracking-tight">
              Assessment History & Records
            </h3>
            <p className="text-xs text-[#8993A0]">
              Verified evaluations logged from your recent interview preparation sessions
            </p>
          </div>

          {/* Filter Pills */}
          <div className="flex items-center gap-1.5 bg-[#F1F3F6] p-1 rounded-xl">
            {[
              { label: "All Records", val: "all" },
              { label: "ATS", val: "ats" },
              { label: "Coding", val: "coding" },
              { label: "Interview", val: "interview" },
            ].map((f) => (
              <button
                key={f.val}
                onClick={() => setFilterType(f.val)}
                className={`px-3 py-1 rounded-lg text-xs font-semibold transition ${
                  filterType === f.val
                    ? "bg-[#123E63] text-white shadow-xs"
                    : "text-[#8993A0] hover:text-[#202B38]"
                }`}
              >
                {f.label}
              </button>
            ))}
          </div>
        </div>

        {/* History Table */}
        <div className="overflow-x-auto">
          {filteredHistory.length > 0 ? (
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="border-b border-[#E5E9EF] text-[11px] font-semibold text-[#8993A0] uppercase tracking-wider">
                  <th className="py-3 px-4">Assessment Type</th>
                  <th className="py-3 px-4">Details</th>
                  <th className="py-3 px-4">Date</th>
                  <th className="py-3 px-4">Score</th>
                  <th className="py-3 px-4">Status</th>
                  <th className="py-3 px-4 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E5E9EF] text-xs">
                {filteredHistory.map((item) => (
                  <tr
                    key={item.id}
                    className="hover:bg-[#F8F9FA] transition"
                  >
                    <td className="py-3.5 px-4 font-semibold text-[#202B38] flex items-center gap-2">
                      {item.type === "ATS Analysis" && (
                        <FileText className="w-4 h-4 text-[#123E63]" />
                      )}
                      {item.type === "Coding Assessment" && (
                        <Code2 className="w-4 h-4 text-[#F5A623]" />
                      )}
                      {item.type === "Mock Interview" && (
                        <Mic className="w-4 h-4 text-[#123E63]" />
                      )}
                      <span>{item.type}</span>
                    </td>
                    <td className="py-3.5 px-4 text-[#8993A0] font-medium truncate max-w-[200px]">
                      {item.title}
                    </td>
                    <td className="py-3.5 px-4 text-[#8993A0]">
                      {item.date}
                    </td>
                    <td className="py-3.5 px-4 font-bold text-[#202B38]">
                      {item.score}%
                    </td>
                    <td className="py-3.5 px-4">
                      <span
                        className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold ${
                          item.status === "Completed" || item.status === "Passed"
                            ? "bg-emerald-50 text-emerald-600 border border-emerald-200"
                            : "bg-[#FFF6E8] text-[#F5A623] border border-[#F5A623]/30"
                        }`}
                      >
                        {item.status}
                      </span>
                    </td>
                    <td className="py-3.5 px-4 text-right">
                      <Link
                        href={item.link}
                        className="inline-flex items-center gap-1 text-xs font-bold text-[#123E63] hover:text-[#0D3557]"
                      >
                        <span>View</span>
                        <ExternalLink className="w-3.5 h-3.5" />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="py-12 text-center text-[#8993A0] space-y-2">
              <CheckCircle2 className="w-8 h-8 text-[#BCD3E6] mx-auto" />
              <p className="text-sm font-semibold text-[#202B38]">No evaluations recorded yet</p>
              <p className="text-xs">
                Upload your resume, solve coding questions, or conduct a mock interview to populate your performance records.
              </p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
