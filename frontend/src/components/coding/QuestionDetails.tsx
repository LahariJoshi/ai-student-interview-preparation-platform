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
    <div className="bg-white rounded-2xl shadow-card border border-[#E5E9EF] flex flex-col h-full overflow-hidden">
      {/* Header */}
      <div className="p-5 border-b border-[#E5E9EF] space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            {getDifficultyBadge(question.difficulty)}
            <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-[11px] font-semibold bg-[#F1F3F6] text-[#123E63] border border-[#E5E9EF]">
              <Layers className="w-3 h-3 text-[#F5A623]" />
              {question.topic}
            </span>
          </div>

          {question.is_solved && (
            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">
              <CheckCircle2 className="w-3.5 h-3.5" />
              <span>Solved</span>
            </div>
          )}
        </div>

        <h1 className="text-xl font-bold text-[#202B38] tracking-tight">
          {question.title}
        </h1>
      </div>

      {/* Tabs */}
      <div className="flex items-center gap-1 px-5 border-b border-[#E5E9EF] bg-[#F8F9FA] text-xs font-bold">
        <button
          onClick={() => setActiveTab("description")}
          className={`py-2.5 px-3 border-b-2 transition ${
            activeTab === "description"
              ? "border-[#123E63] text-[#123E63]"
              : "border-transparent text-[#8993A0] hover:text-[#202B38]"
          }`}
        >
          Description
        </button>

        <button
          onClick={() => setActiveTab("samples")}
          className={`py-2.5 px-3 border-b-2 transition ${
            activeTab === "samples"
              ? "border-[#123E63] text-[#123E63]"
              : "border-transparent text-[#8993A0] hover:text-[#202B38]"
          }`}
        >
          Sample Cases ({question.sample_test_cases?.length || 0})
        </button>

        {question.hints && question.hints.length > 0 && (
          <button
            onClick={() => setActiveTab("hints")}
            className={`py-2.5 px-3 border-b-2 transition ${
              activeTab === "hints"
                ? "border-[#123E63] text-[#123E63]"
                : "border-transparent text-[#8993A0] hover:text-[#202B38]"
            }`}
          >
            Hints ({question.hints.length})
          </button>
        )}
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-5 space-y-5 text-[#202B38] text-xs sm:text-sm leading-relaxed max-h-[600px]">
        {activeTab === "description" && (
          <div className="space-y-5">
            <div className="whitespace-pre-line text-[#202B38] leading-relaxed">
              {question.description}
            </div>

            {question.constraints && (
              <div className="space-y-1.5 p-3.5 rounded-xl bg-[#F8F9FA] border border-[#E5E9EF]">
                <h3 className="text-[11px] font-bold text-[#123E63] uppercase tracking-wider flex items-center gap-1.5">
                  <AlertCircle className="w-3.5 h-3.5 text-[#F5A623]" />
                  Constraints & Requirements
                </h3>
                <div className="text-xs font-mono text-[#202B38] whitespace-pre-line pl-1">
                  {question.constraints}
                </div>
              </div>
            )}

            {question.sample_test_cases && question.sample_test_cases.length > 0 && (
              <div className="space-y-3 pt-2">
                <h3 className="text-xs font-bold text-[#8993A0] uppercase tracking-wider">
                  Examples
                </h3>
                {question.sample_test_cases.map((sample, idx) => (
                  <div
                    key={sample.id || idx}
                    className="p-3.5 rounded-xl bg-[#F8F9FA] border border-[#E5E9EF] space-y-2"
                  >
                    <span className="text-[11px] font-bold text-[#123E63]">
                      Example {idx + 1}
                    </span>

                    <div className="space-y-1 text-xs font-mono">
                      <div className="flex items-start gap-2">
                        <span className="text-[#8993A0] select-none min-w-[60px]">Input:</span>
                        <span className="bg-white px-2 py-0.5 rounded border border-[#E5E9EF] text-[#202B38] break-all">
                          {sample.input_data}
                        </span>
                      </div>
                      <div className="flex items-start gap-2">
                        <span className="text-[#8993A0] select-none min-w-[60px]">Output:</span>
                        <span className="bg-white px-2 py-0.5 rounded border border-emerald-200 text-emerald-700 break-all font-bold">
                          {sample.expected_output}
                        </span>
                      </div>
                    </div>

                    {sample.explanation && (
                      <p className="text-[11px] text-[#8993A0] pt-1 border-t border-[#E5E9EF]">
                        <strong className="text-[#202B38]">Explanation:</strong> {sample.explanation}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === "samples" && (
          <div className="space-y-3">
            {question.sample_test_cases.map((sample, idx) => (
              <div
                key={sample.id || idx}
                className="p-3.5 rounded-xl bg-[#F8F9FA] border border-[#E5E9EF] space-y-2 text-xs font-mono"
              >
                <div className="flex items-center justify-between text-[11px] font-sans font-bold">
                  <span>Sample Case #{idx + 1}</span>
                  <button
                    onClick={() => copyToClipboard(sample.input_data, idx)}
                    className="text-[#123E63] hover:underline flex items-center gap-1"
                  >
                    {copiedIndex === idx ? (
                      <>
                        <Check className="w-3 h-3 text-emerald-600" />
                        <span>Copied</span>
                      </>
                    ) : (
                      <>
                        <Copy className="w-3 h-3" />
                        <span>Copy Input</span>
                      </>
                    )}
                  </button>
                </div>
                <div>
                  <span className="text-[#8993A0] block text-[10px] uppercase font-sans">Input:</span>
                  <div className="bg-white p-2 rounded-lg border border-[#E5E9EF] mt-1">{sample.input_data}</div>
                </div>
                <div>
                  <span className="text-[#8993A0] block text-[10px] uppercase font-sans">Expected:</span>
                  <div className="bg-white p-2 rounded-lg border border-[#E5E9EF] text-emerald-700 font-bold mt-1">
                    {sample.expected_output}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === "hints" && (
          <div className="space-y-2.5">
            {question.hints?.map((hint, idx) => {
              const isRevealed = revealedHints[idx];
              return (
                <div key={idx} className="p-3.5 rounded-xl border border-[#E5E9EF] bg-[#F8F9FA]">
                  <button
                    onClick={() => toggleHint(idx)}
                    className="w-full flex items-center justify-between text-xs font-bold text-[#123E63]"
                  >
                    <span>Hint {idx + 1}</span>
                    {isRevealed ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                  </button>
                  {isRevealed && (
                    <p className="text-xs text-[#202B38] mt-2 pt-2 border-t border-[#E5E9EF] leading-relaxed">
                      {hint}
                    </p>
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
