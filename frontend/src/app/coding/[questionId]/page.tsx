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

  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [runResult, setRunResult] = useState<CodeRunResponse | null>(null);
  const [submission, setSubmission] = useState<CodingSubmissionDetail | null>(null);

  const [viewTab, setViewTab] = useState<"details" | "history">("details");
  const [submissions, setSubmissions] = useState<CodingSubmissionListItem[]>([]);
  const [loadingSubmissions, setLoadingSubmissions] = useState<boolean>(false);

  const resultsRef = useRef<HTMLDivElement>(null);

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

  const fetchPastSubmissions = useCallback(async (qId: string) => {
    setLoadingSubmissions(true);
    try {
      const res = await apiFetch<SubmissionListResponse>(`/coding/questions/${qId}/submissions?limit=20`);
      setSubmissions(res.submissions || []);
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

  const handleRunCode = async (language: string, code: string) => {
    if (!question) return;
    setIsRunning(true);
    setSubmission(null);
    try {
      const result = await apiFetch<CodeRunResponse>(`/coding/run`, {
        method: "POST",
        body: JSON.stringify({ question_id: question.id, language, code }),
      });
      setRunResult(result);
      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: "smooth" });
      }, 100);
    } catch (err: any) {
      setRunResult({
        verdict: "Execution Service Error",
        passed_test_cases: 0,
        total_test_cases: question.sample_test_cases?.length || 0,
        execution_time_ms: 0,
        error_message: err.message || "Failed to execute code.",
        test_cases: [],
      });
    } finally {
      setIsRunning(false);
    }
  };

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

      if (sub.result?.verdict.toLowerCase().includes("accepted")) {
        setQuestion((prev) => (prev ? { ...prev, is_solved: true } : null));
      }

      fetchPastSubmissions(question.id);

      setTimeout(() => {
        resultsRef.current?.scrollIntoView({ behavior: "smooth" });
      }, 100);
    } catch (err: any) {
      setRunResult({
        verdict: "Submission Error",
        passed_test_cases: 0,
        total_test_cases: question.sample_test_cases?.length || 0,
        execution_time_ms: 0,
        error_message: err.message || "Submission failed.",
        test_cases: [],
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="py-20 text-center space-y-2 text-[#8993A0]">
        <RefreshCw className="w-8 h-8 text-[#123E63] animate-spin mx-auto" />
        <p className="text-xs font-semibold">Loading problem workspace...</p>
      </div>
    );
  }

  if (error || !question) {
    return (
      <div className="bg-white rounded-2xl p-8 text-center space-y-4 max-w-lg mx-auto my-12 shadow-card border border-[#E5E9EF]">
        <AlertCircle className="w-10 h-10 text-red-500 mx-auto" />
        <h3 className="text-base font-bold text-[#202B38]">Problem Not Found</h3>
        <p className="text-xs text-[#8993A0]">{error || "The requested problem could not be found."}</p>
        <Link
          href="/coding"
          className="inline-flex items-center gap-1.5 px-4 py-2 bg-[#123E63] text-white rounded-xl text-xs font-bold transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Problem Bank</span>
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Workspace Bar */}
      <div className="flex items-center justify-between gap-4">
        <Link
          href="/coding"
          className="inline-flex items-center gap-1.5 text-xs text-[#8993A0] hover:text-[#123E63] font-bold transition"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Problems</span>
        </Link>

        {/* View mode toggle */}
        <div className="flex items-center gap-1 bg-white border border-[#E5E9EF] p-1 rounded-xl text-xs shadow-xs">
          <button
            onClick={() => setViewTab("details")}
            className={`px-3 py-1.5 rounded-lg font-bold transition ${
              viewTab === "details"
                ? "bg-[#123E63] text-white shadow-xs"
                : "text-[#8993A0] hover:text-[#202B38]"
            }`}
          >
            Description
          </button>
          <button
            onClick={() => setViewTab("history")}
            className={`px-3 py-1.5 rounded-lg font-bold transition flex items-center gap-1.5 ${
              viewTab === "history"
                ? "bg-[#123E63] text-white shadow-xs"
                : "text-[#8993A0] hover:text-[#202B38]"
            }`}
          >
            <History className="w-3.5 h-3.5" />
            <span>Submissions ({submissions.length})</span>
          </button>
        </div>
      </div>

      {/* Main Split Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 items-start">
        {/* Left Side: Question Details / Submissions */}
        <div className="lg:col-span-5 h-full">
          {viewTab === "details" ? (
            <QuestionDetails question={question} />
          ) : (
            <div className="bg-white rounded-2xl p-5 space-y-4 shadow-card border border-[#E5E9EF]">
              <div className="flex items-center justify-between pb-3 border-b border-[#E5E9EF]">
                <h3 className="text-sm font-bold text-[#202B38] flex items-center gap-1.5">
                  <History className="w-4 h-4 text-[#123E63]" />
                  <span>My Submissions for this Problem</span>
                </h3>
                <button
                  onClick={() => fetchPastSubmissions(question.id)}
                  disabled={loadingSubmissions}
                  className="text-xs text-[#8993A0] hover:text-[#202B38]"
                >
                  Refresh
                </button>
              </div>

              {submissions.length === 0 ? (
                <div className="py-8 text-center text-[#8993A0] text-xs">
                  No submissions yet. Submit your code to see results here.
                </div>
              ) : (
                <div className="space-y-2 max-h-[500px] overflow-y-auto pr-1">
                  {submissions.map((sub) => {
                    const isAccepted = sub.verdict?.toLowerCase().includes("accepted");
                    return (
                      <div
                        key={sub.id}
                        className="p-3 rounded-xl border border-[#E5E9EF] bg-[#F8F9FA] hover:bg-white transition flex items-center justify-between text-xs"
                      >
                        <div>
                          <div className="flex items-center gap-1.5 font-bold">
                            <span className={isAccepted ? "text-emerald-600" : "text-red-600"}>
                              {sub.verdict || sub.status}
                            </span>
                            <span className="text-[#8993A0] text-[10px] font-normal font-mono">
                              ({sub.language})
                            </span>
                          </div>
                          <p className="text-[10px] text-[#8993A0] mt-0.5">
                            {new Date(sub.created_at).toLocaleString()}
                          </p>
                        </div>

                        <Link
                          href={`/coding/results?submissionId=${sub.id}`}
                          className="text-xs font-bold text-[#123E63] hover:text-[#0D3557] flex items-center gap-1"
                        >
                          <span>Review</span>
                          <ExternalLink className="w-3 h-3" />
                        </Link>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Right Side: Code Editor & Execution Results */}
        <div className="lg:col-span-7 space-y-5">
          <CodeEditor
            questionId={question.id}
            starterCodeMap={question.starter_code}
            onRunCode={handleRunCode}
            onSubmitCode={handleSubmitCode}
            isRunning={isRunning}
            isSubmitting={isSubmitting}
          />

          <div ref={resultsRef}>
            {(runResult || submission) && (
              <SubmissionResult
                runResult={runResult}
                submission={submission}
              />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
