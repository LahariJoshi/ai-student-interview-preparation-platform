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
  FileCode,
  Copy,
  Check,
  ExternalLink,
  Search,
  Filter,
  ChevronLeft,
  ChevronRight,
  RotateCcw,
  Sparkles,
} from "lucide-react";

function ResultsContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const { user, isLoading: authLoading } = useAuth();
  const submissionId = searchParams.get("submissionId");

  // Single submission state
  const [submission, setSubmission] = useState<CodingSubmissionDetail | null>(null);
  const [perfMetrics, setPerfMetrics] = useState<NormalizedPerformanceResult | null>(null);
  const [copied, setCopied] = useState<boolean>(false);

  // Submissions list state (when no submissionId)
  const [submissionsList, setSubmissionsList] = useState<CodingSubmissionListItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // List filters & pagination
  const [search, setSearch] = useState<string>("");
  const [verdictFilter, setVerdictFilter] = useState<string>("all");
  const [difficultyFilter, setDifficultyFilter] = useState<string>("all");
  const [page, setPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [totalCount, setTotalCount] = useState<number>(0);
  const limit = 20;

  // Fetch single submission details
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

  // Fetch all user submissions with pagination
  const fetchAllSubmissions = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      params.append("page", page.toString());
      params.append("limit", limit.toString());

      const data = await apiFetch<SubmissionListResponse>(`/coding/submissions?${params.toString()}`);
      setSubmissionsList(data.submissions);
      setTotalPages(data.total_pages);
      setTotalCount(data.total_count);
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

  // Client-side filtering for fast searching within the page
  const filteredSubmissions = useMemo(() => {
    return submissionsList.filter((item) => {
      // Search title
      if (search.trim()) {
        const query = search.toLowerCase();
        const matchesTitle = item.question_title?.toLowerCase().includes(query);
        const matchesTopic = item.question_topic?.toLowerCase().includes(query);
        if (!matchesTitle && !matchesTopic) return false;
      }

      // Verdict filter
      if (verdictFilter !== "all") {
        const itemVerdict = (item.verdict || item.status).toLowerCase();
        if (verdictFilter === "accepted" && !itemVerdict.includes("accepted")) return false;
        if (verdictFilter === "wrong_answer" && !itemVerdict.includes("wrong")) return false;
        if (verdictFilter === "error" && (!itemVerdict.includes("error") && !itemVerdict.includes("failed"))) return false;
        if (verdictFilter === "timeout" && !itemVerdict.includes("time")) return false;
      }

      // Difficulty filter
      if (difficultyFilter !== "all") {
        if (item.question_difficulty?.toLowerCase() !== difficultyFilter.toLowerCase()) return false;
      }

      return true;
    });
  }, [submissionsList, search, verdictFilter, difficultyFilter]);

  if (authLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <RefreshCw className="w-8 h-8 text-sky-400 animate-spin" />
      </div>
    );
  }

  if (!user) {
    router.push("/login");
    return null;
  }

  const copyCode = (code: string) => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getDifficultyBadge = (difficulty?: Difficulty | string | null) => {
    if (!difficulty) return <span className="text-slate-500">—</span>;
    switch (difficulty) {
      case "Easy":
        return (
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            Easy
          </span>
        );
      case "Medium":
        return (
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">
            Medium
          </span>
        );
      case "Hard":
        return (
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20">
            Hard
          </span>
        );
      default:
        return (
          <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-800 text-slate-300">
            {difficulty}
          </span>
        );
    }
  };

  // =========================================================================
  // VIEW: SINGLE SUBMISSION DEEP-DIVE
  // =========================================================================
  if (submissionId) {
    if (loading) {
      return (
        <div className="py-20 text-center space-y-3">
          <RefreshCw className="w-8 h-8 text-sky-400 animate-spin mx-auto" />
          <p className="text-sm text-slate-400">Loading submission diagnostic...</p>
        </div>
      );
    }

    if (error || !submission) {
      return (
        <div className="glass-card p-12 text-center space-y-4 max-w-lg mx-auto my-12">
          <p className="text-sm text-rose-400">{error || "Submission not found or unauthorized."}</p>
          <Link
            href="/coding/results"
            className="inline-flex items-center gap-1.5 px-4 py-2 bg-slate-800 text-white rounded-lg text-xs font-semibold hover:bg-slate-700 transition"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>View All Submissions</span>
          </Link>
        </div>
      );
    }

    return (
      <div className="space-y-6 py-2">
        {/* Navigation & Breadcrumb */}
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <Link
              href="/coding/results"
              className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-white transition font-medium"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>All Submissions</span>
            </Link>
            <span className="text-slate-600">/</span>
            <span className="text-xs text-slate-300 font-mono">
              Submission #{submission.id.slice(0, 8)}
            </span>
          </div>

          <div className="flex items-center gap-3">
            {submission.question_id && (
              <Link
                href={`/coding/${submission.question_id}`}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-sky-600 hover:bg-sky-500 text-white text-xs font-semibold transition"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                <span>Retry in Workspace</span>
              </Link>
            )}
          </div>
        </div>

        {/* Problem Attempt Header Card */}
        <div className="glass-card p-5 space-y-3 border-l-4 border-l-sky-500">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <div className="text-[11px] text-slate-400 uppercase tracking-wider font-semibold">
                Problem Attempt
              </div>
              <h1 className="text-xl md:text-2xl font-bold text-white mt-0.5">
                {submission.question_title || "Coding Problem"}
              </h1>
            </div>

            <div className="flex items-center gap-2">
              {getDifficultyBadge(submission.question_difficulty)}
              {submission.question_topic && (
                <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-800 text-sky-400 border border-slate-700">
                  <Layers className="w-3 h-3 text-sky-400" />
                  {submission.question_topic}
                </span>
              )}
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-4 text-xs text-slate-400 pt-2 border-t border-slate-800">
            <div>
              Status:{" "}
              <strong className="text-slate-200 capitalize font-medium">{submission.status}</strong>
            </div>
            <div>•</div>
            <div>
              Language:{" "}
              <strong className="text-slate-200 uppercase font-mono">{submission.language}</strong>
            </div>
            <div>•</div>
            <div>
              Submitted:{" "}
              <strong className="text-slate-200 font-medium">
                {new Date(submission.created_at).toLocaleString()}
              </strong>
            </div>
          </div>
        </div>

        {/* Detailed Results Component (Score, Tests, Execution time, Memory, Test case tabs) */}
        <SubmissionResult submission={submission} />

        {/* Submitted Code Viewer */}
        <div className="glass-card p-5 space-y-3">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <div className="flex items-center gap-2 text-xs font-semibold text-white">
              <FileCode className="w-4 h-4 text-sky-400" />
              <span>Submitted Solution Source Code ({submission.language})</span>
            </div>

            <button
              onClick={() => copyCode(submission.code)}
              className="inline-flex items-center gap-1 text-xs text-slate-300 hover:text-white px-2.5 py-1 rounded bg-slate-800 border border-slate-700 transition"
            >
              {copied ? (
                <>
                  <Check className="w-3.5 h-3.5 text-emerald-400" />
                  <span className="text-emerald-400">Copied</span>
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5" />
                  <span>Copy Code</span>
                </>
              )}
            </button>
          </div>

          <pre className="p-4 bg-slate-950 border border-slate-800 rounded-lg text-xs font-mono text-slate-200 overflow-x-auto whitespace-pre leading-6">
            {submission.code}
          </pre>
        </div>
      </div>
    );
  }

  // =========================================================================
  // VIEW: ALL SUBMISSIONS HISTORY LIST
  // =========================================================================
  return (
    <div className="space-y-6 py-2">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs text-slate-400 mb-1">
            <Link href="/coding" className="hover:text-white transition">
              Coding Assessment
            </Link>
            <span>/</span>
            <span className="text-slate-200 font-medium">Results & History</span>
          </div>
          <h1 className="text-2xl font-extrabold text-white">
            Submission Diagnostic History
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Browse verified execution logs, test-case pass rates, and performance metrics across all your problem attempts.
          </p>
        </div>

        <Link
          href="/coding"
          className="inline-flex items-center gap-1.5 px-4 py-2 bg-sky-600 hover:bg-sky-500 text-white rounded-lg text-xs font-semibold transition"
        >
          <Code2 className="w-4 h-4" />
          <span>Practice Problems</span>
        </Link>
      </div>

      {/* Filter & Search Bar */}
      <div className="glass-card p-4 space-y-3">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {/* Search input */}
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search problem title or topic..."
              className="w-full bg-slate-900 border border-slate-700 rounded-lg pl-9 pr-3 py-1.5 text-xs text-slate-100 placeholder-slate-400 focus:outline-none focus:border-sky-500"
            />
          </div>

          {/* Verdict Filter */}
          <div>
            <select
              value={verdictFilter}
              onChange={(e) => setVerdictFilter(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
            >
              <option value="all">All Verdicts</option>
              <option value="accepted">Accepted (100% Passed)</option>
              <option value="wrong_answer">Wrong Answer</option>
              <option value="timeout">Time Limit Exceeded</option>
              <option value="error">Runtime / Compilation Errors</option>
            </select>
          </div>

          {/* Difficulty Filter */}
          <div>
            <select
              value={difficultyFilter}
              onChange={(e) => setDifficultyFilter(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
            >
              <option value="all">All Difficulties</option>
              <option value="Easy">Easy</option>
              <option value="Medium">Medium</option>
              <option value="Hard">Hard</option>
            </select>
          </div>
        </div>
      </div>

      {/* History Table */}
      <div className="glass-card overflow-hidden">
        {loading ? (
          <div className="py-16 text-center space-y-3">
            <RefreshCw className="w-8 h-8 text-sky-400 animate-spin mx-auto" />
            <p className="text-sm text-slate-400">Loading submissions history...</p>
          </div>
        ) : error ? (
          <div className="py-12 text-center space-y-3">
            <p className="text-sm text-rose-400">{error}</p>
            <button
              onClick={fetchAllSubmissions}
              className="px-4 py-2 bg-slate-800 text-xs text-slate-200 hover:text-white rounded-lg border border-slate-700"
            >
              Retry
            </button>
          </div>
        ) : filteredSubmissions.length === 0 ? (
          <div className="py-16 text-center space-y-3">
            <Code2 className="w-10 h-10 text-slate-600 mx-auto" />
            <h3 className="text-sm font-semibold text-white">No submissions found</h3>
            <p className="text-xs text-slate-400 max-w-sm mx-auto">
              {search || verdictFilter !== "all" || difficultyFilter !== "all"
                ? "No submissions matched your current filters."
                : "You have not submitted any solutions yet. Go to the Problem Bank and solve your first challenge!"}
            </p>
            {(search || verdictFilter !== "all" || difficultyFilter !== "all") && (
              <button
                onClick={() => {
                  setSearch("");
                  setVerdictFilter("all");
                  setDifficultyFilter("all");
                }}
                className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 rounded-lg border border-slate-700"
              >
                Reset Filters
              </button>
            )}
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-900/80 text-slate-400 uppercase text-[11px] font-semibold border-b border-slate-800">
                <tr>
                  <th className="px-5 py-3">Status / Verdict</th>
                  <th className="px-5 py-3">Problem Title</th>
                  <th className="px-5 py-3">Topic</th>
                  <th className="px-5 py-3">Difficulty</th>
                  <th className="px-5 py-3">Language</th>
                  <th className="px-5 py-3">Tests Passed</th>
                  <th className="px-5 py-3">Score</th>
                  <th className="px-5 py-3">Submitted At</th>
                  <th className="px-5 py-3 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 text-slate-200">
                {filteredSubmissions.map((sub) => {
                  const verdictStr = sub.verdict || sub.status;
                  const isAccepted = verdictStr.toLowerCase().includes("accepted");
                  const isTimeout = verdictStr.toLowerCase().includes("time");
                  const isError = verdictStr.toLowerCase().includes("error") || verdictStr.toLowerCase().includes("failed");

                  return (
                    <tr key={sub.id} className="hover:bg-slate-800/40 transition">
                      {/* Verdict */}
                      <td className="px-5 py-3.5">
                        <span
                          className={`font-semibold inline-flex items-center gap-1 ${
                            isAccepted
                              ? "text-emerald-400"
                              : isTimeout
                              ? "text-amber-400"
                              : isError
                              ? "text-rose-400"
                              : "text-rose-400"
                          }`}
                        >
                          {isAccepted ? (
                            <CheckCircle2 className="w-3.5 h-3.5" />
                          ) : isTimeout ? (
                            <Clock className="w-3.5 h-3.5" />
                          ) : (
                            <XCircle className="w-3.5 h-3.5" />
                          )}
                          <span>{verdictStr}</span>
                        </span>
                      </td>

                      {/* Problem Title */}
                      <td className="px-5 py-3.5 font-medium text-white">
                        <Link href={`/coding/${sub.question_id}`} className="hover:text-sky-400 transition">
                          {sub.question_title || "Problem"}
                        </Link>
                      </td>

                      {/* Topic */}
                      <td className="px-5 py-3.5 text-slate-400">{sub.question_topic || "—"}</td>

                      {/* Difficulty */}
                      <td className="px-5 py-3.5">{getDifficultyBadge(sub.question_difficulty)}</td>

                      {/* Language */}
                      <td className="px-5 py-3.5 font-mono text-[11px] text-slate-300 uppercase">
                        {sub.language}
                      </td>

                      {/* Tests Passed / Total */}
                      <td className="px-5 py-3.5 text-slate-300">
                        {sub.passed_test_cases !== undefined && sub.total_test_cases !== undefined && sub.total_test_cases !== null ? (
                          <span className={sub.passed_test_cases === sub.total_test_cases ? "text-emerald-400 font-semibold" : "text-slate-300"}>
                            {sub.passed_test_cases} / {sub.total_test_cases}
                          </span>
                        ) : (
                          "—"
                        )}
                      </td>

                      {/* Score */}
                      <td className="px-5 py-3.5 font-bold text-white">
                        {sub.score !== undefined && sub.score !== null ? (
                          <span className={sub.score === 100 ? "text-emerald-400" : "text-white"}>
                            {sub.score.toFixed(0)}/100
                          </span>
                        ) : (
                          "—"
                        )}
                      </td>

                      {/* Date */}
                      <td className="px-5 py-3.5 text-slate-400 text-[11px]">
                        {new Date(sub.created_at).toLocaleString()}
                      </td>

                      {/* Action */}
                      <td className="px-5 py-3.5 text-right">
                        <Link
                          href={`/coding/results?submissionId=${sub.id}`}
                          className="inline-flex items-center gap-1 text-xs text-sky-400 hover:text-sky-300 font-medium"
                        >
                          <span>Diagnostics</span>
                          <ExternalLink className="w-3.5 h-3.5" />
                        </Link>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="px-5 py-3 bg-slate-900/60 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
            <div>
              Showing page {page} of {totalPages} ({totalCount} total submissions)
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page <= 1 || loading}
                className="p-1.5 bg-slate-800 hover:bg-slate-700 disabled:opacity-40 rounded text-slate-300"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <span>{page} / {totalPages}</span>
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page >= totalPages || loading}
                className="p-1.5 bg-slate-800 hover:bg-slate-700 disabled:opacity-40 rounded text-slate-300"
              >
                <ChevronRight className="w-4 h-4" />
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
        <div className="py-20 text-center space-y-3">
          <RefreshCw className="w-8 h-8 text-sky-400 animate-spin mx-auto" />
          <p className="text-sm text-slate-400">Loading results...</p>
        </div>
      }
    >
      <ResultsContent />
    </Suspense>
  );
}
