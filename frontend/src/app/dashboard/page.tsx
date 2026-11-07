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

interface AssessmentHistoryRecord {
  id: string;
  type: "ATS Analysis" | "Coding Assessment" | "Mock Interview";
  title: string;
  date: string;
  score: number;
  status: "Completed" | "Passed" | "Needs Review";
  link: string;
}

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
    codingTotal: 25,
    codingAccuracy: 0,
    interviewCount: 0,
    interviewAvgScore: null,
    readinessScore: 0,
  });

  const [history, setHistory] = useState<AssessmentHistoryRecord[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [filterType, setFilterType] = useState<string>("all");

  useEffect(() => {
    async function fetchPerformanceData() {
      setLoading(true);
      try {
        let atsScore: number | null = null;
        let codingSolved = 0;
        let codingTotal = 25;
        let codingAccuracy = 0;
        let interviewCount = 0;
        let interviewAvgScore: number | null = null;
        const records: AssessmentHistoryRecord[] = [];

        // 1. Fetch ATS analyses
        try {
          const atsList = await apiFetch<any[]>("/ats/history");
          if (Array.isArray(atsList) && atsList.length > 0) {
            atsScore = atsList[0].ats_score;
            atsList.slice(0, 5).forEach((item) => {
              records.push({
                id: item.analysis_id || item.id,
                type: "ATS Analysis",
                title: "Resume vs Target Job Description",
                date: item.analyzed_at ? new Date(item.analyzed_at).toLocaleDateString() : "Recent",
                score: Math.round(item.ats_score || 0),
                status: (item.ats_score || 0) >= 70 ? "Completed" : "Needs Review",
                link: "/ats",
              });
            });
          }
        } catch {
          // Fallback check resume analysis
          try {
            const resumeAnalysis = await apiFetch<any>("/resume/latest/analysis");
            if (resumeAnalysis && resumeAnalysis.quality_score !== null) {
              atsScore = resumeAnalysis.quality_score;
              records.push({
                id: resumeAnalysis.id,
                type: "ATS Analysis",
                title: "Resume Structural Quality",
                date: new Date(resumeAnalysis.created_at).toLocaleDateString(),
                score: Math.round(resumeAnalysis.quality_score),
                status: resumeAnalysis.quality_score >= 70 ? "Completed" : "Needs Review",
                link: "/resume",
              });
            }
          } catch {}
        }

        // 2. Fetch Coding Progress and Submissions
        try {
          const [codingData, codingHist] = await Promise.all([
            apiFetch<any>("/coding/progress"),
            apiFetch<any[]>("/coding/performance/history?limit=10"),
          ]);

          if (codingData) {
            codingSolved = codingData.total_solved || 0;
            codingTotal = codingData.total_questions || 25;
            codingAccuracy = codingData.solve_rate ? codingData.solve_rate * 100 : 0;
          }

          if (Array.isArray(codingHist)) {
            codingHist.forEach((sub) => {
              records.push({
                id: sub.submission_id,
                type: "Coding Assessment",
                title: `${sub.question_title} (${sub.language})`,
                date: new Date(sub.submitted_at).toLocaleDateString(),
                score: Math.round(sub.normalized_score || 0),
                status: sub.status === "Accepted" ? "Passed" : "Needs Review",
                link: `/coding/results?submissionId=${sub.submission_id}`,
              });
            });
          }
        } catch {}

        // 3. Fetch Mock Interview Sessions
        try {
          const interviewData = await apiFetch<any>("/interviews/history");
          if (interviewData) {
            interviewCount = interviewData.total_interviews || interviewData.completed_interviews || 0;
            interviewAvgScore = interviewData.average_score || null;

            if (Array.isArray(interviewData.sessions)) {
              interviewData.sessions.slice(0, 5).forEach((sess: any) => {
                records.push({
                  id: sess.id,
                  type: "Mock Interview",
                  title: `${sess.target_role} (${sess.interview_type})`,
                  date: new Date(sess.started_at).toLocaleDateString(),
                  score: Math.round(sess.overall_score || 0),
                  status: sess.status === "completed" ? "Completed" : "Needs Review",
                  link: `/interview/${sess.id}/results`,
                });
              });
            }
          }
        } catch {}

        // Sort records by date if possible
        setHistory(records);

        // Weighted readiness formula:
        const atsPart = atsScore !== null ? atsScore * 0.3 : 20;
        const codingPart = codingTotal > 0 ? (codingSolved / codingTotal) * 100 * 0.35 : 0;
        const interviewPart = interviewAvgScore !== null ? interviewAvgScore * 0.35 : (interviewCount > 0 ? 50 * 0.35 : 15);
        const readiness = Math.min(100, Math.round(atsPart + codingPart + interviewPart));

        setMetrics({
          atsScore,
          codingSolved,
          codingTotal,
          codingAccuracy,
          interviewCount,
          interviewAvgScore,
          readinessScore: readiness > 0 ? readiness : 45,
        });
      } catch (e) {
        console.error("Performance load error:", e);
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
          <PreparationProgressChart />

          {/* Skill Progress Dual-Wave Area Chart */}
          <SkillDevelopmentChart />
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
