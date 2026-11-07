"use client";

import React, { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import {
  Sparkles,
  Loader2,
  AlertCircle,
  CheckCircle2,
  HelpCircle,
  LogOut,
  ChevronRight,
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

      setAnswerText("");
      setIsVoiceResponse(false);
      setDeliveryMetrics(null);
      setAudioDuration(0);

      if (session && session.current_question_index + 1 >= session.total_questions) {
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
      <div className="py-24 text-center text-[#8993A0]">
        <Loader2 className="w-8 h-8 animate-spin mx-auto mb-3 text-[#123E63]" />
        <p className="text-xs font-semibold">Preparing interview simulation...</p>
      </div>
    );
  }

  if (errorMsg && !session) {
    return (
      <div className="bg-white rounded-2xl p-8 shadow-card border border-[#E5E9EF] max-w-lg mx-auto text-center space-y-4 my-12">
        <AlertCircle className="w-10 h-10 text-red-500 mx-auto" />
        <h3 className="text-base font-bold text-[#202B38]">Session Unavailable</h3>
        <p className="text-xs text-[#8993A0]">{errorMsg}</p>
        <button
          onClick={() => router.push("/interview")}
          className="px-5 py-2 bg-[#123E63] text-white rounded-xl text-xs font-bold"
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
    <div className="space-y-6 max-w-4xl">
      {/* Top Bar with Status, Progress, and Timer */}
      <div className="bg-white rounded-2xl p-5 shadow-card border border-[#E5E9EF] flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-[#123E63] text-white flex items-center justify-center font-bold text-sm shadow-xs">
            Q{currentIdx}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-sm font-bold text-[#202B38]">
                Question {currentIdx} of {totalCount}
              </span>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#FFF6E8] text-[#F5A623] border border-[#F5A623]/30">
                {session?.interview_type.toUpperCase()}
              </span>
            </div>
            <p className="text-xs text-[#8993A0]">
              Role: <strong className="text-[#202B38]">{session?.target_role}</strong> ({session?.experience_level})
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 self-end sm:self-auto">
          {session && (
            <InterviewTimer
              totalMinutes={session.duration_minutes}
              onTimeExpired={() => setShowEndConfirm(true)}
            />
          )}

          <button
            onClick={() => setShowEndConfirm(true)}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-red-50 hover:bg-red-100 border border-red-200 text-red-600 text-xs font-bold rounded-xl transition"
          >
            <LogOut className="w-3.5 h-3.5" />
            <span>Finish Early</span>
          </button>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-[#E5E9EF] h-1.5 rounded-full overflow-hidden">
        <div
          className="bg-[#123E63] h-full transition-all duration-300 rounded-full"
          style={{ width: `${progressPercent}%` }}
        />
      </div>

      {errorMsg && (
        <div className="p-3 bg-red-50 border border-red-200 text-red-700 rounded-xl text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 shrink-0 text-red-500" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Current Question Display Card */}
      {currentQuestion && (
        <div className="bg-white rounded-2xl p-6 sm:p-7 shadow-card border border-[#E5E9EF] space-y-4">
          <div className="flex items-center justify-between text-xs text-[#8993A0] border-b border-[#E5E9EF] pb-3">
            <span className="uppercase tracking-wider font-bold text-[#123E63]">
              Category: {currentQuestion.category.replace("_", " ")}
            </span>
            {currentQuestion.topic_or_skill && (
              <span className="bg-[#F1F3F6] px-2.5 py-0.5 rounded-md text-[#202B38] font-semibold text-[11px]">
                Topic: {currentQuestion.topic_or_skill}
              </span>
            )}
          </div>

          <p className="text-base sm:text-lg font-bold text-[#202B38] leading-relaxed">
            {currentQuestion.question_text}
          </p>

          {currentQuestion.expected_key_points && currentQuestion.expected_key_points.length > 0 && (
            <div className="bg-[#F8F9FA] rounded-xl p-3.5 border border-[#E5E9EF] text-xs space-y-1.5">
              <span className="text-[#8993A0] font-bold flex items-center gap-1.5 text-[11px] uppercase tracking-wider">
                <HelpCircle className="w-3.5 h-3.5 text-[#F5A623]" />
                Interviewer Focus Points:
              </span>
              <div className="flex flex-wrap gap-1.5 pt-0.5">
                {currentQuestion.expected_key_points.map((pt, i) => (
                  <span
                    key={i}
                    className="bg-white border border-[#E5E9EF] px-2.5 py-0.5 rounded-md text-[#202B38] text-[11px] font-medium"
                  >
                    &bull; {pt}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Answer Workspace */}
      <div className="bg-white rounded-2xl p-6 sm:p-7 shadow-card border border-[#E5E9EF] space-y-5">
        <VoiceRecorder
          sessionId={sessionId}
          onTranscriptReady={handleVoiceTranscriptReady}
          disabled={isSubmittingAnswer || isEndingSession}
        />

        <form onSubmit={handleSubmitAnswer} className="space-y-4">
          <div className="space-y-1.5">
            <div className="flex items-center justify-between text-xs">
              <label className="font-bold text-[#8993A0] uppercase tracking-wider text-[11px]">
                Your Spoken / Typed Response:
              </label>
              <span className="text-[#8993A0]">
                {answerText.trim() ? `${answerText.trim().split(/\s+/).length} words` : "0 words"}
              </span>
            </div>
            <textarea
              rows={6}
              value={answerText}
              onChange={(e) => setAnswerText(e.target.value)}
              placeholder="Structure your response with clear engineering reasoning, architecture details, and measurable impact..."
              disabled={isSubmittingAnswer}
              className="w-full bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl p-4 text-[#202B38] placeholder-[#8993A0] focus:outline-none focus:border-[#123E63] text-xs font-medium leading-relaxed"
            />
          </div>

          <div className="flex items-center justify-between pt-2">
            <span className="text-[11px] text-[#8993A0]">
              Evaluated instantly with AI rubrics on technical accuracy and speech delivery.
            </span>

            <button
              type="submit"
              disabled={!answerText.trim() || isSubmittingAnswer}
              className="flex items-center gap-2 bg-[#F5A623] hover:bg-[#E09212] text-white font-bold px-6 py-2.5 rounded-xl transition shadow-md disabled:opacity-50 text-xs"
            >
              {isSubmittingAnswer ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
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

      {/* Confirmation Modal */}
      {showEndConfirm && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-xs z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-md w-full p-6 space-y-4 shadow-2xl border border-[#E5E9EF]">
            <h3 className="text-base font-bold text-[#202B38]">Conclude Mock Interview?</h3>
            <p className="text-xs text-[#8993A0] leading-relaxed">
              Are you sure you want to end this interview session? Your completed answers will be scored and your final feedback report generated immediately.
            </p>
            <div className="flex items-center justify-end gap-2.5 pt-2">
              <button
                type="button"
                onClick={() => setShowEndConfirm(false)}
                disabled={isEndingSession}
                className="px-4 py-2 bg-[#F8F9FA] text-[#202B38] border border-[#E5E9EF] rounded-xl text-xs font-bold"
              >
                Continue
              </button>
              <button
                type="button"
                onClick={handleEndInterview}
                disabled={isEndingSession}
                className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-xl text-xs font-bold flex items-center gap-1.5"
              >
                {isEndingSession ? "Finalizing..." : "End Session Now"}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
