"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  CodeRunResponse,
  CodingSubmissionDetail,
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
      <div className="bg-white rounded-2xl p-6 shadow-card border border-[#E5E9EF] text-center space-y-3">
        <div className="w-8 h-8 border-2 border-[#123E63] border-t-transparent rounded-full animate-spin mx-auto" />
        <h4 className="text-sm font-bold text-[#202B38]">Running Code Execution...</h4>
        <p className="text-xs text-[#8993A0]">
          Executing your solution against test cases in the sandbox environment.
        </p>
      </div>
    );
  }

  if (!runResult && !submission) {
    return (
      <div className="bg-white rounded-2xl p-6 shadow-card border border-[#E5E9EF] text-center text-xs text-[#8993A0]">
        Run your code to test against sample test cases, or submit when you are ready for evaluation.
      </div>
    );
  }

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
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 font-bold text-xs">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          <span>{isSubmission ? "Accepted" : "Sample Tests Passed"}</span>
        </div>
      );
    }
    if (isTimeLimit) {
      return (
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#FFF6E8] text-[#F5A623] border border-[#F5A623]/30 font-bold text-xs">
          <Clock className="w-4 h-4 text-[#F5A623]" />
          <span>Time Limit Exceeded</span>
        </div>
      );
    }
    if (isError) {
      return (
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-red-50 text-red-600 border border-red-200 font-bold text-xs">
          <AlertTriangle className="w-4 h-4 text-red-500" />
          <span>{verdict || "Runtime Error"}</span>
        </div>
      );
    }
    return (
      <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-red-50 text-red-600 border border-red-200 font-bold text-xs">
        <XCircle className="w-4 h-4 text-red-500" />
        <span>{verdict || "Wrong Answer"}</span>
      </div>
    );
  };

  const activeTestCase = testCases[selectedCaseIdx];

  return (
    <div className="bg-white rounded-2xl shadow-card border border-[#E5E9EF] overflow-hidden space-y-4 p-5 sm:p-6">
      {/* Top Banner */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-3 border-b border-[#E5E9EF]">
        <div className="flex items-center gap-3">
          {getVerdictBadge()}
          <span className="text-xs text-[#8993A0]">
            {isSubmission ? "Full Submission Assessment" : "Interactive Sample Run"}
          </span>
        </div>

        {isSubmission && submission && (
          <Link
            href={`/coding/results?submissionId=${submission.id}`}
            className="inline-flex items-center gap-1 text-xs text-[#123E63] hover:underline font-bold"
          >
            <span>View Diagnostics</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </Link>
        )}
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {score !== null && (
          <div className="bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl p-3">
            <span className="text-[10px] font-bold text-[#8993A0] uppercase tracking-wider block">Score</span>
            <div className="text-lg font-bold text-[#202B38] mt-0.5">
              <span className={score === 100 ? "text-emerald-600" : score > 0 ? "text-[#123E63]" : "text-[#202B38]"}>
                {score.toFixed(1)}
              </span>
              <span className="text-xs text-[#8993A0] font-normal"> / 100</span>
            </div>
          </div>
        )}

        <div className="bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl p-3">
          <span className="text-[10px] font-bold text-[#8993A0] uppercase tracking-wider block">Test Cases</span>
          <div className="text-lg font-bold text-[#202B38] mt-0.5">
            <span className={passedCases === totalCases && totalCases > 0 ? "text-emerald-600" : "text-[#F5A623]"}>
              {passedCases}
            </span>
            <span className="text-xs text-[#8993A0] font-normal"> / {totalCases} Passed</span>
          </div>
        </div>

        <div className="bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl p-3">
          <span className="text-[10px] font-bold text-[#8993A0] uppercase tracking-wider flex items-center gap-1">
            <Zap className="w-3 h-3 text-[#123E63]" />
            Runtime
          </span>
          <div className="text-lg font-bold text-[#202B38] mt-0.5">
            {executionTime !== undefined && executionTime !== null ? `${Math.round(executionTime)} ms` : "—"}
          </div>
        </div>

        <div className="bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl p-3">
          <span className="text-[10px] font-bold text-[#8993A0] uppercase tracking-wider flex items-center gap-1">
            <Cpu className="w-3 h-3 text-[#F5A623]" />
            Memory
          </span>
          <div className="text-lg font-bold text-[#202B38] mt-0.5">
            {memoryKb ? `${Math.round(memoryKb)} KB` : "—"}
          </div>
        </div>
      </div>

      {/* Error Callout */}
      {errorMessage && (
        <div className="p-3.5 bg-red-50 border border-red-200 rounded-xl space-y-1">
          <div className="text-xs font-bold text-red-700 flex items-center gap-1.5">
            <AlertTriangle className="w-3.5 h-3.5 text-red-600" />
            Execution Error Message
          </div>
          <pre className="text-xs font-mono text-red-600 overflow-x-auto whitespace-pre-wrap">
            {errorMessage}
          </pre>
        </div>
      )}

      {/* Test Cases Tab List */}
      {testCases.length > 0 && (
        <div className="space-y-3 pt-1">
          <div className="text-xs font-bold text-[#8993A0] uppercase tracking-wider">
            Test Case Results
          </div>

          <div className="flex flex-wrap gap-2">
            {testCases.map((tc, idx) => {
              const isPassed = tc.passed;
              const isSelected = selectedCaseIdx === idx;
              return (
                <button
                  key={tc.test_case_id || idx}
                  onClick={() => setSelectedCaseIdx(idx)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1.5 transition border ${
                    isSelected
                      ? "bg-[#123E63] text-white border-[#123E63] shadow-xs"
                      : "bg-[#F8F9FA] text-[#8993A0] border-[#E5E9EF] hover:text-[#202B38]"
                  }`}
                >
                  {isPassed ? (
                    <CheckCircle2 className={`w-3.5 h-3.5 ${isSelected ? "text-emerald-300" : "text-emerald-600"}`} />
                  ) : (
                    <XCircle className={`w-3.5 h-3.5 ${isSelected ? "text-red-300" : "text-red-500"}`} />
                  )}
                  <span>Case {idx + 1}</span>
                  {!tc.is_sample && (
                    <Lock className="w-2.5 h-2.5 opacity-60" />
                  )}
                </button>
              );
            })}
          </div>

          {activeTestCase && (
            <div className="p-4 bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl space-y-3 text-xs font-mono">
              <div className="flex items-center justify-between text-[#8993A0] pb-2 border-b border-[#E5E9EF]">
                <span className="font-bold text-[#202B38] font-sans">
                  Case #{selectedCaseIdx + 1} {activeTestCase.is_sample ? "(Sample Case)" : "(Hidden Test Case)"}
                </span>
                <span className={activeTestCase.passed ? "text-emerald-700 font-bold" : "text-red-600 font-bold"}>
                  {activeTestCase.verdict || (activeTestCase.passed ? "Passed" : "Failed")}
                </span>
              </div>

              {activeTestCase.is_sample ? (
                <div className="space-y-2">
                  <div>
                    <span className="text-[#8993A0] block mb-1 font-sans text-[11px]">Input:</span>
                    <pre className="p-2 bg-white rounded-lg border border-[#E5E9EF] text-[#202B38] overflow-x-auto whitespace-pre-wrap">
                      {activeTestCase.input_data || "—"}
                    </pre>
                  </div>

                  <div>
                    <span className="text-[#8993A0] block mb-1 font-sans text-[11px]">Expected:</span>
                    <pre className="p-2 bg-white rounded-lg border border-emerald-200 text-emerald-700 overflow-x-auto whitespace-pre-wrap font-bold">
                      {activeTestCase.expected_output || "—"}
                    </pre>
                  </div>

                  <div>
                    <span className="text-[#8993A0] block mb-1 font-sans text-[11px]">Your Output:</span>
                    <pre className={`p-2 bg-white rounded-lg border overflow-x-auto whitespace-pre-wrap ${
                      activeTestCase.passed ? "border-emerald-200 text-emerald-700" : "border-red-200 text-red-600"
                    }`}>
                      {activeTestCase.actual_output || (activeTestCase.error_message ? `Error: ${activeTestCase.error_message}` : "—")}
                    </pre>
                  </div>
                </div>
              ) : (
                <div className="p-4 rounded-xl bg-white border border-[#E5E9EF] space-y-2 text-center text-[#8993A0]">
                  <div className="flex items-center justify-center gap-1.5 text-[#F5A623] font-sans font-bold text-xs">
                    <Lock className="w-4 h-4" />
                    <span>Protected Assessment Test Case</span>
                  </div>
                  <p className="text-[11px] font-sans max-w-sm mx-auto">
                    Hidden assessment test cases verify edge conditions and algorithmic scalability.
                  </p>
                  <div className="pt-1 text-xs">
                    Result:{" "}
                    <strong className={activeTestCase.passed ? "text-emerald-700" : "text-red-600"}>
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
