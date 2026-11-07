"use client";

import React, { useState, useEffect, useCallback, Suspense, useMemo } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import {
  CodingSubmissionDetail,
  NormalizedPerformanceResult,
  SubmissionListResponse,
  CodingSubmissionListItem,
  Difficulty,
} from "@/types/coding";
import SubmissionResult from "@/components/coding/SubmissionResult";
import {
  ArrowLeft,
  RefreshCw,
  Code2,
  CheckCircle2,
  XCircle,
  Clock,
  Layers,
  Copy,
  Check,
  ExternalLink,
  Search,
  Filter,
  ChevronLeft,
  ChevronRight,
  Sparkles,
} from "lucide-react";

function ResultsContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const { user, isLoading: authLoading } = useAuth();
  const submissionId = searchParams.get("submissionId");

  const [submission, setSubmission] = useState<CodingSubmissionDetail | null>(null);
  const [perfMetrics, setPerfMetrics] = useState<NormalizedPerformanceResult | null>(null);
  const [copied, setCopied] = useState<boolean>(false);

  const [submissionsList, setSubmissionsList] = useState<CodingSubmissionListItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const [search, setSearch] = useState<string>("");
  const [verdictFilter, setVerdictFilter] = useState<string>("all");
  const [difficultyFilter, setDifficultyFilter] = useState<string>("all");
  const [page, setPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [totalCount, setTotalCount] = useState<number>(0);
  const limit = 20;

  const fetchSingleSubmission = useCallback(async (id: string) => {
    setLoading(true);
    setError(null);
    try {
      const [subData, scoreData] = await Promise.all([
        apiFetch<CodingSubmissionDetail>(`/coding/submissions/${id}`),
        apiFetch<NormalizedPerformanceResult>(`/coding/submissions/${id}/score`).catch(() => null),
      ]);
      setSubmission(subData);
      setPerfMetrics(scoreData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load submission details.");
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchAllSubmissions = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      params.append("page", page.toString());
      params.append("limit", limit.toString());

      const data = await apiFetch<SubmissionListResponse>(`/coding/submissions?${params.toString()}`);
      setSubmissionsList(data.submissions || []);
      setTotalPages(data.total_pages || 1);
      setTotalCount(data.total_count || 0);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load submissions list.");
    } finally {
      setLoading(false);
    }
  }, [page, limit]);

  useEffect(() => {
    if (submissionId) {
      fetchSingleSubmission(submissionId);
    } else {
      fetchAllSubmissions();
    }
  }, [submissionId, fetchSingleSubmission, fetchAllSubmissions]);

  const filteredSubmissions = useMemo(() => {
    return submissionsList.filter((item) => {
      if (search.trim()) {
        const query = search.toLowerCase();
        const matchesTitle = item.question_title?.toLowerCase().includes(query);
        const matchesTopic = item.question_topic?.toLowerCase().includes(query);
        if (!matchesTitle && !matchesTopic) return false;
      }

      if (verdictFilter !== "all") {
        const itemVerdict = (item.verdict || item.status).toLowerCase();
        if (verdictFilter === "accepted" && !itemVerdict.includes("accepted")) return false;
        if (verdictFilter === "wrong_answer" && !itemVerdict.includes("wrong")) return false;
        if (verdictFilter === "error" && (!itemVerdict.includes("error") && !itemVerdict.includes("failed"))) return false;
        if (verdictFilter === "timeout" && !itemVerdict.includes("time")) return false;
      }

      if (difficultyFilter !== "all") {
        if (item.question_difficulty?.toLowerCase() !== difficultyFilter.toLowerCase()) return false;
      }

      return true;
    });
  }, [submissionsList, search, verdictFilter, difficultyFilter]);

  if (authLoading) {
    return (
      <div className="py-20 text-center text-[#8993A0]">
        <RefreshCw className="w-8 h-8 text-[#123E63] animate-spin mx-auto mb-2" />
        <p className="text-xs font-semibold">Authenticating...</p>
      </div>
    );
  }

  if (!user) {
    router.push("/login");
    return null;
  }

  const copyCode = (codeText: string) => {
    navigator.clipboard.writeText(codeText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getDifficultyBadge = (difficulty?: Difficulty | string | null) => {
    if (!difficulty) return <span className="text-[#8993A0]">—</span>;
    switch (difficulty) {
      case "Easy":
        return (
          <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
            Easy
          </span>
        );
      case "Medium":
        return (
          <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-[#FFF6E8] text-[#F5A623] border border-[#F5A623]/30">
            Medium
          </span>
        );
      case "Hard":
        return (
          <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-red-50 text-red-600 border border-red-200">
            Hard
          </span>
        );
      default:
        return (
          <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-slate-100 text-slate-600">
            {difficulty}
          </span>
        );
    }
  };

  if (submissionId) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between gap-4">
          <Link
            href="/coding/results"
            className="inline-flex items-center gap-1.5 text-xs text-[#8993A0] hover:text-[#123E63] font-bold transition"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Back to All Submissions</span>
          </Link>

          {submission && (
            <Link
              href={`/coding/${submission.question_id}`}
              className="inline-flex items-center gap-1 text-xs text-[#123E63] hover:underline font-bold"
            >
              <span>Solve Again</span>
              <ExternalLink className="w-3.5 h-3.5" />
            </Link>
          )}
        </div>

        {loading ? (
          <div className="py-20 text-center text-[#8993A0] space-y-2">
            <RefreshCw className="w-8 h-8 text-[#123E63] animate-spin mx-auto" />
            <p className="text-xs font-semibold">Loading diagnostics...</p>
          </div>
        ) : error || !submission ? (
          <div className="bg-white rounded-2xl p-8 text-center space-y-3 shadow-card border border-[#E5E9EF] max-w-lg mx-auto">
            <p className="text-xs font-bold text-red-600">{error || "Submission record not found."}</p>
            <Link href="/coding/results" className="text-xs font-bold text-[#123E63] hover:underline">
              Return to Submissions
            </Link>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl p-6 shadow-card border border-[#E5E9EF] flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  {getDifficultyBadge(submission.question_difficulty)}
                  <span className="px-2.5 py-0.5 rounded-md text-[11px] font-semibold bg-[#F1F3F6] text-[#123E63] border border-[#E5E9EF]">
                    {submission.question_topic || "Algorithm"}
                  </span>
                </div>
                <h2 className="text-xl font-bold text-[#202B38]">{submission.question_title}</h2>
                <p className="text-xs text-[#8993A0] mt-0.5">
                  Language: <strong className="text-[#202B38] uppercase font-mono">{submission.language}</strong> &bull; Submitted {new Date(submission.created_at).toLocaleString()}
                </p>
              </div>

              <div className="text-right">
                <span className="text-[10px] font-bold text-[#8993A0] uppercase block">Normalized Score</span>
                <span className="text-3xl font-extrabold text-[#123E63]">
                  {submission.result?.score?.toFixed(1) || 0}
                  <span className="text-xs text-[#8993A0] font-normal"> / 100</span>
                </span>
              </div>
            </div>

            <SubmissionResult submission={submission} />

            {/* Code Snippet Box */}
            <div className="bg-white rounded-2xl p-6 shadow-card border border-[#E5E9EF] space-y-3">
              <div className="flex items-center justify-between border-b border-[#E5E9EF] pb-3">
                <h3 className="text-sm font-bold text-[#202B38]">Submitted Solution Source</h3>
                <button
                  onClick={() => copyCode(submission.code)}
                  className="px-3 py-1 bg-[#F8F9FA] hover:bg-white text-xs font-bold text-[#123E63] border border-[#E5E9EF] rounded-lg transition flex items-center gap-1.5"
                >
                  {copied ? <Check className="w-3.5 h-3.5 text-emerald-600" /> : <Copy className="w-3.5 h-3.5" />}
                  <span>{copied ? "Copied" : "Copy Code"}</span>
                </button>
              </div>

              <pre className="p-4 rounded-xl bg-[#0A1A2A] text-[#E1EAF5] font-mono text-xs overflow-x-auto leading-5">
                {submission.code}
              </pre>
            </div>
          </div>
        )}
      </div>
    );
  }

  // All Submissions List View
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-2xl p-6 sm:p-7 shadow-card border border-[#E5E9EF] flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#123E63]/10 border border-[#123E63]/20 text-[#123E63] text-xs font-semibold mb-2">
            <Code2 className="w-3.5 h-3.5 text-[#F5A623]" />
            Submission Log
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-[#202B38] tracking-tight">
            Coding Assessment History
          </h2>
          <p className="text-xs sm:text-sm text-[#8993A0] mt-1">
            Historical records of evaluated test executions, solve scores, and runtime benchmarks.
          </p>
        </div>

        <Link
          href="/coding"
          className="px-4 py-2.5 rounded-xl bg-[#123E63] hover:bg-[#0D3557] text-white text-xs font-bold shadow-sm transition flex items-center gap-1.5 self-start sm:self-auto"
        >
          <span>Problem Bank</span>
          <ExternalLink className="w-3.5 h-3.5" />
        </Link>
      </div>

      {/* Filter Bar */}
      <div className="bg-white rounded-2xl p-5 shadow-card border border-[#E5E9EF] flex flex-col md:flex-row gap-3 items-stretch md:items-center justify-between">
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-[#8993A0] absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search submission by problem title or topic..."
            className="w-full bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl pl-10 pr-4 py-2.5 text-xs text-[#202B38] placeholder-[#8993A0] focus:outline-none focus:border-[#123E63] transition"
          />
        </div>

        <div className="flex items-center gap-2">
          <select
            value={verdictFilter}
            onChange={(e) => setVerdictFilter(e.target.value)}
            className="bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl px-3 py-2 text-xs text-[#202B38] font-medium focus:outline-none focus:border-[#123E63]"
          >
            <option value="all">All Verdicts</option>
            <option value="accepted">Accepted</option>
            <option value="wrong_answer">Wrong Answer</option>
            <option value="error">Runtime Error</option>
            <option value="timeout">Time Limit</option>
          </select>

          <select
            value={difficultyFilter}
            onChange={(e) => setDifficultyFilter(e.target.value)}
            className="bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl px-3 py-2 text-xs text-[#202B38] font-medium focus:outline-none focus:border-[#123E63]"
          >
            <option value="all">All Difficulties</option>
            <option value="Easy">Easy</option>
            <option value="Medium">Medium</option>
            <option value="Hard">Hard</option>
          </select>
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-2xl shadow-card border border-[#E5E9EF] overflow-hidden">
        {loading ? (
          <div className="py-16 text-center space-y-2 text-[#8993A0]">
            <RefreshCw className="w-6 h-6 text-[#123E63] animate-spin mx-auto" />
            <p className="text-xs font-semibold">Loading submissions...</p>
          </div>
        ) : filteredSubmissions.length === 0 ? (
          <div className="py-16 text-center space-y-2 text-[#8993A0]">
            <Code2 className="w-8 h-8 text-[#BCD3E6] mx-auto" />
            <p className="text-xs font-bold text-[#202B38]">No submissions found</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-[#F8F9FA] text-[#8993A0] uppercase text-[10px] font-bold border-b border-[#E5E9EF]">
                <tr>
                  <th className="px-5 py-3">Verdict</th>
                  <th className="px-5 py-3">Problem Title</th>
                  <th className="px-5 py-3">Topic</th>
                  <th className="px-5 py-3">Difficulty</th>
                  <th className="px-5 py-3">Language</th>
                  <th className="px-5 py-3">Tests Passed</th>
                  <th className="px-5 py-3">Score</th>
                  <th className="px-5 py-3">Date</th>
                  <th className="px-5 py-3 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#E5E9EF] text-[#202B38]">
                {filteredSubmissions.map((sub) => {
                  const verdictStr = sub.verdict || sub.status;
                  const isAccepted = verdictStr.toLowerCase().includes("accepted");
                  return (
                    <tr key={sub.id} className="hover:bg-[#F8F9FA] transition">
                      <td className="px-5 py-3.5">
                        <span
                          className={`font-bold inline-flex items-center gap-1.5 ${
                            isAccepted ? "text-emerald-700" : "text-red-600"
                          }`}
                        >
                          {isAccepted ? <CheckCircle2 className="w-3.5 h-3.5" /> : <XCircle className="w-3.5 h-3.5" />}
                          <span>{verdictStr}</span>
                        </span>
                      </td>

                      <td className="px-5 py-3.5 font-bold">
                        <Link href={`/coding/${sub.question_id}`} className="hover:text-[#123E63] transition">
                          {sub.question_title || "Problem"}
                        </Link>
                      </td>

                      <td className="px-5 py-3.5 text-[#8993A0]">{sub.question_topic || "—"}</td>
                      <td className="px-5 py-3.5">{getDifficultyBadge(sub.question_difficulty)}</td>
                      <td className="px-5 py-3.5 font-mono text-[11px] text-[#8993A0] uppercase">
                        {sub.language}
                      </td>

                      <td className="px-5 py-3.5">
                        {sub.passed_test_cases !== undefined && sub.total_test_cases !== null ? (
                          <span className={sub.passed_test_cases === sub.total_test_cases ? "text-emerald-700 font-bold" : "text-[#202B38]"}>
                            {sub.passed_test_cases} / {sub.total_test_cases}
                          </span>
                        ) : (
                          "—"
                        )}
                      </td>

                      <td className="px-5 py-3.5 font-bold">
                        {sub.score !== undefined && sub.score !== null ? `${sub.score.toFixed(0)}/100` : "—"}
                      </td>

                      <td className="px-5 py-3.5 text-[#8993A0] text-[11px]">
                        {new Date(sub.created_at).toLocaleDateString()}
                      </td>

                      <td className="px-5 py-3.5 text-right">
                        <Link
                          href={`/coding/results?submissionId=${sub.id}`}
                          className="inline-flex items-center gap-1 text-xs text-[#123E63] hover:underline font-bold"
                        >
                          <span>Review</span>
                          <ExternalLink className="w-3 h-3" />
                        </Link>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}

        {totalPages > 1 && (
          <div className="px-5 py-3 bg-[#F8F9FA] border-t border-[#E5E9EF] flex items-center justify-between text-xs text-[#8993A0]">
            <div>
              Showing page {page} of {totalPages} ({totalCount} total)
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page <= 1 || loading}
                className="p-1.5 bg-white border border-[#E5E9EF] rounded-lg text-[#202B38] disabled:opacity-40"
              >
                <ChevronLeft className="w-3.5 h-3.5" />
              </button>
              <span>{page} / {totalPages}</span>
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page >= totalPages || loading}
                className="p-1.5 bg-white border border-[#E5E9EF] rounded-lg text-[#202B38] disabled:opacity-40"
              >
                <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function CodingResultsPage() {
  return (
    <Suspense
      fallback={
        <div className="py-20 text-center text-[#8993A0]">
          <RefreshCw className="w-8 h-8 text-[#123E63] animate-spin mx-auto mb-2" />
          <p className="text-xs font-semibold">Loading results...</p>
        </div>
      }
    >
      <ResultsContent />
    </Suspense>
  );
}
