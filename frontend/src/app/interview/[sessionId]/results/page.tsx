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
      <div className="py-24 text-center text-slate-400">
        <div className="w-8 h-8 border-2 border-sky-400 border-t-transparent rounded-full animate-spin mx-auto mb-3" />
        <p className="text-sm">Compiling evaluation analytics & transparent rubric...</p>
      </div>
    );
  }

  if (errorMsg || !results) {
    return (
      <div className="max-w-xl mx-auto py-16 text-center space-y-4">
        <div className="w-12 h-12 rounded-full bg-rose-950/60 border border-rose-800 flex items-center justify-center text-rose-400 mx-auto">
          <AlertTriangle className="w-6 h-6" />
        </div>
        <h2 className="text-xl font-bold text-white">Results Unavailable</h2>
        <p className="text-slate-400 text-sm">{errorMsg || "Could not retrieve results."}</p>
        <Link
          href="/interview"
          className="inline-block px-6 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg text-sm font-medium transition"
        >
          Return to Studio
        </Link>
      </div>
    );
  }

  const getScoreBadgeColor = (score: number) => {
    if (score >= 80) return "text-emerald-400 border-emerald-500/40 bg-emerald-950/50";
    if (score >= 60) return "text-sky-400 border-sky-500/40 bg-sky-950/50";
    return "text-amber-400 border-amber-500/40 bg-amber-950/50";
  };

  return (
    <div className="max-w-4xl mx-auto py-4 space-y-8">
      {/* Top Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-950/80 border border-emerald-800 text-emerald-300 text-xs font-semibold mb-2">
            <Award className="w-3.5 h-3.5 text-emerald-400" />
            Interview Performance Report
          </div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">
            Session Evaluation & Feedback
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Target Role: <span className="text-slate-200 font-medium">{results.target_role}</span> • Level: {results.experience_level} • {new Date(results.started_at).toLocaleDateString()}
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Link
            href="/interview"
            className="flex items-center gap-2 px-4 py-2 bg-sky-600 hover:bg-sky-500 text-white text-sm font-medium rounded-xl transition shadow-lg shadow-sky-950"
          >
            <RotateCcw className="w-4 h-4" />
            <span>Practice Another</span>
          </Link>
          <Link
            href="/interview/history"
            className="flex items-center gap-2 px-4 py-2 bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-300 text-sm font-medium rounded-xl transition"
          >
            <History className="w-4 h-4 text-sky-400" />
            <span>History</span>
          </Link>
        </div>
      </div>

      {/* Primary Score Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Overall Score */}
        <div className="glass-card p-6 flex flex-col items-center justify-center text-center space-y-2 border-slate-800">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Overall Readiness Score
          </span>
          <div className={`text-4xl font-extrabold px-4 py-2 rounded-2xl border ${getScoreBadgeColor(results.overall_score)}`}>
            {Math.round(results.overall_score)}<span className="text-xl font-normal text-slate-400">/100</span>
          </div>
          <p className="text-xs text-slate-400">Automated student practice evaluation</p>
        </div>

        {/* Technical Accuracy */}
        <div className="glass-card p-6 flex flex-col items-center justify-center text-center space-y-2 border-slate-800">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Technical Proficiency
          </span>
          <div className="text-3xl font-bold text-sky-400">
            {Math.round(results.technical_score)}<span className="text-lg font-normal text-slate-500">/100</span>
          </div>
          <p className="text-xs text-slate-400">Concept coverage & architecture depth</p>
        </div>

        {/* Communication & Delivery */}
        <div className="glass-card p-6 flex flex-col items-center justify-center text-center space-y-2 border-slate-800">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Clarity & Communication
          </span>
          <div className="text-3xl font-bold text-indigo-400">
            {Math.round(results.communication_score)}<span className="text-lg font-normal text-slate-500">/100</span>
          </div>
          <p className="text-xs text-slate-400">Structure, articulation & pacing</p>
        </div>
      </div>

      {/* Strengths & Weaknesses Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Strengths */}
        <div className="glass-card p-6 space-y-3">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <CheckCircle2 className="w-5 h-5 text-emerald-400" />
            Demonstrated Strengths
          </h3>
          <ul className="space-y-2 text-sm text-slate-300">
            {results.strengths.map((str, idx) => (
              <li key={idx} className="flex items-start gap-2 bg-emerald-950/20 border border-emerald-900/40 p-2.5 rounded-lg">
                <span className="text-emerald-400 font-bold">•</span>
                <span>{str}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Weaknesses / Growth Areas */}
        <div className="glass-card p-6 space-y-3">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-amber-400" />
            Key Areas for Improvement
          </h3>
          <ul className="space-y-2 text-sm text-slate-300">
            {results.weaknesses.map((w, idx) => (
              <li key={idx} className="flex items-start gap-2 bg-amber-950/20 border border-amber-900/40 p-2.5 rounded-lg">
                <span className="text-amber-400 font-bold">•</span>
                <span>{w}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Actionable Learning Recommendations */}
      {results.recommendations && results.recommendations.length > 0 && (
        <div className="glass-card p-6 space-y-4">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-sky-400" />
            Personalized Next Steps & Practice Recommendations
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {results.recommendations.map((rec, i) => (
              <div key={i} className="bg-slate-900 border border-slate-800 p-4 rounded-xl flex flex-col justify-between space-y-3">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    {rec.action_type === "coding" && <Code2 className="w-4 h-4 text-emerald-400" />}
                    {rec.action_type === "resume" && <FileText className="w-4 h-4 text-indigo-400" />}
                    {rec.action_type === "study" && <BookOpen className="w-4 h-4 text-sky-400" />}
                    <h4 className="text-sm font-semibold text-white">{rec.title}</h4>
                  </div>
                  <p className="text-xs text-slate-400">{rec.description}</p>
                </div>

                <Link
                  href={rec.link}
                  className="text-xs text-sky-400 hover:text-sky-300 font-medium inline-flex items-center gap-1 mt-auto pt-2"
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
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <HelpCircle className="w-5 h-5 text-sky-400" />
          Question Breakdown & Transparent Rubrics
        </h2>

        {results.questions.map((q, idx) => {
          const matchingAnswer = results.answers.find((a) => a.question_id === q.id);

          return (
            <div key={q.id} className="glass-card p-6 space-y-4">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-slate-800 pb-3">
                <div className="flex items-center gap-2">
                  <span className="w-6 h-6 rounded-md bg-sky-950 border border-sky-800 text-sky-400 font-bold text-xs flex items-center justify-center">
                    {idx + 1}
                  </span>
                  <span className="text-xs font-semibold text-slate-400 uppercase">
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
              <p className="text-base font-medium text-white">{q.question_text}</p>

              {/* Student Answer */}
              {matchingAnswer ? (
                <div className="space-y-3 bg-slate-900/60 p-4 rounded-xl border border-slate-800 text-sm">
                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span className="font-semibold text-slate-300">Your Response:</span>
                    {matchingAnswer.is_voice_response && (
                      <span className="flex items-center gap-1 text-sky-400">
                        <Volume2 className="w-3.5 h-3.5" />
                        Voice Transcribed
                      </span>
                    )}
                  </div>
                  <p className="text-slate-300 leading-relaxed italic">
                    "{matchingAnswer.answer_text}"
                  </p>

                  {/* Delivery metrics if voice */}
                  {matchingAnswer.delivery_metrics && matchingAnswer.delivery_metrics.speaking_rate_wpm ? (
                    <div className="pt-2 border-t border-slate-800/80 text-xs text-slate-400 flex flex-wrap gap-4">
                      <span>
                        Pacing: <strong className="text-slate-200">{matchingAnswer.delivery_metrics.speaking_rate_wpm} WPM</strong>
                      </span>
                      <span>
                        Fillers: <strong className="text-slate-200">{matchingAnswer.delivery_metrics.filler_count || 0}</strong>
                      </span>
                      <span className="text-slate-400 italic">
                        {matchingAnswer.delivery_metrics.pacing_verdict}
                      </span>
                    </div>
                  ) : null}

                  {/* Feedback and suggestions */}
                  {matchingAnswer.detailed_feedback && (
                    <div className="pt-2 border-t border-slate-800/80 space-y-1 text-xs">
                      <span className="font-semibold text-sky-400">Evaluation Feedback:</span>
                      <p className="text-slate-300">{matchingAnswer.detailed_feedback}</p>
                    </div>
                  )}

                  {/* Improvement tips */}
                  {matchingAnswer.improvement_tips && matchingAnswer.improvement_tips.length > 0 && (
                    <div className="space-y-1 text-xs pt-1">
                      <span className="font-semibold text-amber-400">Suggestions to Elevate:</span>
                      <ul className="list-disc list-inside text-slate-400 space-y-0.5">
                        {matchingAnswer.improvement_tips.map((tip, ti) => (
                          <li key={ti}>{tip}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ) : (
                <div className="text-xs text-slate-500 italic">No answer submitted for this question.</div>
              )}

              {/* Reference Answer */}
              {q.reference_answer && (
                <div className="bg-slate-950/70 p-4 rounded-xl border border-slate-800/60 text-xs space-y-1.5">
                  <span className="font-semibold text-slate-400 flex items-center gap-1.5">
                    <BookOpen className="w-3.5 h-3.5 text-sky-400" />
                    Reference Answer / Ideal Strategy:
                  </span>
                  <p className="text-slate-300 leading-relaxed">{q.reference_answer}</p>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
