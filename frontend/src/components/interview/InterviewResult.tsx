"use client";

import React, { useState } from "react";
import Link from "next/link";
import {
  Trophy,
  Code2,
  Mic,
  Award,
  Clock,
  CheckCircle2,
  AlertTriangle,
  Lightbulb,
  ChevronDown,
  ChevronUp,
  RotateCcw,
  Sparkles,
  ArrowRight,
  Briefcase,
  Flame,
  FileText,
} from "lucide-react";
import { InterviewResultData, QuestionPerformance } from "@/types/interview";
import VoiceMetrics from "@/components/voice/VoiceMetrics";
import VoiceFeedback from "@/components/voice/VoiceFeedback";

interface InterviewResultProps {
  result: InterviewResultData;
  className?: string;
}

export default function InterviewResult({ result, className = "" }: InterviewResultProps) {
  const [expandedQuestionId, setExpandedQuestionId] = useState<string | null>(
    result.question_performance.length > 0 ? result.question_performance[0].question_id : null
  );

  const toggleQuestion = (qId: string) => {
    setExpandedQuestionId((prev) => (prev === qId ? null : qId));
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return "text-emerald-400";
    if (score >= 60) return "text-sky-400";
    if (score >= 40) return "text-amber-400";
    return "text-rose-400";
  };

  const getScoreBadge = (score: number) => {
    if (score >= 80) return "bg-emerald-500/10 text-emerald-400 border-emerald-500/30";
    if (score >= 60) return "bg-sky-500/10 text-sky-400 border-sky-500/30";
    if (score >= 40) return "bg-amber-500/10 text-amber-400 border-amber-500/30";
    return "bg-rose-500/10 text-rose-400 border-rose-500/30";
  };

  return (
    <div className={`space-y-8 ${className}`}>
      {/* Top Banner / Target Role Header */}
      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-4 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex flex-wrap items-center gap-2 mb-2">
              <span className="px-3 py-1 rounded-full text-xs font-semibold bg-sky-500/10 text-sky-400 border border-sky-500/30">
                {result.interview_type} Interview
              </span>
              <span className="px-3 py-1 rounded-full text-xs font-semibold bg-slate-800 text-slate-300 border border-slate-700">
                Level: {result.experience_level}
              </span>
              <span className="px-3 py-1 rounded-full text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/30">
                {result.difficulty}
              </span>
              <span className="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                Completed
              </span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
              Interview Evaluation Report
            </h1>
            <p className="text-sm text-slate-400 mt-1 flex items-center gap-2">
              <Briefcase className="w-4 h-4 text-slate-500" />
              <span>Target Role: <strong className="text-slate-200">{result.target_role}</strong></span>
            </p>
          </div>

          {/* Quick Metrics (Duration & Questions) */}
          <div className="flex sm:flex-col items-end gap-2 text-xs text-slate-400 bg-slate-950/60 p-3.5 rounded-2xl border border-slate-800">
            <div className="flex items-center gap-1.5 font-semibold text-slate-200">
              <Clock className="w-3.5 h-3.5 text-sky-400" />
              <span>Duration: {result.formatted_duration}</span>
            </div>
            <div className="flex items-center gap-1.5 text-slate-400">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
              <span>
                {result.answered_questions} of {result.total_questions} Questions Answered
              </span>
            </div>
          </div>
        </div>

        {/* Executive Summary */}
        <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800 text-xs sm:text-sm text-slate-300 leading-relaxed">
          {result.summary}
        </div>
      </div>

      {/* Main Score Dashboard (Backend Calculated Scores) */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* Overall Blended Score */}
        <div className="p-6 rounded-2xl bg-gradient-to-br from-slate-900 via-slate-900 to-sky-950/40 border border-slate-800 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <Trophy className="w-4 h-4 text-sky-400" /> Overall Performance
            </span>
            <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold border ${getScoreBadge(result.interview_score)}`}>
              {result.interview_score >= 75 ? "Proficient" : result.interview_score >= 55 ? "Developing" : "Needs Review"}
            </span>
          </div>
          <div className="flex items-baseline gap-2">
            <span className={`text-4xl sm:text-5xl font-extrabold ${getScoreColor(result.interview_score)}`}>
              {result.interview_score}
            </span>
            <span className="text-slate-500 font-medium text-sm">/ 100</span>
          </div>
          <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
            <div
              className="bg-gradient-to-r from-sky-500 to-indigo-500 h-2 rounded-full transition-all duration-500"
              style={{ width: `${Math.min(100, Math.max(0, result.interview_score))}%` }}
            />
          </div>
          <p className="text-[11px] text-slate-400">
            Weighted composite score calculated by backend intelligence.
          </p>
        </div>

        {/* Technical Score */}
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <Code2 className="w-4 h-4 text-indigo-400" /> Technical Score
            </span>
            <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold border ${getScoreBadge(result.technical_score)}`}>
              {result.technical_score >= 75 ? "Strong" : "Practice"}
            </span>
          </div>
          <div className="flex items-baseline gap-2">
            <span className={`text-4xl sm:text-5xl font-extrabold ${getScoreColor(result.technical_score)}`}>
              {result.technical_score}
            </span>
            <span className="text-slate-500 font-medium text-sm">/ 100</span>
          </div>
          <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
            <div
              className="bg-indigo-500 h-2 rounded-full transition-all duration-500"
              style={{ width: `${Math.min(100, Math.max(0, result.technical_score))}%` }}
            />
          </div>
          <p className="text-[11px] text-slate-400">
            Correctness, depth, architectural trade-offs, and completeness.
          </p>
        </div>

        {/* Communication Score */}
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 shadow-sm space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
              <Mic className="w-4 h-4 text-emerald-400" /> Communication Score
            </span>
            <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold border ${getScoreBadge(result.communication_score)}`}>
              {result.communication_score >= 75 ? "Clear" : "Polishing"}
            </span>
          </div>
          <div className="flex items-baseline gap-2">
            <span className={`text-4xl sm:text-5xl font-extrabold ${getScoreColor(result.communication_score)}`}>
              {result.communication_score}
            </span>
            <span className="text-slate-500 font-medium text-sm">/ 100</span>
          </div>
          <div className="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
            <div
              className="bg-emerald-500 h-2 rounded-full transition-all duration-500"
              style={{ width: `${Math.min(100, Math.max(0, result.communication_score))}%` }}
            />
          </div>
          <p className="text-[11px] text-slate-400">
            Speaking pace, cadence, verbal economy, and delivery transitions.
          </p>
        </div>
      </div>

      {/* Two Column: Key Strengths vs Improvement Suggestions */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Strengths Card */}
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-emerald-500/10 flex items-center justify-center text-emerald-400 border border-emerald-500/30">
              <CheckCircle2 className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-white">Demonstrated Strengths</h3>
              <p className="text-[11px] text-slate-400">Key competencies highlighted across your responses</p>
            </div>
          </div>

          <ul className="space-y-2.5">
            {result.strengths.map((strength, idx) => (
              <li key={idx} className="flex items-start gap-2.5 text-xs text-slate-300 leading-relaxed p-2.5 rounded-xl bg-slate-950/60 border border-slate-800">
                <span className="text-emerald-400 font-bold shrink-0 mt-0.5">✓</span>
                <span>{strength}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Improvement Areas Card */}
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-amber-500/10 flex items-center justify-center text-amber-400 border border-amber-500/30">
              <AlertTriangle className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-white">Target Areas for Improvement</h3>
              <p className="text-[11px] text-slate-400">Missing concepts or depth opportunities identified</p>
            </div>
          </div>

          <ul className="space-y-2.5">
            {result.weaknesses.map((weakness, idx) => (
              <li key={idx} className="flex items-start gap-2.5 text-xs text-slate-300 leading-relaxed p-2.5 rounded-xl bg-slate-950/60 border border-slate-800">
                <span className="text-amber-400 font-bold shrink-0 mt-0.5">•</span>
                <span>{weakness}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Actionable Recommendations */}
      {result.recommendations.length > 0 && (
        <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-sky-500/10 flex items-center justify-center text-sky-400 border border-sky-500/30">
              <Lightbulb className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-white">Actionable Preparation Roadmap</h3>
              <p className="text-[11px] text-slate-400">Tailored suggestions to prepare for upcoming real interview rounds</p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {result.recommendations.map((rec, idx) => (
              <div key={idx} className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 text-xs text-slate-300 space-y-1">
                <div className="flex items-center gap-2 text-sky-400 font-semibold text-[11px]">
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Recommendation #{idx + 1}</span>
                </div>
                <p className="leading-relaxed">{rec}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Voice Delivery & Communication Telemetry Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Mic className="w-5 h-5 text-sky-400" />
              <span>Voice Delivery & Communication Intelligence</span>
            </h2>
            <p className="text-xs text-slate-400">Speaking cadence, filler-word economy, and coaching feedback</p>
          </div>
        </div>

        {/* Voice Metrics Cards */}
        <VoiceMetrics metrics={result.voice_metrics} />

        {/* Voice Feedback Explanations */}
        {result.voice_metrics.has_voice_data && (
          <VoiceFeedback
            feedbackList={result.voice_metrics.communication_feedback}
            communicationScore={result.communication_score}
          />
        )}
      </div>

      {/* Question-Wise Performance Breakdown */}
      <div className="space-y-4">
        <div>
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <FileText className="w-5 h-5 text-sky-400" />
            <span>Question-by-Question Deep Dive</span>
          </h2>
          <p className="text-xs text-slate-400">
            Review detailed question analysis, candidate answers, and scoring breakdown
          </p>
        </div>

        <div className="space-y-3">
          {result.question_performance.map((qp) => {
            const isExpanded = expandedQuestionId === qp.question_id;

            return (
              <div
                key={qp.question_id}
                className="rounded-2xl bg-slate-900 border border-slate-800 overflow-hidden transition"
              >
                {/* Accordion Header */}
                <button
                  type="button"
                  onClick={() => toggleQuestion(qp.question_id)}
                  className="w-full p-5 flex items-center justify-between gap-4 text-left hover:bg-slate-800/40 transition cursor-pointer"
                >
                  <div className="flex items-center gap-3">
                    <span className="w-7 h-7 rounded-lg bg-slate-800 flex items-center justify-center text-xs font-bold text-slate-300">
                      #{qp.question_order}
                    </span>
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                          {qp.category}
                        </span>
                        {qp.difficulty && (
                          <span className="text-[10px] font-semibold text-slate-400">
                            • {qp.difficulty}
                          </span>
                        )}
                        {qp.topic && (
                          <span className="text-[10px] text-slate-500">
                            • {qp.topic}
                          </span>
                        )}
                      </div>
                      <h4 className="text-sm font-semibold text-white line-clamp-1">
                        {qp.question_text}
                      </h4>
                    </div>
                  </div>

                  <div className="flex items-center gap-3 shrink-0">
                    {qp.score !== null && qp.score !== undefined ? (
                      <span className={`px-3 py-1 rounded-xl text-xs font-bold border ${getScoreBadge(qp.score)}`}>
                        {qp.score} / 100
                      </span>
                    ) : (
                      <span className="px-3 py-1 rounded-xl text-xs font-medium text-slate-400 bg-slate-800">
                        Unscored
                      </span>
                    )}

                    {isExpanded ? (
                      <ChevronUp className="w-4 h-4 text-slate-400" />
                    ) : (
                      <ChevronDown className="w-4 h-4 text-slate-400" />
                    )}
                  </div>
                </button>

                {/* Expanded Question Details */}
                {isExpanded && (
                  <div className="p-5 border-t border-slate-800/80 bg-slate-950/40 space-y-4">
                    {/* Full Question Text */}
                    <div className="space-y-1">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500">
                        Question Prompt
                      </span>
                      <p className="text-sm font-medium text-white leading-relaxed">
                        {qp.question_text}
                      </p>
                    </div>

                    {/* Candidate Answer */}
                    <div className="space-y-1.5">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-sky-400 flex items-center gap-1.5">
                        <FileText className="w-3.5 h-3.5" />
                        Candidate Submitted Response
                      </span>
                      <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-300 leading-relaxed whitespace-pre-wrap">
                        {qp.candidate_answer || (
                          <span className="text-slate-500 italic">No answer was submitted for this question.</span>
                        )}
                      </div>
                    </div>

                    {/* Telemetry pill row if recorded */}
                    {(qp.speaking_rate_wpm !== null || qp.filler_word_count !== null || qp.audio_duration_seconds !== null) && (
                      <div className="flex flex-wrap items-center gap-3 text-[11px] text-slate-400">
                        {qp.speaking_rate_wpm && (
                          <span className="px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800">
                            Cadence: <strong className="text-slate-200">{qp.speaking_rate_wpm} WPM</strong>
                          </span>
                        )}
                        {qp.filler_word_count !== null && (
                          <span className="px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800">
                            Fillers: <strong className="text-slate-200">{qp.filler_word_count}</strong>
                          </span>
                        )}
                        {qp.audio_duration_seconds && (
                          <span className="px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800">
                            Duration: <strong className="text-slate-200">{Math.round(qp.audio_duration_seconds)}s</strong>
                          </span>
                        )}
                        {qp.clarity_score !== null && (
                          <span className="px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800">
                            Delivery Clarity: <strong className="text-emerald-400">{qp.clarity_score}/100</strong>
                          </span>
                        )}
                      </div>
                    )}

                    {/* Feedback & Points */}
                    {qp.feedback && (
                      <div className="space-y-1">
                        <span className="text-[10px] font-bold uppercase tracking-wider text-slate-500">
                          Evaluator Feedback
                        </span>
                        <p className="text-xs text-slate-300 leading-relaxed whitespace-pre-wrap">
                          {qp.feedback}
                        </p>
                      </div>
                    )}

                    {/* Strengths & Missing Concepts Grid */}
                    {(qp.strengths.length > 0 || qp.weaknesses.length > 0) && (
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
                        {qp.strengths.length > 0 && (
                          <div className="p-3 rounded-xl bg-emerald-500/5 border border-emerald-500/20 space-y-1.5">
                            <span className="text-[11px] font-bold text-emerald-400 flex items-center gap-1">
                              <CheckCircle2 className="w-3 h-3" /> Question Strengths
                            </span>
                            <ul className="text-xs text-slate-300 space-y-1 list-disc list-inside">
                              {qp.strengths.map((s, idx) => (
                                <li key={idx}>{s}</li>
                              ))}
                            </ul>
                          </div>
                        )}

                        {qp.weaknesses.length > 0 && (
                          <div className="p-3 rounded-xl bg-amber-500/5 border border-amber-500/20 space-y-1.5">
                            <span className="text-[11px] font-bold text-amber-400 flex items-center gap-1">
                              <AlertTriangle className="w-3 h-3" /> Areas to Elaborate
                            </span>
                            <ul className="text-xs text-slate-300 space-y-1 list-disc list-inside">
                              {qp.weaknesses.map((w, idx) => (
                                <li key={idx}>{w}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Action Footer */}
      <div className="pt-6 border-t border-slate-800 flex flex-wrap items-center justify-between gap-4">
        <Link
          href="/interview"
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white text-xs font-semibold border border-slate-700 transition"
        >
          <RotateCcw className="w-4 h-4" />
          <span>Return to Interview Hub</span>
        </Link>

        <Link
          href="/interview/setup"
          className="inline-flex items-center gap-2 px-6 py-2.5 rounded-xl bg-gradient-to-r from-sky-500 to-indigo-500 hover:from-sky-400 hover:to-indigo-400 text-slate-950 font-bold text-xs shadow-lg shadow-sky-500/20 transition"
        >
          <span>Start Another Practice Session</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </div>
    </div>
  );
}
