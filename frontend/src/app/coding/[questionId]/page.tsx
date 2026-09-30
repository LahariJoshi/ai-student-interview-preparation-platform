"use client";

import React, { useState, useEffect, useCallback, useRef } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import {
  CodingQuestionDetail,
  CodeRunResponse,
  CodingSubmissionDetail,
  SubmissionListResponse,
  CodingSubmissionListItem,
} from "@/types/coding";
import QuestionDetails from "@/components/coding/QuestionDetails";
import CodeEditor from "@/components/coding/CodeEditor";
import SubmissionResult from "@/components/coding/SubmissionResult";
import {
  ArrowLeft,
  RefreshCw,
  History,
  Code2,
  CheckCircle2,
  AlertCircle,
  ExternalLink,
} from "lucide-react";

export default function CodingWorkspacePage() {
  const params = useParams();
  const router = useRouter();
  const { user, isLoading: authLoading } = useAuth();
  const questionIdParam = params?.questionId as string;

  const [question, setQuestion] = useState<CodingQuestionDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Execution & Submission State
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [runResult, setRunResult] = useState<CodeRunResponse | null>(null);
  const [submission, setSubmission] = useState<CodingSubmissionDetail | null>(null);

  // Past Submissions tab for this question
  const [viewTab, setViewTab] = useState<"details" | "history">("details");
  const [submissions, setSubmissions] = useState<CodingSubmissionListItem[]>([]);
  const [loadingSubmissions, setLoadingSubmissions] = useState<boolean>(false);

  const resultsRef = useRef<HTMLDivElement>(null);

  // Fetch question details
  const fetchQuestion = useCallback(async () => {
    if (!questionIdParam) return;
    setLoading(true);
    setError(null);
    try {
      const data = await apiFetch<CodingQuestionDetail>(`/coding/questions/${questionIdParam}`);
      setQuestion(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load coding question.");
    } finally {
      setLoading(false);
    }
  }, [questionIdParam]);

  // Fetch past submissions for this question
  const fetchPastSubmissions = useCallback(async (qId: string) => {
    setLoadingSubmissions(true);
    try {
      const res = await apiFetch<SubmissionListResponse>(`/coding/questions/${qId}/submissions?limit=20`);
      setSubmissions(res.submissions);
    } catch (err) {
      console.warn("Could not load submissions for question:", err);
    } finally {
      setLoadingSubmissions(false);
    }
  }, []);

  useEffect(() => {
    fetchQuestion();
  }, [fetchQuestion]);

  useEffect(() => {
    if (question?.id) {
      fetchPastSubmissions(question.id);
    }
  }, [question?.id, fetchPastSubmissions]);

  // Auth protection check
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

  // Handle Run Code (interactive sample testing)
  const handleRunCode = async (language: string, code: string) => {
    if (!question) return;
    setIsRunning(true);
    setSubmission(null);
    try {
      const result = await apiFetch<CodeRunResponse>(`/coding/questions/${question.id}/run`, {
        method: "POST",
        body: JSON.stringify({ language, code }),
      });
      setRunResult(result);
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: "smooth" });
      }, 100);
    } catch (err) {
      setRunResult({
        verdict: "Execution Failed",
        passed_test_cases: 0,
        total_test_cases: question.sample_test_cases.length,
        execution_time_ms: 0,
        error_message: err instanceof Error ? err.message : "Run execution failed.",
        test_cases: [],
      });
    } finally {
      setIsRunning(false);
    }
  };

  // Handle Submit Code (full sandbox evaluation)
  const handleSubmitCode = async (language: string, code: string) => {
    if (!question) return;
    setIsSubmitting(true);
    setRunResult(null);
    try {
      const sub = await apiFetch<CodingSubmissionDetail>(`/coding/submissions?evaluate=true`, {
        method: "POST",
        body: JSON.stringify({
          question_id: question.id,
          language,
          code,
        }),
      });
      setSubmission(sub);

      // If accepted, update local question solve status
      if (sub.result?.verdict.toLowerCase().includes("accepted")) {
        setQuestion((prev) => (prev ? { ...prev, is_solved: true } : null));
      }

      // Refresh past submissions
      fetchPastSubmissions(question.id);

      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: "smooth" });
      }, 100);
    } catch (err) {
      alert(err instanceof Error ? err.message : "Submission failed.");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-3">
        <RefreshCw className="w-8 h-8 text-sky-400 animate-spin" />
        <p className="text-sm text-slate-400">Loading problem workspace...</p>
      </div>
    );
  }

  if (error || !question) {
    return (
      <div className="glass-card p-12 text-center space-y-4 max-w-lg mx-auto my-12">
        <AlertCircle className="w-12 h-12 text-rose-400 mx-auto" />
        <h2 className="text-lg font-bold text-white">Problem Not Found</h2>
        <p className="text-xs text-slate-400">{error || "The requested problem could not be found."}</p>
        <Link
          href="/coding"
          className="inline-flex items-center gap-1.5 px-4 py-2 bg-sky-600 hover:bg-sky-500 text-white rounded-lg text-xs font-semibold transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Problem Bank</span>
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-4 py-2">
      {/* Workspace Navigation Bar */}
      <div className="flex items-center justify-between gap-4">
        <Link
          href="/coding"
          className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-white font-medium transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Problem Bank</span>
        </Link>

        {/* View mode toggle */}
        <div className="flex items-center gap-1 bg-slate-900 border border-slate-800 p-1 rounded-lg text-xs">
          <button
            onClick={() => setViewTab("details")}
            className={`px-3 py-1 rounded font-medium transition ${
              viewTab === "details"
                ? "bg-sky-600 text-white"
                : "text-slate-400 hover:text-white"
            }`}
          >
            Problem Description
          </button>
          <button
            onClick={() => setViewTab("history")}
            className={`px-3 py-1 rounded font-medium transition flex items-center gap-1.5 ${
              viewTab === "history"
                ? "bg-sky-600 text-white"
                : "text-slate-400 hover:text-white"
            }`}
          >
            <History className="w-3.5 h-3.5" />
            <span>Submissions ({submissions.length})</span>
          </button>
        </div>
      </div>

      {/* Main Split Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Side: Problem Details or Submissions */}
        <div className="lg:col-span-5 h-full">
          {viewTab === "details" ? (
            <QuestionDetails question={question} />
          ) : (
            <div className="glass-card p-5 space-y-4">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <h3 className="text-sm font-bold text-white flex items-center gap-1.5">
                  <History className="w-4 h-4 text-sky-400" />
                  <span>My Submissions for this Problem</span>
                </h3>
                <button
                  onClick={() => fetchPastSubmissions(question.id)}
                  disabled={loadingSubmissions}
                  className="text-xs text-slate-400 hover:text-white"
                >
                  <RefreshCw className={`w-3.5 h-3.5 ${loadingSubmissions ? "animate-spin" : ""}`} />
                </button>
              </div>

              {submissions.length === 0 ? (
                <div className="py-12 text-center text-xs text-slate-400 space-y-1">
                  <p>You have not submitted any solutions for this problem yet.</p>
                  <p className="text-slate-500">Write your code and click &quot;Submit Solution&quot;.</p>
                </div>
              ) : (
                <div className="divide-y divide-slate-800 text-xs">
                  {submissions.map((sub) => {
                    const isAccepted = sub.verdict?.toLowerCase().includes("accepted");
                    return (
                      <div
                        key={sub.id}
                        className="py-3 flex items-center justify-between hover:bg-slate-800/30 px-2 rounded transition"
                      >
                        <div className="space-y-0.5">
                          <div className="flex items-center gap-2">
                            <span
                              className={`font-semibold ${
                                isAccepted ? "text-emerald-400" : "text-rose-400"
                              }`}
                            >
                              {sub.verdict || sub.status}
                            </span>
                            <span className="font-mono text-[11px] text-slate-400 uppercase">
                              {sub.language}
                            </span>
                          </div>
                          <div className="text-[11px] text-slate-500">
                            {new Date(sub.created_at).toLocaleString()}
                          </div>
                        </div>

                        <div className="flex items-center gap-3">
                          {sub.score !== undefined && sub.score !== null && (
                            <span className="font-bold text-white text-xs">
                              {sub.score.toFixed(0)}/100
                            </span>
                          )}
                          <Link
                            href={`/coding/results?submissionId=${sub.id}`}
                            className="p-1 hover:text-sky-400 text-slate-400"
                            title="View submission details"
                          >
                            <ExternalLink className="w-3.5 h-3.5" />
                          </Link>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Right Side: Code Editor & Result Dock */}
        <div className="lg:col-span-7 space-y-4">
          <CodeEditor
            questionId={question.id}
            starterCodeMap={question.starter_code || {}}
            onRunCode={handleRunCode}
            onSubmitCode={handleSubmitCode}
            isRunning={isRunning}
            isSubmitting={isSubmitting}
          />

          {/* Test Case / Submission Execution Dock */}
          <div ref={resultsRef}>
            <SubmissionResult
              runResult={runResult}
              submission={submission}
              isEvaluating={isRunning || isSubmitting}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
