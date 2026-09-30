"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  CodeRunResponse,
  CodingSubmissionDetail,
  SubmissionResultSummary,
  TestCaseRunResult,
} from "@/types/coding";
import {
  CheckCircle2,
  XCircle,
  Clock,
  AlertTriangle,
  Zap,
  Cpu,
  Layers,
  ChevronDown,
  ChevronUp,
  FileText,
  Lock,
  ExternalLink,
} from "lucide-react";

interface SubmissionResultProps {
  runResult?: CodeRunResponse | null;
  submission?: CodingSubmissionDetail | null;
  isEvaluating?: boolean;
  onClear?: () => void;
}

export default function SubmissionResult({
  runResult,
  submission,
  isEvaluating = false,
  onClear,
}: SubmissionResultProps) {
  const [selectedCaseIdx, setSelectedCaseIdx] = useState<number>(0);

  if (isEvaluating) {
    return (
      <div className="glass-card p-6 border border-slate-800 text-center space-y-3">
        <div className="w-8 h-8 border-2 border-sky-400 border-t-transparent rounded-full animate-spin mx-auto" />
        <h4 className="text-sm font-semibold text-white">Running Sandbox Evaluation...</h4>
        <p className="text-xs text-slate-400">
          Executing your solution against test cases in an isolated sandbox.
        </p>
      </div>
    );
  }

  // Handle empty state
  if (!runResult && !submission) {
    return (
      <div className="glass-card p-6 border border-slate-800 text-center text-xs text-slate-500">
        Run your code to test against sample cases, or submit when you are ready for grading.
      </div>
    );
  }

  // Extract normalized fields whether from runResult or submission
  const isSubmission = !!submission;
  const verdict = submission
    ? submission.result?.verdict || (submission.status === "failed" ? "Failed" : "Evaluating")
    : runResult?.verdict || "Executed";

  const score = submission?.result ? submission.result.score : null;
  const passedCases = submission?.result
    ? submission.result.passed_test_cases
    : runResult?.passed_test_cases || 0;
  const totalCases = submission?.result
    ? submission.result.total_test_cases
    : runResult?.total_test_cases || 0;

  const executionTime = submission?.result?.execution_time_ms ?? runResult?.execution_time_ms;
  const memoryKb = submission?.result?.memory_kb;
  const errorMessage = submission?.result?.error_message || runResult?.error_message;

  const testCases: TestCaseRunResult[] = (submission?.result?.test_case_results as TestCaseRunResult[]) ||
    runResult?.test_cases ||
    [];

  const isAccepted = verdict.toLowerCase().includes("accepted") || (passedCases === totalCases && totalCases > 0);
  const isTimeLimit = verdict.toLowerCase().includes("time");
  const isError =
    verdict.toLowerCase().includes("error") ||
    verdict.toLowerCase().includes("failed") ||
    !!errorMessage;

  const getVerdictBadge = () => {
    if (isAccepted) {
      return (
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 font-bold text-sm">
          <CheckCircle2 className="w-5 h-5 text-emerald-400" />
          <span>Accepted</span>
        </div>
      );
    }
    if (isTimeLimit) {
      return (
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-400 font-bold text-sm">
          <Clock className="w-5 h-5 text-amber-400" />
          <span>Time Limit Exceeded</span>
        </div>
      );
    }
    if (isError) {
      return (
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-400 font-bold text-sm">
          <AlertTriangle className="w-5 h-5 text-rose-400" />
          <span>{verdict || "Runtime Error"}</span>
        </div>
      );
    }
    return (
      <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-rose-500/10 border border-rose-500/30 text-rose-400 font-bold text-sm">
        <XCircle className="w-5 h-5 text-rose-400" />
        <span>{verdict || "Wrong Answer"}</span>
      </div>
    );
  };

  const activeTestCase = testCases[selectedCaseIdx];

  return (
    <div className="glass-card border border-slate-800 rounded-xl overflow-hidden space-y-4 p-5">
      {/* Top Banner */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div className="flex items-center gap-3">
          {getVerdictBadge()}
          <span className="text-xs text-slate-400">
            {isSubmission ? "Full Submission Result" : "Sample Run Result"}
          </span>
        </div>

        {/* Action Link for full submission */}
        {isSubmission && submission && (
          <Link
            href={`/coding/results?submissionId=${submission.id}`}
            className="inline-flex items-center gap-1 text-xs text-sky-400 hover:text-sky-300 font-medium"
          >
            <span>View Full Diagnostic</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </Link>
        )}
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {/* Score */}
        {score !== null && (
          <div className="bg-slate-900/80 border border-slate-800 rounded-lg p-3">
            <div className="text-[11px] font-medium text-slate-400 uppercase tracking-wider">Score</div>
            <div className="text-xl font-bold text-white mt-1">
              <span className={score === 100 ? "text-emerald-400" : score > 0 ? "text-sky-400" : "text-slate-400"}>
                {score.toFixed(1)}
              </span>
              <span className="text-xs text-slate-500 font-normal"> / 100</span>
            </div>
          </div>
        )}

        {/* Tests Passed */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-lg p-3">
          <div className="text-[11px] font-medium text-slate-400 uppercase tracking-wider">Test Cases</div>
          <div className="text-xl font-bold text-white mt-1">
            <span className={passedCases === totalCases && totalCases > 0 ? "text-emerald-400" : "text-amber-400"}>
              {passedCases}
            </span>
            <span className="text-xs text-slate-500 font-normal"> / {totalCases} Passed</span>
          </div>
        </div>

        {/* Runtime */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-lg p-3">
          <div className="text-[11px] font-medium text-slate-400 uppercase tracking-wider flex items-center gap-1">
            <Zap className="w-3 h-3 text-sky-400" />
            Runtime
          </div>
          <div className="text-xl font-bold text-white mt-1">
            {executionTime !== undefined && executionTime !== null ? `${Math.round(executionTime)} ms` : "—"}
          </div>
        </div>

        {/* Memory */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-lg p-3">
          <div className="text-[11px] font-medium text-slate-400 uppercase tracking-wider flex items-center gap-1">
            <Cpu className="w-3 h-3 text-indigo-400" />
            Memory
          </div>
          <div className="text-xl font-bold text-white mt-1">
            {memoryKb ? `${Math.round(memoryKb)} KB` : "—"}
          </div>
        </div>
      </div>

      {/* Error Callout */}
      {errorMessage && (
        <div className="p-3.5 bg-rose-950/40 border border-rose-900/60 rounded-lg space-y-1">
          <div className="text-xs font-semibold text-rose-300 flex items-center gap-1.5">
            <AlertTriangle className="w-3.5 h-3.5" />
            Runtime / Compilation Message
          </div>
          <pre className="text-xs font-mono text-rose-200 overflow-x-auto whitespace-pre-wrap">
            {errorMessage}
          </pre>
        </div>
      )}

      {/* Test Cases Tab List */}
      {testCases.length > 0 && (
        <div className="space-y-3 pt-2">
          <div className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
            Test Case Details
          </div>

          {/* Test Case Selection Tabs */}
          <div className="flex flex-wrap gap-2">
            {testCases.map((tc, idx) => {
              const isPassed = tc.passed;
              const isSelected = selectedCaseIdx === idx;
              return (
                <button
                  key={tc.test_case_id || idx}
                  onClick={() => setSelectedCaseIdx(idx)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center gap-1.5 transition border ${
                    isSelected
                      ? "bg-slate-800 text-white border-sky-500 shadow-sm"
                      : "bg-slate-900/80 text-slate-400 border-slate-800 hover:text-slate-200"
                  }`}
                >
                  {isPassed ? (
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                  ) : (
                    <XCircle className="w-3.5 h-3.5 text-rose-400" />
                  )}
                  <span>Case {idx + 1}</span>
                  {!tc.is_sample && (
                    <span title="Hidden Test Case">
                      <Lock className="w-2.5 h-2.5 text-slate-500" />
                    </span>
                  )}
                </button>
              );
            })}
          </div>

          {/* Active Test Case Diagnostics */}
          {activeTestCase && (
            <div className="p-4 bg-slate-950 border border-slate-800 rounded-lg space-y-3 text-xs font-mono">
              <div className="flex items-center justify-between text-slate-400 pb-2 border-b border-slate-900">
                <span className="font-semibold text-white">
                  Case #{selectedCaseIdx + 1} {activeTestCase.is_sample ? "(Sample)" : "(Hidden Test Case)"}
                </span>
                <span className={activeTestCase.passed ? "text-emerald-400" : "text-rose-400"}>
                  {activeTestCase.verdict || (activeTestCase.passed ? "Passed" : "Failed")}
                </span>
              </div>

              {/* Sample Test Case I/O */}
              {activeTestCase.is_sample ? (
                <div className="space-y-2">
                  <div>
                    <span className="text-slate-500 block mb-1">Input:</span>
                    <pre className="p-2 bg-slate-900 rounded text-slate-200 overflow-x-auto whitespace-pre-wrap">
                      {activeTestCase.input_data || "—"}
                    </pre>
                  </div>

                  <div>
                    <span className="text-slate-500 block mb-1">Expected Output:</span>
                    <pre className="p-2 bg-slate-900 rounded text-emerald-400 overflow-x-auto whitespace-pre-wrap">
                      {activeTestCase.expected_output || "—"}
                    </pre>
                  </div>

                  <div>
                    <span className="text-slate-500 block mb-1">Your Output:</span>
                    <pre className={`p-2 bg-slate-900 rounded overflow-x-auto whitespace-pre-wrap ${
                      activeTestCase.passed ? "text-emerald-400" : "text-rose-400"
                    }`}>
                      {activeTestCase.actual_output || (activeTestCase.error_message ? `Error: ${activeTestCase.error_message}` : "—")}
                    </pre>
                  </div>
                </div>
              ) : (
                /* Hidden Test Case Protected view */
                <div className="p-4 rounded bg-slate-900/60 border border-slate-800/80 space-y-2 text-center text-slate-400">
                  <div className="flex items-center justify-center gap-2 text-amber-400 font-sans font-medium text-xs">
                    <Lock className="w-4 h-4" />
                    <span>Protected Assessment Test Case</span>
                  </div>
                  <p className="text-[11px] text-slate-500 font-sans max-w-sm mx-auto">
                    Input and expected output for hidden evaluation test cases are sealed to maintain assessment integrity.
                  </p>
                  <div className="pt-2 text-xs">
                    Status:{" "}
                    <strong className={activeTestCase.passed ? "text-emerald-400" : "text-rose-400"}>
                      {activeTestCase.passed ? "Passed ✓" : "Failed ✗"}
                    </strong>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
