"use client";

import React, { useState, useEffect } from "react";
import { InterviewQuestion as IQuestion } from "@/types/interview";
import {
  Code2,
  Users,
  Briefcase,
  HelpCircle,
  Flame,
  ArrowRight,
  ArrowLeft,
  CheckCircle2,
  Loader2,
  Send,
  Flag,
  Mic,
  FileText,
  RotateCcw,
  AlertCircle,
} from "lucide-react";
import AudioRecorder, { RecordedAudioData } from "@/components/voice/AudioRecorder";

interface InterviewQuestionProps {
  question: IQuestion;
  questionNumber: number;
  totalQuestions: number;
  initialAnswer?: string;
  isSubmitting: boolean;
  isLastQuestion: boolean;
  canGoPrevious: boolean;
  canGoNext: boolean;
  answerMode?: string;
  onPreviousQuestion: () => void;
  onNextQuestion: () => void;
  onSubmitAnswer: (answerText: string, audioData?: RecordedAudioData) => Promise<void>;
  onFinishInterview: () => Promise<void>;
}

export default function InterviewQuestion({
  question,
  questionNumber,
  totalQuestions,
  initialAnswer = "",
  isSubmitting,
  isLastQuestion,
  canGoPrevious,
  canGoNext,
  answerMode = "Voice + Text",
  onPreviousQuestion,
  onNextQuestion,
  onSubmitAnswer,
  onFinishInterview,
}: InterviewQuestionProps) {
  const [answerText, setAnswerText] = useState(initialAnswer);
  const [hasSaved, setHasSaved] = useState(Boolean(initialAnswer.trim()));
  const [validationWarning, setValidationWarning] = useState<string | null>(null);
  const [inputMode, setInputMode] = useState<"text" | "voice">(
    answerMode === "Voice" ? "voice" : "text"
  );
  const [recordedAudio, setRecordedAudio] = useState<RecordedAudioData | null>(null);
  const [pipelineError, setPipelineError] = useState<string | null>(null);
  const [isProcessingVoice, setIsProcessingVoice] = useState<boolean>(false);

  // Sync answer text when question changes
  useEffect(() => {
    setAnswerText(initialAnswer || "");
    setHasSaved(Boolean(initialAnswer && initialAnswer.trim()));
    setValidationWarning(null);
    setPipelineError(null);
    setRecordedAudio(null);
    setIsProcessingVoice(false);
  }, [question.id, initialAnswer]);

  const wordCount = answerText.trim() ? answerText.trim().split(/\s+/).length : 0;
  const progressPercent = Math.round((questionNumber / totalQuestions) * 100);

  const getCategoryIcon = (category: string) => {
    const cat = category.toLowerCase();
    if (cat.includes("tech")) return Code2;
    if (cat.includes("behav")) return Users;
    if (cat.includes("hr")) return Briefcase;
    return HelpCircle;
  };

  const getCategoryBadgeColor = (category: string) => {
    const cat = category.toLowerCase();
    if (cat.includes("tech")) return "bg-sky-500/10 text-sky-400 border-sky-500/30";
    if (cat.includes("behav")) return "bg-indigo-500/10 text-indigo-400 border-indigo-500/30";
    if (cat.includes("hr")) return "bg-emerald-500/10 text-emerald-400 border-emerald-500/30";
    return "bg-amber-500/10 text-amber-400 border-amber-500/30";
  };

  const getDifficultyBadge = (difficulty?: string | null) => {
    const diff = (difficulty || "Medium").toLowerCase();
    if (diff === "easy") return "bg-emerald-500/10 text-emerald-400 border-emerald-500/30";
    if (diff === "hard") return "bg-rose-500/10 text-rose-400 border-rose-500/30";
    return "bg-amber-500/10 text-amber-400 border-amber-500/30";
  };

  const handleSaveAndAdvance = async () => {
    if (isSubmitting || isProcessingVoice) return;

    const trimmed = answerText.trim();
    if (!trimmed) {
      setValidationWarning("Please enter an answer before submitting.");
      return;
    }

    setValidationWarning(null);
    await onSubmitAnswer(trimmed);
    setHasSaved(true);
  };

  const handleVoiceSubmit = async (data: RecordedAudioData) => {
    if (isSubmitting || isProcessingVoice) return;
    setRecordedAudio(data);
    setPipelineError(null);
    setIsProcessingVoice(true);

    try {
      const fallbackText = answerText.trim()
        ? answerText.trim()
        : `[Voice Recording: ${Math.round(data.durationSeconds)}s]`;
      await onSubmitAnswer(fallbackText, data);
      setHasSaved(true);
      setRecordedAudio(null);
    } catch (err: any) {
      setPipelineError(
        err.message || "Failed to process audio recording. You can retry or record again."
      );
    } finally {
      setIsProcessingVoice(false);
    }
  };

  const CategoryIcon = getCategoryIcon(question.category);

  return (
    <div className="space-y-6">
      {/* Top Progress Bar */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-sm">
        <div className="flex items-center justify-between text-xs mb-2">
          <div className="flex items-center gap-2">
            <span className="font-bold text-white">
              Question {questionNumber} of {totalQuestions}
            </span>
            <span className="text-slate-500">•</span>
            <span className="text-slate-400">{progressPercent}% Completed</span>
          </div>

          {hasSaved && (
            <span className="inline-flex items-center gap-1 text-emerald-400 font-semibold text-xs">
              <CheckCircle2 className="w-3.5 h-3.5" /> Answer Saved
            </span>
          )}
        </div>

        <div className="w-full bg-slate-950 rounded-full h-2.5 overflow-hidden border border-slate-800">
          <div
            className="bg-gradient-to-r from-sky-500 to-indigo-500 h-2.5 rounded-full transition-all duration-300"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>

      {/* Main Question Card */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 md:p-8 shadow-sm space-y-6">
        {/* Badges */}
        <div className="flex flex-wrap items-center gap-2.5">
          <span
            className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold border ${getCategoryBadgeColor(
              question.category
            )}`}
          >
            <CategoryIcon className="w-3.5 h-3.5" />
            <span>{question.category}</span>
          </span>

          <span
            className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold border ${getDifficultyBadge(
              question.difficulty
            )}`}
          >
            <Flame className="w-3.5 h-3.5" />
            <span>{question.difficulty || "Medium"}</span>
          </span>

          {question.topic && (
            <span className="px-3 py-1 rounded-full text-xs font-medium bg-slate-800 text-slate-300 border border-slate-700">
              Topic: {question.topic}
            </span>
          )}
        </div>

        {/* Question Text */}
        <div className="pt-1">
          <h2 className="text-xl md:text-2xl font-bold text-white leading-relaxed tracking-tight">
            {question.question_text}
          </h2>
        </div>

        {/* Answer Mode Tabs (if voice is supported) */}
        {answerMode !== "Text" && (
          <div className="flex items-center gap-2 p-1 rounded-xl bg-slate-950/70 border border-slate-800 max-w-fit">
            <button
              type="button"
              onClick={() => setInputMode("text")}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer ${
                inputMode === "text"
                  ? "bg-sky-500 text-slate-950 shadow-sm"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <FileText className="w-3.5 h-3.5" />
              <span>Written Response</span>
            </button>
            <button
              type="button"
              onClick={() => setInputMode("voice")}
              className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer ${
                inputMode === "voice"
                  ? "bg-sky-500 text-slate-950 shadow-sm"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Mic className="w-3.5 h-3.5" />
              <span>Voice Recording</span>
            </button>
          </div>
        )}

        {/* Answer Input Section */}
        {inputMode === "voice" && answerMode !== "Text" ? (
          <div className="space-y-4 pt-1">
            {/* Voice Processing State Indicator */}
            {isProcessingVoice && (
              <div className="p-4 rounded-xl bg-sky-500/10 border border-sky-500/30 space-y-2 animate-pulse">
                <div className="flex items-center gap-2.5 text-sky-400 font-semibold text-xs">
                  <Loader2 className="w-4 h-4 animate-spin text-sky-400" />
                  <span>Processing Voice Pipeline...</span>
                </div>
                <p className="text-xs text-slate-300 leading-relaxed">
                  Uploading recording → Speech-to-Text transcription → Evaluating technical response → Calculating cadence & delivery feedback...
                </p>
              </div>
            )}

            {/* Processing Failure Alert & Retry */}
            {pipelineError && (
              <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 space-y-3">
                <div className="flex items-start gap-2.5 text-xs text-rose-300">
                  <AlertCircle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold text-rose-200">Voice Processing Failed:</span>
                    <p className="mt-0.5 text-rose-300/90 leading-relaxed">{pipelineError}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3 pt-1">
                  {recordedAudio && (
                    <button
                      type="button"
                      onClick={() => handleVoiceSubmit(recordedAudio)}
                      disabled={isSubmitting || isProcessingVoice}
                      className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold text-xs transition cursor-pointer disabled:opacity-50"
                    >
                      <RotateCcw className="w-3.5 h-3.5" />
                      <span>Retry Processing</span>
                    </button>
                  )}
                  <button
                    type="button"
                    onClick={() => {
                      setPipelineError(null);
                      setRecordedAudio(null);
                    }}
                    className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white font-medium text-xs transition cursor-pointer"
                  >
                    <span>Dismiss / Record Again</span>
                  </button>
                </div>
              </div>
            )}

            <AudioRecorder
              onSubmitRecording={handleVoiceSubmit}
              isSubmitting={isSubmitting || isProcessingVoice}
            />
          </div>
        ) : (
          <div className="space-y-3 pt-2">
            <div className="flex items-center justify-between">
              <label htmlFor="answer-input" className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                Your Response
              </label>
              <div className="text-xs text-slate-400">
                <span className="font-semibold text-slate-300">{wordCount}</span> words •{" "}
                <span className="font-semibold text-slate-300">{answerText.length}</span> characters
              </div>
            </div>

            <textarea
              id="answer-input"
              rows={7}
              value={answerText}
              onChange={(e) => {
                setAnswerText(e.target.value);
                setValidationWarning(null);
              }}
              placeholder="Type your structured answer here. Speak to the key technical trade-offs, architecture choices, or STAR situation details..."
              disabled={isSubmitting}
              className="w-full p-4 rounded-xl bg-slate-950 border border-slate-700 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500 transition text-sm leading-relaxed resize-y"
            />

            {validationWarning && (
              <p className="text-xs text-amber-400 flex items-center gap-1.5 font-medium">
                <span>⚠️</span> {validationWarning}
              </p>
            )}

            {/* Helper Tips */}
            <div className="p-3.5 rounded-xl bg-slate-950/60 border border-slate-800 text-xs text-slate-400 space-y-1">
              <span className="font-semibold text-slate-300">💡 Interview Tip:</span>
              {question.category.toLowerCase().includes("behav") ? (
                <p>
                  Use the <span className="text-sky-300 font-semibold">STAR method</span>: Situation, Task, Action you
                  personally took, and measurable Result.
                </p>
              ) : (
                <p>
                  Explain the <span className="text-sky-300 font-semibold">&ldquo;Why&rdquo;</span> behind your technical decisions,
                  clarify edge cases, and state performance trade-offs.
                </p>
              )}
            </div>
          </div>
        )}

        {/* Navigation & Submission Controls */}
        <div className="pt-4 border-t border-slate-800 flex flex-wrap items-center justify-between gap-3">
          {/* Previous Button */}
          <button
            type="button"
            onClick={onPreviousQuestion}
            disabled={!canGoPrevious || isSubmitting || isProcessingVoice}
            className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs font-semibold border border-slate-700 transition disabled:opacity-40 disabled:cursor-not-allowed cursor-pointer"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Previous Question</span>
          </button>

          {/* Action Buttons */}
          <div className="flex items-center gap-3">
            {canGoNext && !isLastQuestion && (
              <button
                type="button"
                onClick={onNextQuestion}
                disabled={isSubmitting || isProcessingVoice}
                className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs font-semibold border border-slate-700 transition cursor-pointer"
              >
                <span>Skip to Next</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            )}

            {isLastQuestion ? (
              <button
                type="button"
                onClick={async () => {
                  if (answerText.trim()) {
                    await handleSaveAndAdvance();
                  }
                  await onFinishInterview();
                }}
                disabled={isSubmitting || isProcessingVoice}
                className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold text-xs shadow-lg shadow-emerald-600/25 transition disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
              >
                {isSubmitting || isProcessingVoice ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Submitting & Finalizing...</span>
                  </>
                ) : (
                  <>
                    <Flag className="w-4 h-4" />
                    <span>Submit & Finish Interview</span>
                  </>
                )}
              </button>
            ) : (
              <button
                type="button"
                onClick={handleSaveAndAdvance}
                disabled={isSubmitting || isProcessingVoice}
                className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs shadow-lg shadow-sky-600/25 transition disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
              >
                {isSubmitting || isProcessingVoice ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Processing Answer...</span>
                  </>
                ) : (
                  <>
                    <Send className="w-3.5 h-3.5" />
                    <span>Submit & Next</span>
                    <ArrowRight className="w-4 h-4" />
                  </>
                )}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
