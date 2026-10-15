"use client";

import React, { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import {
  Sparkles,
  Send,
  Loader2,
  AlertCircle,
  CheckCircle2,
  HelpCircle,
  LogOut,
  ChevronRight,
  BookOpen,
} from "lucide-react";
import InterviewTimer from "@/components/interview/InterviewTimer";
import VoiceRecorder from "@/components/interview/VoiceRecorder";
import { InterviewSessionOut, QuestionOut, AnswerOut } from "@/types/interview";

export default function ActiveInterviewRoom() {
  const params = useParams();
  const router = useRouter();
  const sessionId = params.sessionId as string;
  const { user, isLoading: authLoading } = useAuth();

  const [session, setSession] = useState<InterviewSessionOut | null>(null);
  const [currentQuestion, setCurrentQuestion] = useState<QuestionOut | null>(null);
  const [answerText, setAnswerText] = useState("");
  const [isVoiceResponse, setIsVoiceResponse] = useState(false);
  const [deliveryMetrics, setDeliveryMetrics] = useState<any>(null);
  const [audioDuration, setAudioDuration] = useState<number>(0);

  const [isFetchingSession, setIsFetchingSession] = useState(true);
  const [isSubmittingAnswer, setIsSubmittingAnswer] = useState(false);
  const [isEndingSession, setIsEndingSession] = useState(false);
  const [showEndConfirm, setShowEndConfirm] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push("/login");
      return;
    }

    if (sessionId) {
      fetchSessionAndQuestion();
    }
  }, [sessionId, user, authLoading]);

  const fetchSessionAndQuestion = async () => {
    setIsFetchingSession(true);
    setErrorMsg(null);
    try {
      const sess = await apiFetch<InterviewSessionOut>(`/interviews/sessions/${sessionId}`);
      setSession(sess);

      if (sess.status === "completed") {
        router.push(`/interview/${sessionId}/results`);
        return;
      }

      // Fetch current active question
      const currQ = await apiFetch<QuestionOut>(`/interviews/sessions/${sessionId}/current-question`);
      setCurrentQuestion(currQ);
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to load interview session.");
    } finally {
      setIsFetchingSession(false);
    }
  };

  const handleVoiceTranscriptReady = (transcript: string, metrics: any, duration: number) => {
    setAnswerText((prev) => (prev ? `${prev} ${transcript}` : transcript));
    setIsVoiceResponse(true);
    setDeliveryMetrics(metrics);
    setAudioDuration(duration);
  };

  const handleSubmitAnswer = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!answerText.trim() || !currentQuestion) return;

    setIsSubmittingAnswer(true);
    setErrorMsg(null);

    try {
      await apiFetch<AnswerOut>(`/interviews/sessions/${sessionId}/answers`, {
        method: "POST",
        body: JSON.stringify({
          question_id: currentQuestion.id,
          answer_text: answerText.trim(),
          is_voice_response: isVoiceResponse,
          duration_seconds: audioDuration > 0 ? audioDuration : undefined,
          delivery_metrics: deliveryMetrics || undefined,
        }),
      });

      // Reset input state for next question
      setAnswerText("");
      setIsVoiceResponse(false);
      setDeliveryMetrics(null);
      setAudioDuration(0);

      // Check if session reached end or fetch next question
      if (session && session.current_question_index + 1 >= session.total_questions) {
        // Automatically finalize session
        await handleEndInterview();
      } else {
        await fetchSessionAndQuestion();
      }
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to submit answer.");
    } finally {
      setIsSubmittingAnswer(false);
    }
  };

  const handleEndInterview = async () => {
    setIsEndingSession(true);
    setErrorMsg(null);
    try {
      await apiFetch<InterviewSessionOut>(`/interviews/sessions/${sessionId}/end`, {
        method: "POST",
      });
      router.push(`/interview/${sessionId}/results`);
    } catch (err: any) {
      setErrorMsg(err.message || "Failed to finalize interview.");
      setIsEndingSession(false);
      setShowEndConfirm(false);
    }
  };

  if (authLoading || isFetchingSession) {
    return (
      <div className="py-24 text-center text-slate-400">
        <Loader2 className="w-8 h-8 animate-spin mx-auto mb-3 text-sky-400" />
        <p className="text-sm">Preparing interview environment...</p>
      </div>
    );
  }

  if (errorMsg && !session) {
    return (
      <div className="max-w-xl mx-auto py-16 text-center space-y-4">
        <div className="w-12 h-12 rounded-full bg-rose-950/60 border border-rose-800 flex items-center justify-center text-rose-400 mx-auto">
          <AlertCircle className="w-6 h-6" />
        </div>
        <h2 className="text-xl font-bold text-white">Interview Session Unavailable</h2>
        <p className="text-slate-400 text-sm">{errorMsg}</p>
        <button
          onClick={() => router.push("/interview")}
          className="px-6 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-lg text-sm font-medium transition"
        >
          Return to Studio
        </button>
      </div>
    );
  }

  const currentIdx = session ? session.current_question_index + 1 : 1;
  const totalCount = session ? session.total_questions : 5;
  const progressPercent = Math.min(100, Math.round(((currentIdx - 1) / totalCount) * 100));

  return (
    <div className="max-w-4xl mx-auto py-4 space-y-6">
      {/* Top Bar with Status, Progress, and Timer */}
      <div className="glass-card p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-lg bg-sky-950/80 border border-sky-800 flex items-center justify-center text-sky-400 font-bold text-sm">
            Q{currentIdx}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-sm font-semibold text-white">
                Question {currentIdx} of {totalCount}
              </span>
              <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
                {session?.interview_type.toUpperCase()}
              </span>
            </div>
            <p className="text-xs text-slate-400">
              Role: <span className="text-slate-300 font-medium">{session?.target_role}</span> ({session?.experience_level})
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {session && (
            <InterviewTimer
              totalMinutes={session.duration_minutes}
              onTimeExpired={() => setShowEndConfirm(true)}
            />
          )}

          <button
            onClick={() => setShowEndConfirm(true)}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-rose-950/40 hover:bg-rose-900/60 border border-rose-800 text-rose-300 text-xs font-medium rounded-lg transition"
          >
            <LogOut className="w-3.5 h-3.5" />
            <span>Finish Early</span>
          </button>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-slate-900 h-1.5 rounded-full overflow-hidden border border-slate-800">
        <div
          className="bg-sky-500 h-full transition-all duration-300 rounded-full"
          style={{ width: `${progressPercent}%` }}
        />
      </div>

      {errorMsg && (
        <div className="p-3 bg-rose-950/50 border border-rose-800 text-rose-300 rounded-xl text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Current Question Display Card */}
      {currentQuestion && (
        <div className="glass-card p-6 md:p-8 space-y-4">
          <div className="flex items-center justify-between text-xs text-slate-400 border-b border-slate-800 pb-2">
            <span className="uppercase tracking-wider font-semibold text-sky-400">
              Category: {currentQuestion.category.replace("_", " ")}
            </span>
            {currentQuestion.topic_or_skill && (
              <span className="bg-slate-800 px-2.5 py-0.5 rounded text-slate-300">
                Topic: {currentQuestion.topic_or_skill}
              </span>
            )}
          </div>

          <p className="text-lg md:text-xl font-medium text-white leading-relaxed">
            {currentQuestion.question_text}
          </p>

          {currentQuestion.expected_key_points && currentQuestion.expected_key_points.length > 0 && (
            <div className="bg-slate-900/50 rounded-lg p-3 border border-slate-800/80 text-xs space-y-1">
              <span className="text-slate-400 font-semibold flex items-center gap-1">
                <HelpCircle className="w-3.5 h-3.5 text-indigo-400" />
                Interviewer Focus Areas:
              </span>
              <div className="flex flex-wrap gap-1.5 pt-1">
                {currentQuestion.expected_key_points.map((pt, i) => (
                  <span
                    key={i}
                    className="bg-slate-800/80 border border-slate-700/80 px-2 py-0.5 rounded text-slate-300"
                  >
                    • {pt}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Answer Workspace */}
      <div className="glass-card p-6 space-y-4">
        {/* Optional Voice Recorder */}
        <VoiceRecorder
          sessionId={sessionId}
          onTranscriptReady={handleVoiceTranscriptReady}
          disabled={isSubmittingAnswer || isEndingSession}
        />

        {/* Text Answer Area */}
        <form onSubmit={handleSubmitAnswer} className="space-y-4">
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-300 flex items-center justify-between">
              <span>Your Answer (Speak or Type):</span>
              <span className="text-slate-500 font-normal">
                {answerText.trim() ? `${answerText.trim().split(/\s+/).length} words` : "0 words"}
              </span>
            </label>
            <textarea
              rows={6}
              value={answerText}
              onChange={(e) => setAnswerText(e.target.value)}
              placeholder="Structure your answer clearly with context, engineering rationale, examples, and measurable impact..."
              disabled={isSubmittingAnswer}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl p-4 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500 text-sm leading-relaxed"
            />
          </div>

          <div className="flex items-center justify-between pt-2">
            <span className="text-xs text-slate-500">
              Answers are scored against transparent rubrics and saved to your progress profile.
            </span>

            <button
              type="submit"
              disabled={!answerText.trim() || isSubmittingAnswer}
              className="flex items-center gap-2 bg-sky-600 hover:bg-sky-500 text-white font-medium px-6 py-2.5 rounded-xl transition shadow-lg shadow-sky-950 disabled:opacity-50 text-sm"
            >
              {isSubmittingAnswer ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Evaluating Answer...</span>
                </>
              ) : currentIdx === totalCount ? (
                <>
                  <span>Submit & Complete</span>
                  <CheckCircle2 className="w-4 h-4" />
                </>
              ) : (
                <>
                  <span>Submit & Next Question</span>
                  <ChevronRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Confirmation Modal to End Interview Early */}
      {showEndConfirm && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="glass-card max-w-md w-full p-6 space-y-4 border-slate-700">
            <div className="w-10 h-10 rounded-full bg-amber-950/60 border border-amber-800 flex items-center justify-center text-amber-400">
              <LogOut className="w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold text-white">Conclude Mock Interview?</h3>
            <p className="text-slate-300 text-sm">
              Are you sure you want to finalize this session now? All answered questions will be evaluated, and your performance report will be generated immediately.
            </p>
            <div className="flex items-center justify-end gap-3 pt-3">
              <button
                type="button"
                onClick={() => setShowEndConfirm(false)}
                disabled={isEndingSession}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-lg text-sm font-medium transition"
              >
                Continue Interview
              </button>
              <button
                type="button"
                onClick={handleEndInterview}
                disabled={isEndingSession}
                className="flex items-center gap-2 px-4 py-2 bg-rose-600 hover:bg-rose-500 text-white rounded-lg text-sm font-medium transition"
              >
                {isEndingSession ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Finalizing...</span>
                  </>
                ) : (
                  <span>Yes, End Session</span>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
