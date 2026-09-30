"use client";

import React, { useState, useEffect, useCallback } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { apiFetch } from "@/lib/api";
import {
  CodingQuestionSummary,
  QuestionListResponse,
  TopicSummary,
  Difficulty,
  SolveStatus,
} from "@/types/coding";
import {
  Search,
  CheckCircle2,
  Circle,
  HelpCircle,
  Sparkles,
  ArrowUpDown,
  ChevronLeft,
  ChevronRight,
  Filter,
  RefreshCw,
  Code2,
  Layers,
} from "lucide-react";

interface QuestionListProps {
  onSelectQuestion?: (question: CodingQuestionSummary) => void;
}

export default function QuestionList({ onSelectQuestion }: QuestionListProps) {
  const router = useRouter();

  // State
  const [questions, setQuestions] = useState<CodingQuestionSummary[]>([]);
  const [topics, setTopics] = useState<TopicSummary[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [randomLoading, setRandomLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Filters
  const [search, setSearch] = useState<string>("");
  const [selectedTopic, setSelectedTopic] = useState<string>("All");
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>("All");
  const [selectedStatus, setSelectedStatus] = useState<SolveStatus>("all");
  const [sortBy, setSortBy] = useState<string>("created_at");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");

  // Pagination
  const [page, setPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [totalCount, setTotalCount] = useState<number>(0);
  const limit = 15;

  // Fetch topics list
  const fetchTopics = useCallback(async () => {
    try {
      const data = await apiFetch<TopicSummary[]>("/coding/questions/topics/summary");
      setTopics(data);
    } catch (err) {
      console.warn("Could not load topics summary, falling back to empty list:", err);
    }
  }, []);

  // Fetch questions
  const fetchQuestions = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const params = new URLSearchParams();
      params.append("page", page.toString());
      params.append("limit", limit.toString());
      params.append("sort_by", sortBy);
      params.append("sort_order", sortOrder);

      if (search.trim()) {
        params.append("search", search.trim());
      }
      if (selectedTopic !== "All") {
        params.append("topic", selectedTopic);
      }
      if (selectedDifficulty !== "All") {
        params.append("difficulty", selectedDifficulty);
      }
      if (selectedStatus !== "all") {
        params.append("status", selectedStatus);
      }

      const res = await apiFetch<QuestionListResponse>(`/coding/questions?${params.toString()}`);
      setQuestions(res.questions);
      setTotalPages(res.total_pages);
      setTotalCount(res.total_count);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load questions.");
    } finally {
      setLoading(false);
    }
  }, [page, limit, sortBy, sortOrder, search, selectedTopic, selectedDifficulty, selectedStatus]);

  useEffect(() => {
    fetchTopics();
  }, [fetchTopics]);

  useEffect(() => {
    fetchQuestions();
  }, [fetchQuestions]);

  // Handle Pick Random
  const handlePickRandom = async () => {
    try {
      setRandomLoading(true);
      const params = new URLSearchParams();
      if (selectedTopic !== "All") params.append("topic", selectedTopic);
      if (selectedDifficulty !== "All") params.append("difficulty", selectedDifficulty);
      if (selectedStatus !== "all") params.append("status", selectedStatus);

      const queryStr = params.toString() ? `?${params.toString()}` : "";
      const randomQ = await apiFetch<{ id: string; slug: string }>(`/coding/questions/random${queryStr}`);
      if (randomQ && randomQ.id) {
        router.push(`/coding/${randomQ.id}`);
      }
    } catch (err) {
      alert(err instanceof Error ? err.message : "No questions matched your random selection criteria.");
    } finally {
      setRandomLoading(false);
    }
  };

  const resetFilters = () => {
    setSearch("");
    setSelectedTopic("All");
    setSelectedDifficulty("All");
    setSelectedStatus("all");
    setPage(1);
    setSortBy("created_at");
    setSortOrder("desc");
  };

  const getDifficultyBadge = (difficulty: Difficulty) => {
    switch (difficulty) {
      case "Easy":
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            Easy
          </span>
        );
      case "Medium":
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-500/10 text-amber-400 border border-amber-500/20">
            Medium
          </span>
        );
      case "Hard":
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-rose-500/10 text-rose-400 border border-rose-500/20">
            Hard
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-700 text-slate-300">
            {difficulty}
          </span>
        );
    }
  };

  return (
    <div className="space-y-6">
      {/* Controls & Filter Bar */}
      <div className="glass-card p-5 space-y-4">
        {/* Top Search & Random Action */}
        <div className="flex flex-col md:flex-row gap-3 items-stretch md:items-center justify-between">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setPage(1);
              }}
              placeholder="Search by problem title, topic, or description..."
              className="w-full bg-slate-900 border border-slate-700 rounded-lg pl-9 pr-4 py-2 text-sm text-slate-100 placeholder-slate-400 focus:outline-none focus:border-sky-500"
            />
            {search && (
              <button
                onClick={() => {
                  setSearch("");
                  setPage(1);
                }}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400 hover:text-slate-200"
              >
                Clear
              </button>
            )}
          </div>

          <button
            onClick={handlePickRandom}
            disabled={randomLoading}
            className="inline-flex items-center justify-center gap-2 px-4 py-2 bg-gradient-to-r from-sky-600 to-indigo-600 hover:from-sky-500 hover:to-indigo-500 text-white rounded-lg text-sm font-medium transition shadow-sm disabled:opacity-50"
          >
            <Sparkles className="w-4 h-4 text-sky-200" />
            {randomLoading ? "Selecting..." : "Pick Random Problem"}
          </button>
        </div>

        {/* Filter Pills / Dropdowns */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 pt-2 border-t border-slate-800">
          {/* Topic */}
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">Topic</label>
            <select
              value={selectedTopic}
              onChange={(e) => {
                setSelectedTopic(e.target.value);
                setPage(1);
              }}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
            >
              <option value="All">All Topics ({totalCount})</option>
              {topics.map((t) => (
                <option key={t.topic} value={t.topic}>
                  {t.topic} ({t.question_count})
                </option>
              ))}
            </select>
          </div>

          {/* Difficulty */}
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">Difficulty</label>
            <select
              value={selectedDifficulty}
              onChange={(e) => {
                setSelectedDifficulty(e.target.value);
                setPage(1);
              }}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
            >
              <option value="All">All Difficulties</option>
              <option value="Easy">Easy</option>
              <option value="Medium">Medium</option>
              <option value="Hard">Hard</option>
            </select>
          </div>

          {/* Status */}
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">Status</label>
            <select
              value={selectedStatus}
              onChange={(e) => {
                setSelectedStatus(e.target.value as SolveStatus);
                setPage(1);
              }}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
            >
              <option value="all">All Problems</option>
              <option value="solved">Solved</option>
              <option value="unsolved">Unsolved</option>
            </select>
          </div>

          {/* Sort */}
          <div>
            <label className="block text-xs font-medium text-slate-400 mb-1">Sort By</label>
            <div className="flex gap-2">
              <select
                value={sortBy}
                onChange={(e) => {
                  setSortBy(e.target.value);
                  setPage(1);
                }}
                className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-sky-500"
              >
                <option value="created_at">Date Added</option>
                <option value="title">Title</option>
                <option value="difficulty">Difficulty</option>
              </select>
              <button
                onClick={() => setSortOrder((prev) => (prev === "asc" ? "desc" : "asc"))}
                title={`Sort ${sortOrder === "asc" ? "Ascending" : "Descending"}`}
                className="p-1.5 bg-slate-900 border border-slate-700 rounded-lg text-slate-400 hover:text-white"
              >
                <ArrowUpDown className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Questions Table / List */}
      <div className="glass-card overflow-hidden">
        {loading ? (
          <div className="py-16 text-center space-y-3">
            <RefreshCw className="w-6 h-6 text-sky-400 animate-spin mx-auto" />
            <p className="text-sm text-slate-400">Loading coding questions...</p>
          </div>
        ) : error ? (
          <div className="py-12 text-center space-y-3">
            <p className="text-sm text-rose-400">{error}</p>
            <button
              onClick={fetchQuestions}
              className="px-3 py-1.5 bg-slate-800 text-xs text-slate-200 hover:text-white rounded-lg border border-slate-700"
            >
              Retry
            </button>
          </div>
        ) : questions.length === 0 ? (
          <div className="py-16 text-center space-y-4">
            <Code2 className="w-10 h-10 text-slate-600 mx-auto" />
            <div className="space-y-1">
              <h3 className="text-base font-semibold text-white">No coding questions found</h3>
              <p className="text-xs text-slate-400 max-w-sm mx-auto">
                No problems matched your current search and filter criteria.
              </p>
            </div>
            <button
              onClick={resetFilters}
              className="px-4 py-2 bg-sky-600 hover:bg-sky-500 text-xs font-medium text-white rounded-lg transition"
            >
              Reset Filters
            </button>
          </div>
        ) : (
          <div className="divide-y divide-slate-800">
            {/* Table Header */}
            <div className="grid grid-cols-12 gap-4 px-5 py-3 text-xs font-semibold text-slate-400 bg-slate-900/60 uppercase tracking-wider">
              <div className="col-span-1 text-center">Status</div>
              <div className="col-span-6 md:col-span-6">Problem Title</div>
              <div className="col-span-3 md:col-span-3">Topic</div>
              <div className="col-span-2 md:col-span-2 text-right">Difficulty</div>
            </div>

            {/* Rows */}
            {questions.map((q, idx) => (
              <div
                key={q.id}
                onClick={() => {
                  if (onSelectQuestion) {
                    onSelectQuestion(q);
                  } else {
                    router.push(`/coding/${q.id}`);
                  }
                }}
                className="grid grid-cols-12 gap-4 px-5 py-3.5 items-center hover:bg-slate-800/40 cursor-pointer transition group"
              >
                {/* Solved Icon */}
                <div className="col-span-1 flex justify-center">
                  {q.is_solved ? (
                    <span title="Solved">
                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    </span>
                  ) : (
                    <span title="Unsolved">
                      <Circle className="w-4 h-4 text-slate-600 group-hover:text-slate-400 transition" />
                    </span>
                  )}
                </div>

                {/* Title */}
                <div className="col-span-6 md:col-span-6">
                  <Link
                    href={`/coding/${q.id}`}
                    onClick={(e) => e.stopPropagation()}
                    className="text-sm font-medium text-slate-200 group-hover:text-sky-400 transition inline-flex items-center gap-1.5"
                  >
                    <span>{q.title}</span>
                  </Link>
                  <div className="text-[11px] text-slate-500 mt-0.5">
                    {q.sample_test_case_count} sample test {q.sample_test_case_count === 1 ? "case" : "cases"}
                  </div>
                </div>

                {/* Topic */}
                <div className="col-span-3 md:col-span-3">
                  <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-md text-xs font-medium bg-slate-800 text-slate-300 border border-slate-700">
                    <Layers className="w-3 h-3 text-sky-400" />
                    {q.topic}
                  </span>
                </div>

                {/* Difficulty */}
                <div className="col-span-2 md:col-span-2 text-right">
                  {getDifficultyBadge(q.difficulty)}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Pagination Bar */}
        {totalPages > 1 && (
          <div className="px-5 py-3 bg-slate-900/60 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
            <div>
              Showing {questions.length} of {totalCount} questions
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page <= 1 || loading}
                className="p-1.5 bg-slate-800 hover:bg-slate-700 disabled:opacity-40 disabled:hover:bg-slate-800 rounded text-slate-300"
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <span className="px-2">
                Page <strong className="text-white">{page}</strong> of <strong className="text-white">{totalPages}</strong>
              </span>
              <button
                onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                disabled={page >= totalPages || loading}
                className="p-1.5 bg-slate-800 hover:bg-slate-700 disabled:opacity-40 disabled:hover:bg-slate-800 rounded text-slate-300"
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
