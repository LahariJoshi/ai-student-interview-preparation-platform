"use client";

import React, { useEffect, useState, useCallback, useMemo } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import { InterviewHistoryItem, InterviewHistoryPagination } from "@/types/interview";
import {
  Calendar,
  Clock,
  CheckCircle2,
  Play,
  Award,
  Sparkles,
  ArrowLeft,
  ArrowRight,
  RotateCcw,
  Loader2,
  AlertCircle,
  Search,
  Filter,
  Mic,
  ChevronLeft,
  ChevronRight,
  Plus,
  HelpCircle,
} from "lucide-react";

export default function InterviewHistoryPage() {
  const { user, isLoading: isAuthLoading } = useAuth();
  const router = useRouter();

  const [historyData, setHistoryData] = useState<InterviewHistoryPagination | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Pagination state
  const [page, setPage] = useState<number>(1);
  const [pageSize, setPageSize] = useState<number>(10);

  // Client-side search & filtering
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [typeFilter, setTypeFilter] = useState<string>("ALL");
  const [statusFilter, setStatusFilter] = useState<string>("ALL");

  // Redirect unauthenticated users
  useEffect(() => {
    if (!isAuthLoading && !user) {
      router.push("/login");
    }
  }, [user, isAuthLoading, router]);

  // Fetch interview history from backend API
  const fetchHistory = useCallback(async () => {
    if (!user) return;
    try {
      setIsLoading(true);
      setError(null);

      const skip = (page - 1) * pageSize;
      const data = await apiFetch<InterviewHistoryPagination>(
        `/interview/history?skip=${skip}&limit=${pageSize}`
      );
      setHistoryData(data);
    } catch (err: any) {
      setError(err.message || "Failed to load interview history records.");
    } finally {
      setIsLoading(false);
    }
  }, [user, page, pageSize]);

  useEffect(() => {
    if (user) {
      fetchHistory();
    }
  }, [user, fetchHistory]);

  // Filtered items based on local search term and dropdown filters
  const filteredItems = useMemo(() => {
    if (!historyData?.items) return [];

    return historyData.items.filter((item) => {
      const matchesSearch =
        searchTerm.trim() === "" ||
        item.target_role.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.interview_type.toLowerCase().includes(searchTerm.toLowerCase());

      const matchesType =
        typeFilter === "ALL" ||
        item.interview_type.toUpperCase() === typeFilter.toUpperCase();

      const matchesStatus =
        statusFilter === "ALL" ||
        item.status.toUpperCase() === statusFilter.toUpperCase();

      return matchesSearch && matchesType && matchesStatus;
    });
  }, [historyData, searchTerm, typeFilter, statusFilter]);

  // Helper formatting for status badge
  const renderStatusBadge = (status: string) => {
    switch (status.toLowerCase()) {
      case "completed":
        return (
          <span className="inline-flex items-center gap-1 text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-emerald-950/80 text-emerald-400 border border-emerald-500/30">
            <CheckCircle2 className="w-3 h-3" />
            <span>Completed</span>
          </span>
        );
      case "in_progress":
        return (
          <span className="inline-flex items-center gap-1 text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-amber-950/80 text-amber-400 border border-amber-500/30">
            <Play className="w-3 h-3 fill-current" />
            <span>In Progress</span>
          </span>
        );
      case "abandoned":
        return (
          <span className="inline-flex items-center gap-1 text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-rose-950/80 text-rose-400 border border-rose-500/30">
            <AlertCircle className="w-3 h-3" />
            <span>Abandoned</span>
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 text-[11px] font-semibold px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
            <Clock className="w-3 h-3" />
            <span>Pending</span>
          </span>
        );
    }
  };

  // Helper score rendering
  const renderScore = (score: number | null | undefined, label: string) => {
    if (score === null || score === undefined) {
      return (
        <span className="text-slate-500 text-xs font-mono" title={`${label} not yet evaluated`}>
          —
        </span>
      );
    }

    const rounded = Math.round(score);
    let colorClass = "text-emerald-400 bg-emerald-950/40 border-emerald-500/30";
    if (rounded < 60) {
      colorClass = "text-rose-400 bg-rose-950/40 border-rose-500/30";
    } else if (rounded < 75) {
      colorClass = "text-amber-400 bg-amber-950/40 border-amber-500/30";
    }

    return (
      <span
        className={`inline-flex items-center justify-center font-bold px-2 py-0.5 rounded-md border text-xs ${colorClass}`}
      >
        {rounded}
      </span>
    );
  };

  // Auth loading state
  if (isAuthLoading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-3">
        <Loader2 className="w-8 h-8 animate-spin text-sky-400" />
        <p className="text-sm text-slate-400">Authenticating user...</p>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 space-y-6">
      {/* Header & Navigation */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Link
              href="/interview"
              className="inline-flex items-center gap-1 text-xs font-semibold text-slate-400 hover:text-sky-400 transition"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Interview Hub</span>
            </Link>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex items-center gap-3">
            <span>Interview History</span>
            <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-sky-950/80 text-sky-400 border border-sky-500/30">
              {historyData?.total ?? 0} Recorded
            </span>
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Review past mock interview evaluations, technical answers, communication feedback, and performance scores.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Link
            href="/interview/setup"
            className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold text-xs transition shadow-lg shadow-sky-500/20"
          >
            <Plus className="w-4 h-4" />
            <span>New Mock Interview</span>
          </Link>
        </div>
      </div>

      {/* Filters and Search Bar */}
      <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800 flex flex-col md:flex-row gap-3 items-stretch md:items-center justify-between shadow-sm">
        {/* Search Input */}
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search target role or interview type..."
            className="w-full pl-9 pr-4 py-2 text-xs bg-slate-950 text-white rounded-xl border border-slate-800 focus:outline-none focus:border-sky-500 transition placeholder:text-slate-500"
          />
        </div>

        {/* Filter Dropdowns */}
        <div className="flex flex-wrap items-center gap-2">
          <div className="flex items-center gap-1.5 text-xs text-slate-400 bg-slate-950 px-3 py-1.5 rounded-xl border border-slate-800">
            <Filter className="w-3.5 h-3.5 text-slate-500" />
            <span>Type:</span>
            <select
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              className="bg-transparent text-white font-medium focus:outline-none text-xs cursor-pointer"
            >
              <option value="ALL" className="bg-slate-900 text-white">All Types</option>
              <option value="TECHNICAL" className="bg-slate-900 text-white">Technical</option>
              <option value="BEHAVIORAL" className="bg-slate-900 text-white">Behavioral</option>
              <option value="HR" className="bg-slate-900 text-white">HR</option>
              <option value="MIXED" className="bg-slate-900 text-white">Mixed</option>
            </select>
          </div>

          <div className="flex items-center gap-1.5 text-xs text-slate-400 bg-slate-950 px-3 py-1.5 rounded-xl border border-slate-800">
            <span>Status:</span>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="bg-transparent text-white font-medium focus:outline-none text-xs cursor-pointer"
            >
              <option value="ALL" className="bg-slate-900 text-white">All Statuses</option>
              <option value="COMPLETED" className="bg-slate-900 text-white">Completed</option>
              <option value="IN_PROGRESS" className="bg-slate-900 text-white">In Progress</option>
              <option value="PENDING" className="bg-slate-900 text-white">Pending</option>
            </select>
          </div>

          {/* Page size picker */}
          <div className="flex items-center gap-1.5 text-xs text-slate-400 bg-slate-950 px-3 py-1.5 rounded-xl border border-slate-800">
            <span>Rows:</span>
            <select
              value={pageSize}
              onChange={(e) => {
                setPageSize(Number(e.target.value));
                setPage(1);
              }}
              className="bg-transparent text-white font-medium focus:outline-none text-xs cursor-pointer"
            >
              <option value={10} className="bg-slate-900 text-white">10</option>
              <option value={20} className="bg-slate-900 text-white">20</option>
              <option value={50} className="bg-slate-900 text-white">50</option>
            </select>
          </div>
        </div>
      </div>

      {/* Error State */}
      {error && (
        <div className="p-4 rounded-2xl bg-rose-950/40 border border-rose-500/30 flex items-center justify-between gap-3 text-sm text-rose-200">
          <div className="flex items-center gap-2.5">
            <AlertCircle className="w-5 h-5 text-rose-400 flex-shrink-0" />
            <span>{error}</span>
          </div>
          <button
            type="button"
            onClick={fetchHistory}
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 font-semibold text-xs transition"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Retry</span>
          </button>
        </div>
      )}

      {/* Loading State */}
      {isLoading ? (
        <div className="p-16 rounded-2xl bg-slate-900 border border-slate-800 flex flex-col items-center justify-center gap-3">
          <Loader2 className="w-8 h-8 animate-spin text-sky-400" />
          <p className="text-xs sm:text-sm text-slate-400">Loading your interview sessions history...</p>
        </div>
      ) : historyData && historyData.total === 0 ? (
        /* Empty State: No interviews at all */
        <div className="p-16 rounded-2xl bg-slate-900/60 border border-slate-800 border-dashed text-center flex flex-col items-center justify-center space-y-4">
          <div className="w-14 h-14 rounded-2xl bg-slate-800/80 text-sky-400 flex items-center justify-center border border-slate-700/50 shadow-inner">
            <Mic className="w-7 h-7" />
          </div>
          <div className="max-w-md">
            <h3 className="text-lg font-bold text-white">No interview records yet</h3>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">
              You have not conducted any mock interview sessions yet. Launch a session to practice technical and behavioral questions with instant AI analysis.
            </p>
          </div>
          <Link
            href="/interview/setup"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold text-xs transition shadow-lg shadow-sky-500/20"
          >
            <Plus className="w-4 h-4" />
            <span>Start Your First Interview</span>
          </Link>
        </div>
      ) : filteredItems.length === 0 ? (
        /* Empty State: Filters produced no results */
        <div className="p-12 rounded-2xl bg-slate-900/50 border border-slate-800 text-center space-y-3">
          <HelpCircle className="w-8 h-8 text-slate-500 mx-auto" />
          <h3 className="text-base font-semibold text-white">No matching interviews found</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto">
            Try adjusting your search query or clear the filter criteria to see other completed sessions.
          </p>
          <button
            type="button"
            onClick={() => {
              setSearchTerm("");
              setTypeFilter("ALL");
              setStatusFilter("ALL");
            }}
            className="text-xs font-semibold text-sky-400 hover:text-sky-300 underline"
          >
            Reset Filters
          </button>
        </div>
      ) : (
        /* Data Presentation */
        <div className="space-y-4">
          {/* Desktop Table View (>= md) */}
          <div className="hidden md:block overflow-hidden rounded-2xl bg-slate-900 border border-slate-800 shadow-sm">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs border-collapse">
                <thead>
                  <tr className="border-b border-slate-800 bg-slate-950/70 text-slate-400 uppercase tracking-wider font-semibold">
                    <th scope="col" className="px-5 py-3.5">Date</th>
                    <th scope="col" className="px-5 py-3.5">Target Role</th>
                    <th scope="col" className="px-4 py-3.5">Type</th>
                    <th scope="col" className="px-4 py-3.5 text-center">Questions</th>
                    <th scope="col" className="px-4 py-3.5 text-center">Duration</th>
                    <th scope="col" className="px-4 py-3.5 text-center">Overall</th>
                    <th scope="col" className="px-4 py-3.5 text-center">Technical</th>
                    <th scope="col" className="px-4 py-3.5 text-center">Communication</th>
                    <th scope="col" className="px-4 py-3.5 text-center">Status</th>
                    <th scope="col" className="px-5 py-3.5 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60">
                  {filteredItems.map((item) => (
                    <tr
                      key={item.id}
                      onClick={() => router.push(`/interview/result/${item.id}`)}
                      className="hover:bg-slate-800/40 transition cursor-pointer group"
                    >
                      {/* Date */}
                      <td className="px-5 py-4 whitespace-nowrap">
                        <div className="flex items-center gap-2 text-slate-300">
                          <Calendar className="w-3.5 h-3.5 text-slate-500" />
                          <span className="font-medium">
                            {new Date(item.date || item.created_at).toLocaleDateString("en-US", {
                              month: "short",
                              day: "numeric",
                              year: "numeric",
                            })}
                          </span>
                        </div>
                        <div className="text-[10px] text-slate-500 pl-5">
                          {new Date(item.date || item.created_at).toLocaleTimeString("en-US", {
                            hour: "2-digit",
                            minute: "2-digit",
                          })}
                        </div>
                      </td>

                      {/* Target Role */}
                      <td className="px-5 py-4">
                        <div className="font-bold text-white group-hover:text-sky-400 transition line-clamp-1">
                          {item.target_role}
                        </div>
                        <div className="text-[11px] text-slate-500 mt-0.5">
                          {item.experience_level || "Fresher"} • {item.difficulty || "Medium"}
                        </div>
                      </td>

                      {/* Interview Type */}
                      <td className="px-4 py-4 whitespace-nowrap">
                        <span className="inline-block px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 text-[11px] font-medium border border-slate-700/50">
                          {item.interview_type}
                        </span>
                      </td>

                      {/* Number of Questions */}
                      <td className="px-4 py-4 text-center whitespace-nowrap font-medium text-slate-300">
                        {item.number_of_questions || item.question_count}
                      </td>

                      {/* Duration */}
                      <td className="px-4 py-4 text-center whitespace-nowrap">
                        <span className="inline-flex items-center gap-1 text-[11px] text-slate-300 bg-slate-950 px-2.5 py-1 rounded-lg border border-slate-800 font-mono">
                          <Clock className="w-3 h-3 text-slate-500" />
                          {item.formatted_duration || item.duration || "0s"}
                        </span>
                      </td>

                      {/* Overall Score */}
                      <td className="px-4 py-4 text-center whitespace-nowrap">
                        {renderScore(item.overall_score, "Overall")}
                      </td>

                      {/* Technical Score */}
                      <td className="px-4 py-4 text-center whitespace-nowrap">
                        {renderScore(item.technical_score, "Technical")}
                      </td>

                      {/* Communication Score */}
                      <td className="px-4 py-4 text-center whitespace-nowrap">
                        {renderScore(item.communication_score, "Communication")}
                      </td>

                      {/* Status */}
                      <td className="px-4 py-4 text-center whitespace-nowrap">
                        {renderStatusBadge(item.status)}
                      </td>

                      {/* Action Link */}
                      <td className="px-5 py-4 text-right whitespace-nowrap">
                        <Link
                          href={`/interview/result/${item.id}`}
                          onClick={(e) => e.stopPropagation()}
                          className="inline-flex items-center gap-1 text-xs font-semibold text-sky-400 group-hover:text-sky-300 transition"
                        >
                          <span>Results</span>
                          <ArrowRight className="w-3.5 h-3.5" />
                        </Link>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Mobile Card List (< md) */}
          <div className="grid grid-cols-1 gap-3.5 md:hidden">
            {filteredItems.map((item) => (
              <div
                key={item.id}
                onClick={() => router.push(`/interview/result/${item.id}`)}
                className="p-4 rounded-2xl bg-slate-900 border border-slate-800 hover:border-slate-700 transition cursor-pointer space-y-3.5 shadow-sm"
              >
                <div className="flex items-start justify-between gap-2">
                  <div>
                    <h3 className="text-base font-bold text-white line-clamp-1">{item.target_role}</h3>
                    <div className="flex items-center gap-2 mt-1 text-[11px] text-slate-500">
                      <Calendar className="w-3 h-3" />
                      <span>{new Date(item.date || item.created_at).toLocaleDateString()}</span>
                      <span>•</span>
                      <span className="text-slate-400 font-medium">{item.interview_type}</span>
                    </div>
                  </div>
                  {renderStatusBadge(item.status)}
                </div>

                <div className="grid grid-cols-3 gap-2 p-2.5 rounded-xl bg-slate-950 border border-slate-800/80 text-center">
                  <div>
                    <div className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold">Overall</div>
                    <div className="mt-1">{renderScore(item.overall_score, "Overall")}</div>
                  </div>
                  <div>
                    <div className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold">Technical</div>
                    <div className="mt-1">{renderScore(item.technical_score, "Technical")}</div>
                  </div>
                  <div>
                    <div className="text-[10px] text-slate-500 uppercase tracking-wider font-semibold">Voice & Comm</div>
                    <div className="mt-1">{renderScore(item.communication_score, "Communication")}</div>
                  </div>
                </div>

                <div className="flex items-center justify-between text-xs text-slate-400 pt-1">
                  <div className="flex items-center gap-3">
                    <span>{item.number_of_questions || item.question_count} Questions</span>
                    <span>•</span>
                    <span className="flex items-center gap-1 font-mono">
                      <Clock className="w-3 h-3 text-slate-500" />
                      {item.formatted_duration || item.duration || "0s"}
                    </span>
                  </div>

                  <Link
                    href={`/interview/result/${item.id}`}
                    onClick={(e) => e.stopPropagation()}
                    className="inline-flex items-center gap-1 font-semibold text-sky-400"
                  >
                    <span>View Result</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </Link>
                </div>
              </div>
            ))}
          </div>

          {/* Pagination Controls */}
          {historyData && historyData.total_pages > 1 && (
            <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs">
              <div className="text-slate-400">
                Showing{" "}
                <span className="font-semibold text-white">
                  {historyData.total === 0 ? 0 : historyData.skip + 1}
                </span>{" "}
                to{" "}
                <span className="font-semibold text-white">
                  {Math.min(historyData.skip + historyData.limit, historyData.total)}
                </span>{" "}
                of <span className="font-semibold text-white">{historyData.total}</span> interviews
              </div>

              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={() => setPage((prev) => Math.max(1, prev - 1))}
                  disabled={page <= 1}
                  className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 disabled:opacity-40 disabled:cursor-not-allowed text-white font-medium transition cursor-pointer"
                >
                  <ChevronLeft className="w-3.5 h-3.5" />
                  <span>Previous</span>
                </button>

                <div className="px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-800 text-slate-300 font-medium">
                  Page {historyData.page} of {historyData.total_pages}
                </div>

                <button
                  type="button"
                  onClick={() => setPage((prev) => Math.min(historyData.total_pages, prev + 1))}
                  disabled={page >= historyData.total_pages}
                  className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 disabled:opacity-40 disabled:cursor-not-allowed text-white font-medium transition cursor-pointer"
                >
                  <span>Next</span>
                  <ChevronRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
