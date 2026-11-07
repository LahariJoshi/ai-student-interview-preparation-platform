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
      setTopics(data || []);
    } catch (err) {
      console.warn("Could not load topics summary:", err);
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

      if (search.trim()) params.append("search", search.trim());
      if (selectedTopic !== "All") params.append("topic", selectedTopic);
      if (selectedDifficulty !== "All") params.append("difficulty", selectedDifficulty);
      if (selectedStatus !== "all") params.append("status", selectedStatus);

      const res = await apiFetch<QuestionListResponse>(`/coding/questions?${params.toString()}`);
      setQuestions(res.questions || []);
      setTotalPages(res.total_pages || 1);
      setTotalCount(res.total_count || 0);
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
          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
            Easy
          </span>
        );
      case "Medium":
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-bold bg-[#FFF6E8] text-[#F5A623] border border-[#F5A623]/30">
            Medium
          </span>
        );
      case "Hard":
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-bold bg-red-50 text-red-600 border border-red-200">
            Hard
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-bold bg-slate-100 text-slate-600">
            {difficulty}
          </span>
        );
    }
  };

  return (
    <div className="space-y-5">
      {/* Search & Filter Toolbar */}
      <div className="bg-white rounded-2xl p-5 shadow-card border border-[#E5E9EF] space-y-4">
        <div className="flex flex-col md:flex-row gap-3 items-stretch md:items-center justify-between">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-[#8993A0] absolute left-3.5 top-1/2 -translate-y-1/2" />
            <input
              type="text"
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                setPage(1);
              }}
              placeholder="Search by problem title, algorithmic pattern, or description..."
              className="w-full bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl pl-10 pr-4 py-2.5 text-xs text-[#202B38] placeholder-[#8993A0] focus:outline-none focus:border-[#123E63] transition"
            />
          </div>

          <button
            onClick={handlePickRandom}
            disabled={randomLoading}
            className="inline-flex items-center justify-center gap-2 px-4 py-2.5 bg-[#F5A623] hover:bg-[#E09212] text-white rounded-xl text-xs font-bold transition shadow-sm disabled:opacity-50 shrink-0"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>{randomLoading ? "Selecting..." : "Pick Random Question"}</span>
          </button>
        </div>

        {/* Filter Selectors */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 pt-3 border-t border-[#E5E9EF]">
          <div>
            <label className="block text-[10px] font-bold text-[#8993A0] uppercase tracking-wider mb-1">Topic</label>
            <select
              value={selectedTopic}
              onChange={(e) => {
                setSelectedTopic(e.target.value);
                setPage(1);
              }}
              className="w-full bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl px-3 py-1.5 text-xs text-[#202B38] font-medium focus:outline-none focus:border-[#123E63]"
            >
              <option value="All">All Topics ({totalCount})</option>
              {topics.map((t) => (
                <option key={t.topic} value={t.topic}>
                  {t.topic} ({t.question_count})
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-[10px] font-bold text-[#8993A0] uppercase tracking-wider mb-1">Difficulty</label>
            <select
              value={selectedDifficulty}
              onChange={(e) => {
                setSelectedDifficulty(e.target.value);
                setPage(1);
              }}
              className="w-full bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl px-3 py-1.5 text-xs text-[#202B38] font-medium focus:outline-none focus:border-[#123E63]"
            >
              <option value="All">All Difficulties</option>
              <option value="Easy">Easy</option>
              <option value="Medium">Medium</option>
              <option value="Hard">Hard</option>
            </select>
          </div>

          <div>
            <label className="block text-[10px] font-bold text-[#8993A0] uppercase tracking-wider mb-1">Solve Status</label>
            <select
              value={selectedStatus}
              onChange={(e) => {
                setSelectedStatus(e.target.value as SolveStatus);
                setPage(1);
              }}
              className="w-full bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl px-3 py-1.5 text-xs text-[#202B38] font-medium focus:outline-none focus:border-[#123E63]"
            >
              <option value="all">All Problems</option>
              <option value="solved">Solved</option>
              <option value="unsolved">Unsolved</option>
            </select>
          </div>

          <div>
            <label className="block text-[10px] font-bold text-[#8993A0] uppercase tracking-wider mb-1">Sort</label>
            <div className="flex gap-1.5">
              <select
                value={sortBy}
                onChange={(e) => {
                  setSortBy(e.target.value);
                  setPage(1);
                }}
                className="flex-1 bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl px-3 py-1.5 text-xs text-[#202B38] font-medium focus:outline-none focus:border-[#123E63]"
              >
                <option value="created_at">Date Added</option>
                <option value="title">Title</option>
                <option value="difficulty">Difficulty</option>
              </select>
              <button
                onClick={() => setSortOrder((prev) => (prev === "asc" ? "desc" : "asc"))}
                title={`Sort ${sortOrder === "asc" ? "Ascending" : "Descending"}`}
                className="p-1.5 bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl text-[#8993A0] hover:text-[#202B38]"
              >
                <ArrowUpDown className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Questions Table */}
      <div className="bg-white rounded-2xl shadow-card border border-[#E5E9EF] overflow-hidden">
        {loading ? (
          <div className="py-16 text-center space-y-2 text-[#8993A0]">
            <RefreshCw className="w-6 h-6 text-[#123E63] animate-spin mx-auto" />
            <p className="text-xs font-semibold">Loading questions list...</p>
          </div>
        ) : error ? (
          <div className="py-12 text-center space-y-3">
            <p className="text-xs text-red-600 font-bold">{error}</p>
            <button
              onClick={fetchQuestions}
              className="px-3 py-1.5 bg-[#123E63] text-xs font-bold text-white rounded-lg"
            >
              Retry
            </button>
          </div>
        ) : questions.length === 0 ? (
          <div className="py-16 text-center space-y-3 text-[#8993A0]">
            <Code2 className="w-10 h-10 text-[#BCD3E6] mx-auto" />
            <p className="text-sm font-bold text-[#202B38]">No coding problems match filters</p>
            <button
              onClick={resetFilters}
              className="px-4 py-2 bg-[#123E63] text-white text-xs font-bold rounded-xl"
            >
              Reset Filters
            </button>
          </div>
        ) : (
          <div className="divide-y divide-[#E5E9EF]">
            {/* Header */}
            <div className="grid grid-cols-12 gap-4 px-5 py-3 text-[11px] font-bold text-[#8993A0] bg-[#F8F9FA] uppercase tracking-wider">
              <div className="col-span-1 text-center">Status</div>
              <div className="col-span-6">Problem Title</div>
              <div className="col-span-3">Topic</div>
              <div className="col-span-2 text-right">Difficulty</div>
            </div>

            {/* Rows */}
            {questions.map((q) => (
              <div
                key={q.id}
                onClick={() => {
                  if (onSelectQuestion) onSelectQuestion(q);
                  else router.push(`/coding/${q.id}`);
                }}
                className="grid grid-cols-12 gap-4 px-5 py-3.5 items-center hover:bg-[#F8F9FA] cursor-pointer transition group"
              >
                <div className="col-span-1 flex justify-center">
                  {q.is_solved ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                  ) : (
                    <Circle className="w-4 h-4 text-slate-300 group-hover:text-slate-400" />
                  )}
                </div>

                <div className="col-span-6">
                  <Link
                    href={`/coding/${q.id}`}
                    onClick={(e) => e.stopPropagation()}
                    className="text-xs font-bold text-[#202B38] group-hover:text-[#123E63] transition"
                  >
                    {q.title}
                  </Link>
                  <p className="text-[10px] text-[#8993A0] mt-0.5">
                    {q.sample_test_case_count} sample test {q.sample_test_case_count === 1 ? "case" : "cases"}
                  </p>
                </div>

                <div className="col-span-3">
                  <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-[11px] font-semibold bg-[#F1F3F6] text-[#123E63] border border-[#E5E9EF]">
                    <Layers className="w-3 h-3 text-[#F5A623]" />
                    {q.topic}
                  </span>
                </div>

                <div className="col-span-2 text-right">
                  {getDifficultyBadge(q.difficulty)}
                </div>
              </div>
            ))}
          </div>
        )}

        {totalPages > 1 && (
          <div className="px-5 py-3 bg-[#F8F9FA] border-t border-[#E5E9EF] flex items-center justify-between text-xs text-[#8993A0]">
            <div>
              Showing {questions.length} of {totalCount} questions
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                disabled={page <= 1 || loading}
                className="p-1.5 bg-white border border-[#E5E9EF] rounded-lg text-[#202B38] disabled:opacity-40"
              >
                <ChevronLeft className="w-3.5 h-3.5" />
              </button>
              <span>
                Page <strong className="text-[#202B38]">{page}</strong> of <strong className="text-[#202B38]">{totalPages}</strong>
              </span>
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
