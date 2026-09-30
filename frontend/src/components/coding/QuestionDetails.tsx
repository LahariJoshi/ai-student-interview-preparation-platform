"use client";

import React, { useState } from "react";
import { CodingQuestionDetail, Difficulty } from "@/types/coding";
import {
  Layers,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  ChevronDown,
  ChevronUp,
  FileCode,
  Copy,
  Check,
} from "lucide-react";

interface QuestionDetailsProps {
  question: CodingQuestionDetail;
}

export default function QuestionDetails({ question }: QuestionDetailsProps) {
  const [activeTab, setActiveTab] = useState<"description" | "hints" | "samples">("description");
  const [revealedHints, setRevealedHints] = useState<Record<number, boolean>>({});
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const toggleHint = (index: number) => {
    setRevealedHints((prev) => ({
      ...prev,
      [index]: !prev[index],
    }));
  };

  const copyToClipboard = (text: string, index: number) => {
    navigator.clipboard.writeText(text);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  const getDifficultyBadge = (difficulty: Difficulty) => {
    switch (difficulty) {
      case "Easy":
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            Easy
          </span>
        );
      case "Medium":
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20">
            Medium
          </span>
        );
      case "Hard":
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/20">
            Hard
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-700 text-slate-300">
            {difficulty}
          </span>
        );
    }
  };

  return (
    <div className="glass-card flex flex-col h-full overflow-hidden">
      {/* Question Header */}
      <div className="p-6 border-b border-slate-800 space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            {getDifficultyBadge(question.difficulty)}
            <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-slate-800 text-slate-300 border border-slate-700">
              <Layers className="w-3 h-3 text-sky-400" />
              {question.topic}
            </span>
          </div>

          {question.is_solved && (
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-emerald-950/60 text-emerald-400 border border-emerald-800">
              <CheckCircle2 className="w-3.5 h-3.5" />
              Solved
            </div>
          )}
        </div>

        <h1 className="text-xl md:text-2xl font-bold text-white tracking-tight">
          {question.title}
        </h1>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-1 px-6 border-b border-slate-800 bg-slate-900/40 text-xs font-medium">
        <button
          onClick={() => setActiveTab("description")}
          className={`py-3 px-3 border-b-2 transition ${
            activeTab === "description"
              ? "border-sky-500 text-sky-400 font-semibold"
              : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          Description
        </button>

        <button
          onClick={() => setActiveTab("samples")}
          className={`py-3 px-3 border-b-2 transition ${
            activeTab === "samples"
              ? "border-sky-500 text-sky-400 font-semibold"
              : "border-transparent text-slate-400 hover:text-slate-200"
          }`}
        >
          Sample Test Cases ({question.sample_test_cases.length})
        </button>

        {question.hints && question.hints.length > 0 && (
          <button
            onClick={() => setActiveTab("hints")}
            className={`py-3 px-3 border-b-2 transition ${
              activeTab === "hints"
                ? "border-sky-500 text-sky-400 font-semibold"
                : "border-transparent text-slate-400 hover:text-slate-200"
            }`}
          >
            Hints ({question.hints.length})
          </button>
        )}
      </div>

      {/* Scrollable Content Body */}
      <div className="flex-1 overflow-y-auto p-6 space-y-6 text-slate-300 text-sm leading-relaxed">
        {activeTab === "description" && (
          <div className="space-y-6">
            {/* Main Description */}
            <div className="whitespace-pre-line text-slate-200">
              {question.description}
            </div>

            {/* Constraints */}
            {question.constraints && (
              <div className="space-y-2 p-4 rounded-lg bg-slate-900/80 border border-slate-800">
                <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                  <AlertCircle className="w-3.5 h-3.5 text-amber-400" />
                  Constraints & Requirements
                </h3>
                <div className="text-xs text-slate-300 font-mono whitespace-pre-line pl-2">
                  {question.constraints}
                </div>
              </div>
            )}

            {/* Sample Cases Preview */}
            {question.sample_test_cases.length > 0 && (
              <div className="space-y-4 pt-2">
                <h3 className="text-sm font-semibold text-white">Examples</h3>
                <div className="space-y-3">
                  {question.sample_test_cases.map((sample, idx) => (
                    <div
                      key={sample.id || idx}
                      className="p-4 rounded-lg bg-slate-900/60 border border-slate-800 space-y-2"
                    >
                      <div className="text-xs font-semibold text-sky-400">
                        Example {idx + 1}
                      </div>

                      <div className="space-y-1.5 text-xs font-mono">
                        <div className="flex items-start gap-2">
                          <span className="text-slate-500 select-none min-w-[70px]">Input:</span>
                          <span className="bg-slate-950 px-2 py-0.5 rounded text-slate-200 border border-slate-800/80 break-all">
                            {sample.input_data}
                          </span>
                        </div>
                        <div className="flex items-start gap-2">
                          <span className="text-slate-500 select-none min-w-[70px]">Output:</span>
                          <span className="bg-slate-950 px-2 py-0.5 rounded text-emerald-400 border border-slate-800/80 break-all">
                            {sample.expected_output}
                          </span>
                        </div>
                      </div>

                      {sample.explanation && (
                        <div className="text-xs text-slate-400 pt-1 border-t border-slate-800/60">
                          <span className="font-semibold text-slate-300">Explanation: </span>
                          {sample.explanation}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === "samples" && (
          <div className="space-y-4">
            <p className="text-xs text-slate-400">
              Sample test cases are run when you click &quot;Run Code&quot;. Full submission evaluates all sample and hidden test cases.
            </p>

            <div className="space-y-4">
              {question.sample_test_cases.map((sample, idx) => (
                <div
                  key={sample.id || idx}
                  className="p-4 rounded-lg bg-slate-900 border border-slate-800 space-y-3"
                >
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-white">Sample Case #{idx + 1}</span>
                    <button
                      onClick={() => copyToClipboard(sample.input_data, idx)}
                      className="inline-flex items-center gap-1 text-[11px] text-slate-400 hover:text-white transition"
                    >
                      {copiedIndex === idx ? (
                        <>
                          <Check className="w-3.5 h-3.5 text-emerald-400" />
                          <span className="text-emerald-400">Copied</span>
                        </>
                      ) : (
                        <>
                          <Copy className="w-3.5 h-3.5" />
                          <span>Copy Input</span>
                        </>
                      )}
                    </button>
                  </div>

                  <div className="space-y-2 text-xs font-mono">
                    <div>
                      <div className="text-slate-400 mb-1">Input:</div>
                      <pre className="p-2.5 rounded bg-slate-950 text-slate-200 border border-slate-800 overflow-x-auto whitespace-pre-wrap">
                        {sample.input_data}
                      </pre>
                    </div>

                    <div>
                      <div className="text-slate-400 mb-1">Expected Output:</div>
                      <pre className="p-2.5 rounded bg-slate-950 text-emerald-400 border border-slate-800 overflow-x-auto whitespace-pre-wrap">
                        {sample.expected_output}
                      </pre>
                    </div>
                  </div>

                  {sample.explanation && (
                    <div className="text-xs text-slate-400 bg-slate-950/40 p-2.5 rounded border border-slate-800/40">
                      <strong className="text-slate-300">Explanation: </strong>
                      {sample.explanation}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === "hints" && question.hints && (
          <div className="space-y-3">
            <p className="text-xs text-slate-400">
              Need a nudge? Expand hints one at a time to guide your problem-solving.
            </p>

            {question.hints.map((hint, idx) => {
              const isRevealed = revealedHints[idx];
              return (
                <div
                  key={idx}
                  className="rounded-lg bg-slate-900 border border-slate-800 overflow-hidden"
                >
                  <button
                    onClick={() => toggleHint(idx)}
                    className="w-full px-4 py-3 text-left flex items-center justify-between text-xs font-medium text-slate-200 hover:bg-slate-800/60 transition"
                  >
                    <span className="flex items-center gap-2">
                      <HelpCircle className="w-4 h-4 text-sky-400" />
                      Hint {idx + 1}
                    </span>
                    {isRevealed ? (
                      <ChevronUp className="w-4 h-4 text-slate-400" />
                    ) : (
                      <ChevronDown className="w-4 h-4 text-slate-400" />
                    )}
                  </button>

                  {isRevealed && (
                    <div className="px-4 py-3 bg-slate-950/60 border-t border-slate-800 text-xs text-slate-300 whitespace-pre-line leading-relaxed">
                      {hint}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
