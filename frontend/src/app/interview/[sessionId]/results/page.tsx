"use client";

import React, { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import {
  Sparkles,
  Award,
  CheckCircle2,
  AlertTriangle,
  ArrowRight,
  TrendingUp,
  Volume2,
  BookOpen,
  Code2,
  FileText,
  RotateCcw,
  History,
  HelpCircle,
  Briefcase,
  Target,
} from "lucide-react";
import { InterviewResultsResponse } from "@/types/interview";

export default function InterviewResultsPage() {
  const params = useParams();
  const router = useRouter();
  const sessionId = params.sessionId as string;
  const { user, isLoading: authLoading } = useAuth();

  const [results, setResults] = useState<InterviewResultsResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push("/login");
      return;
    }

    if (sessionId) {
      fetchResults();
    }
  }, [sessionId, user, authLoading]);

  const fetchResults = async () => {
    setIsLoading(true);
    try {
      const data = await apiFetch<InterviewResultsResponse>(`/interviews/sessions/${sessionId}/results`);
      setResults(data);
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to load interview results.");
    } finally {
      setIsLoading(false);
    }
  };

  if (authLoading || isLoading) {
    return (
      <div className="py-24 text-center text-[#8993A0]">
        <div className="w-8 h-8 border-3 border-[#123E63] border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <p className="text-sm font-medium">Compiling evaluation analytics & transparent rubric...</p>
      </div>
    );
  }

  if (errorMsg || !results) {
    return (
      <div className="max-w-xl mx-auto py-16 text-center space-y-4">
        <div className="w-14 h-14 rounded-full bg-rose-50 border border-rose-200 flex items-center justify-center text-rose-500 mx-auto">
          <AlertTriangle className="w-6 h-6" />
        </div>
        <h2 className="text-xl font-bold text-[#202B38]">Results Unavailable</h2>
        <p className="text-[#8993A0] text-sm">{errorMsg || "Could not retrieve results."}</p>
        <Link
          href="/interview"
          className="inline-block px-6 py-2.5 bg-[#123E63] hover:bg-[#0D3557] text-white rounded-xl text-sm font-semibold transition shadow-sm"
        >
          Return to Studio
        </Link>
      </div>
    );
  }

  const getScoreBadgeColor = (score: number) => {
    if (score >= 80) return "text-emerald-700 border-emerald-200 bg-emerald-50";
    if (score >= 60) return "text-[#123E63] border-blue-200 bg-blue-50";
    return "text-amber-700 border-amber-200 bg-amber-50";
  };

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#123E63]/10 text-[#123E63] text-xs font-semibold mb-2">
            <Award className="w-3.5 h-3.5 text-[#F5A623]" />
            Interview Performance Report
          </div>
          <h1 className="text-2xl font-bold text-[#202B38] tracking-tight">
            Session Evaluation & Feedback
          </h1>
          <p className="text-[#8993A0] text-xs mt-1">
            Target Role: <span className="text-[#202B38] font-semibold">{results.target_role}</span> • Level: {results.experience_level} • {new Date(results.started_at).toLocaleDateString()}
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Link
            href="/interview"
            className="flex items-center gap-2 px-4 py-2 bg-[#F5A623] hover:bg-[#E09612] text-white text-xs font-semibold rounded-xl transition shadow-sm"
          >
            <RotateCcw className="w-4 h-4" />
            <span>Practice Another</span>
          </Link>
          <Link
            href="/interview/history"
            className="flex items-center gap-2 px-4 py-2 bg-white hover:bg-slate-50 border border-[#E5E9EF] text-[#202B38] text-xs font-semibold rounded-xl transition shadow-sm"
          >
            <History className="w-4 h-4 text-[#123E63]" />
            <span>History</span>
          </Link>
        </div>
      </div>

      {/* Primary Score Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Overall Score - Solid Navy Card */}
        <div className="bg-[#123E63] text-white rounded-2xl p-6 shadow-sm flex flex-col items-center justify-center text-center space-y-2">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-white/70">
            Overall Readiness Score
          </span>
          <div className="text-4xl font-extrabold text-white">
            {Math.round(results.overall_score)}<span className="text-lg font-normal text-white/70">/100</span>
          </div>
          <p className="text-xs text-white/70">Automated student practice evaluation</p>
        </div>

        {/* Technical Accuracy - White Card */}
        <div className="bg-white border border-[#E5E9EF] rounded-2xl p-6 shadow-sm flex flex-col items-center justify-center text-center space-y-2">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-[#8993A0]">
            Technical Proficiency
          </span>
          <div className="text-3xl font-extrabold text-[#123E63]">
            {Math.round(results.technical_score)}<span className="text-lg font-normal text-[#8993A0]">/100</span>
          </div>
          <p className="text-xs text-[#8993A0]">Concept coverage & architecture depth</p>
        </div>

        {/* Communication & Delivery - White Card */}
        <div className="bg-white border border-[#E5E9EF] rounded-2xl p-6 shadow-sm flex flex-col items-center justify-center text-center space-y-2">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-[#8993A0]">
            Clarity & Communication
          </span>
          <div className="text-3xl font-extrabold text-[#F5A623]">
            {Math.round(results.communication_score)}<span className="text-lg font-normal text-[#8993A0]">/100</span>
          </div>
          <p className="text-xs text-[#8993A0]">Structure, articulation & pacing</p>
        </div>
      </div>

      {/* Strengths & Weaknesses Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Strengths */}
        <div className="bg-white border border-[#E5E9EF] rounded-2xl p-6 shadow-sm space-y-3">
          <h3 className="text-sm font-bold text-[#202B38] flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            Demonstrated Strengths
          </h3>
          <ul className="space-y-2 text-xs text-[#202B38]">
            {results.strengths.map((str, idx) => (
              <li key={idx} className="flex items-start gap-2 bg-emerald-50/60 border border-emerald-100 p-3 rounded-xl">
                <span className="text-emerald-600 font-bold">•</span>
                <span>{str}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Weaknesses / Growth Areas */}
        <div className="bg-white border border-[#E5E9EF] rounded-2xl p-6 shadow-sm space-y-3">
          <h3 className="text-sm font-bold text-[#202B38] flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-[#F5A623]" />
            Key Areas for Improvement
          </h3>
          <ul className="space-y-2 text-xs text-[#202B38]">
            {results.weaknesses.map((w, idx) => (
              <li key={idx} className="flex items-start gap-2 bg-amber-50/60 border border-amber-100 p-3 rounded-xl">
                <span className="text-[#F5A623] font-bold">•</span>
                <span>{w}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Actionable Learning Recommendations */}
      {results.recommendations && results.recommendations.length > 0 && (
        <div className="bg-white border border-[#E5E9EF] rounded-2xl p-6 shadow-sm space-y-4">
          <h3 className="text-sm font-bold text-[#202B38] flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-[#F5A623]" />
            Personalized Next Steps & Practice Recommendations
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {results.recommendations.map((rec, i) => (
              <div key={i} className="bg-[#F8FAFC] border border-[#E5E9EF] p-4 rounded-xl flex flex-col justify-between space-y-3">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    {rec.action_type === "coding" && <Code2 className="w-4 h-4 text-emerald-600" />}
                    {rec.action_type === "resume" && <FileText className="w-4 h-4 text-[#123E63]" />}
                    {rec.action_type === "study" && <BookOpen className="w-4 h-4 text-[#F5A623]" />}
                    <h4 className="text-xs font-bold text-[#202B38]">{rec.title}</h4>
                  </div>
                  <p className="text-[11px] text-[#8993A0] leading-relaxed">{rec.description}</p>
                </div>

                <Link
                  href={rec.link}
                  className="text-xs text-[#123E63] hover:text-[#0D3557] font-semibold inline-flex items-center gap-1 mt-auto pt-2"
                >
                  <span>Practice Now</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Detailed Question by Question Rubric Breakdown */}
      <div className="space-y-4">
        <h2 className="text-base font-bold text-[#202B38] flex items-center gap-2">
          <HelpCircle className="w-4 h-4 text-[#123E63]" />
          Question Breakdown & Transparent Rubrics
        </h2>

        {results.questions.map((q, idx) => {
          const matchingAnswer = results.answers.find((a) => a.question_id === q.id);

          return (
            <div key={q.id} className="bg-white border border-[#E5E9EF] rounded-2xl p-6 shadow-sm space-y-4">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-[#E5E9EF] pb-3">
                <div className="flex items-center gap-2">
                  <span className="w-6 h-6 rounded-lg bg-[#123E63] text-white font-bold text-xs flex items-center justify-center">
                    {idx + 1}
                  </span>
                  <span className="text-[11px] font-semibold text-[#8993A0] uppercase">
                    {q.category.replace("_", " ")} {q.topic_or_skill ? `• ${q.topic_or_skill}` : ""}
                  </span>
                </div>

                {matchingAnswer && matchingAnswer.score !== null && matchingAnswer.score !== undefined && (
                  <span className={`px-2.5 py-0.5 rounded-full text-xs font-semibold border ${getScoreBadgeColor(matchingAnswer.score)}`}>
                    Score: {Math.round(matchingAnswer.score)}/100
                  </span>
                )}
              </div>

              {/* Question text */}
              <p className="text-sm font-semibold text-[#202B38]">{q.question_text}</p>

              {/* Student Answer */}
              {matchingAnswer ? (
                <div className="space-y-3 bg-[#F8FAFC] p-4 rounded-xl border border-[#E5E9EF] text-xs">
                  <div className="flex items-center justify-between text-xs text-[#8993A0]">
                    <span className="font-semibold text-[#202B38]">Your Response:</span>
                    {matchingAnswer.is_voice_response && (
                      <span className="flex items-center gap-1 text-[#123E63] font-medium">
                        <Volume2 className="w-3.5 h-3.5 text-[#F5A623]" />
                        Voice Transcribed
                      </span>
                    )}
                  </div>
                  <p className="text-[#202B38] leading-relaxed italic bg-white p-3 rounded-lg border border-[#E5E9EF]">
                    "{matchingAnswer.answer_text}"
                  </p>

                  {/* Delivery metrics if voice */}
                  {matchingAnswer.delivery_metrics && matchingAnswer.delivery_metrics.speaking_rate_wpm ? (
                    <div className="pt-2 border-t border-[#E5E9EF] text-xs text-[#8993A0] flex flex-wrap gap-4">
                      <span>
                        Pacing: <strong className="text-[#202B38]">{matchingAnswer.delivery_metrics.speaking_rate_wpm} WPM</strong>
                      </span>
                      <span>
                        Fillers: <strong className="text-[#202B38]">{matchingAnswer.delivery_metrics.filler_count || 0}</strong>
                      </span>
                      <span className="italic text-[#8993A0]">
                        {matchingAnswer.delivery_metrics.pacing_verdict}
                      </span>
                    </div>
                  ) : null}

                  {/* Feedback and suggestions */}
                  {matchingAnswer.detailed_feedback && (
                    <div className="pt-2 border-t border-[#E5E9EF] space-y-1 text-xs">
                      <span className="font-semibold text-[#123E63]">Evaluation Feedback:</span>
                      <p className="text-[#202B38] leading-relaxed">{matchingAnswer.detailed_feedback}</p>
                    </div>
                  )}

                  {/* Improvement tips */}
                  {matchingAnswer.improvement_tips && matchingAnswer.improvement_tips.length > 0 && (
                    <div className="space-y-1 text-xs pt-1">
                      <span className="font-semibold text-[#F5A623]">Suggestions to Elevate:</span>
                      <ul className="list-disc list-inside text-[#202B38] space-y-0.5">
                        {matchingAnswer.improvement_tips.map((tip, ti) => (
                          <li key={ti}>{tip}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-xs text-[#8993A0] italic">No answer submitted for this question.</div>
              )}

              {/* Reference Answer */}
              {q.reference_answer && (
                <div className="bg-[#123E63]/5 p-4 rounded-xl border border-[#123E63]/15 text-xs space-y-1.5">
                  <span className="font-semibold text-[#123E63] flex items-center gap-1.5">
                    <BookOpen className="w-3.5 h-3.5 text-[#F5A623]" />
                    Reference Answer / Ideal Strategy:
                  </span>
                  <p className="text-[#202B38] leading-relaxed">{q.reference_answer}</p>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}