"use client";

import React, { useState } from "react";
import { Mic, FileText, Sparkles, AlertCircle, CheckCircle2, Info } from "lucide-react";
import AudioRecorder, { RecordedAudioData } from "@/components/voice/AudioRecorder";
import { AnswerMode } from "@/types/interview";

interface AnswerRecorderProps {
  questionText: string;
  answerMode?: AnswerMode | string;
  initialTextAnswer?: string;
  isSubmitting?: boolean;
  onSubmitAnswer: (answerText: string, audioData?: RecordedAudioData) => Promise<void>;
  className?: string;
}

export default function AnswerRecorder({
  questionText,
  answerMode = "Voice + Text",
  initialTextAnswer = "",
  isSubmitting = false,
  onSubmitAnswer,
  className = "",
}: AnswerRecorderProps) {
  const [activeTab, setActiveTab] = useState<"voice" | "text">(
    answerMode === "Text" ? "text" : "voice"
  );
  const [textAnswer, setTextAnswer] = useState<string>(initialTextAnswer);
  const [recordedAudio, setRecordedAudio] = useState<RecordedAudioData | null>(null);
  const [validationError, setValidationError] = useState<string | null>(null);

  const isVoiceAllowed = answerMode !== "Text";
  const isTextAllowed = answerMode !== "Voice";

  // Audio recording completion handler
  const handleRecordingComplete = (data: RecordedAudioData) => {
    setRecordedAudio(data);
    setValidationError(null);
  };

  // Audio deletion handler
  const handleDeleteRecording = () => {
    setRecordedAudio(null);
  };

  // Submission handler from voice recorder
  const handleSubmitVoiceAnswer = async (data: RecordedAudioData) => {
    setValidationError(null);
    try {
      // In Task 8: Audio is recorded and previewed; text placeholder or transcript passed
      const answerPayload = textAnswer.trim()
        ? textAnswer.trim()
        : `[Voice Recording: ${Math.round(data.durationSeconds)}s]`;
      await onSubmitAnswer(answerPayload, data);
    } catch (err: any) {
      setValidationError(err.message || "Failed to submit voice answer.");
    }
  };

  // Submission handler for text answer
  const handleSubmitTextAnswer = async () => {
    if (!textAnswer.trim()) {
      setValidationError("Please enter your answer text before submitting.");
      return;
    }
    setValidationError(null);
    try {
      await onSubmitAnswer(textAnswer.trim(), recordedAudio || undefined);
    } catch (err: any) {
      setValidationError(err.message || "Failed to submit answer.");
    }
  };

  return (
    <div className={`w-full rounded-2xl bg-slate-900/90 border border-slate-800 p-6 space-y-6 ${className}`}>
      {/* Question Header & Context */}
      <div className="space-y-2 border-b border-slate-800 pb-4">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold uppercase tracking-wider text-sky-400">
            Current Question
          </span>
          <span className="text-xs text-slate-400 font-medium">
            Mode: <strong className="text-slate-200">{answerMode}</strong>
          </span>
        </div>
        <p className="text-base sm:text-lg font-medium text-white leading-relaxed">
          {questionText}
        </p>
      </div>

      {/* Mode Switch Tabs (If Voice + Text is allowed) */}
      {isVoiceAllowed && isTextAllowed && (
        <div className="flex items-center gap-2 p-1 rounded-xl bg-slate-950/70 border border-slate-800 max-w-fit">
          <button
            type="button"
            onClick={() => setActiveTab("voice")}
            className={`flex items-center gap-2 px-4 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer ${
              activeTab === "voice"
                ? "bg-sky-500 text-slate-950 shadow-sm"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <Mic className="w-3.5 h-3.5" />
            <span>Voice Response</span>
            {recordedAudio && (
              <span className="w-2 h-2 rounded-full bg-emerald-400" title="Audio Recorded" />
            )}
          </button>

          <button
            type="button"
            onClick={() => setActiveTab("text")}
            className={`flex items-center gap-2 px-4 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer ${
              activeTab === "text"
                ? "bg-sky-500 text-slate-950 shadow-sm"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <FileText className="w-3.5 h-3.5" />
            <span>Written Response</span>
            {textAnswer.trim().length > 0 && (
              <span className="w-2 h-2 rounded-full bg-emerald-400" title="Text Entered" />
            )}
          </button>
        </div>
      )}

      {/* Voice Recorder View */}
      {isVoiceAllowed && activeTab === "voice" && (
        <div className="space-y-4">
          <AudioRecorder
            onRecordingComplete={handleRecordingComplete}
            onSubmitRecording={handleSubmitVoiceAnswer}
            onDeleteRecording={handleDeleteRecording}
            isSubmitting={isSubmitting}
          />

          {/* Voice Response Interview Tips */}
          <div className="flex items-start gap-2.5 p-3 rounded-xl bg-sky-500/5 border border-sky-500/20 text-xs text-sky-300">
            <Info className="w-4 h-4 text-sky-400 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold text-sky-200">Tips for Voice Answers:</p>
              <ul className="list-disc list-inside space-y-0.5 text-slate-300 mt-1">
                <li>Speak clearly at an even pace directly into your microphone.</li>
                <li>Structure technical answers: definition &rarr; architecture &rarr; practical trade-offs.</li>
                <li>You can review playback, discard, or re-record as many times as you like.</li>
              </ul>
            </div>
          </div>
        </div>
      )}

      {/* Written Text View */}
      {isTextAllowed && activeTab === "text" && (
        <div className="space-y-4">
          <div className="relative">
            <textarea
              rows={6}
              value={textAnswer}
              onChange={(e) => {
                setTextAnswer(e.target.value);
                setValidationError(null);
              }}
              placeholder="Type your structured answer here (or paste code/notes)..."
              disabled={isSubmitting}
              className="w-full rounded-xl bg-slate-950/70 border border-slate-800 p-4 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-sky-500 transition resize-y"
            />
            <div className="absolute bottom-3 right-3 text-xs text-slate-500">
              {textAnswer.trim() ? textAnswer.trim().split(/\s+/).length : 0} words
            </div>
          </div>

          <div className="flex items-center justify-end">
            <button
              type="button"
              onClick={handleSubmitTextAnswer}
              disabled={isSubmitting || !textAnswer.trim()}
              className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-sky-500 hover:bg-sky-400 disabled:bg-sky-500/40 text-slate-950 font-bold text-xs shadow-md shadow-sky-500/20 transition active:scale-95 disabled:cursor-not-allowed cursor-pointer"
            >
              {isSubmitting ? (
                <>
                  <span className="w-3.5 h-3.5 border-2 border-slate-950 border-t-transparent rounded-full animate-spin" />
                  <span>Submitting...</span>
                </>
              ) : (
                <>
                  <span>Submit Answer</span>
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* Validation or Error Message */}
      {validationError && (
        <div className="flex items-center gap-2 p-3 rounded-xl bg-rose-950/40 border border-rose-500/30 text-rose-400 text-xs">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{validationError}</span>
        </div>
      )}
    </div>
  );
}
