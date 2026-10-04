"use client";

import React, { useEffect, useState, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import {
  InterviewSessionDetail,
  InterviewQuestion as IQuestion,
  InterviewResponse as IResponse,
  VoicePipelineResult,
} from "@/types/interview";
import InterviewQuestion from "@/components/interview/InterviewQuestion";
import { RecordedAudioData } from "@/components/voice/AudioRecorder";
import {
  Loader2,
  AlertCircle,
  Play,
  CheckCircle2,
  ArrowLeft,
  Sparkles,
  ArrowRight,
  Briefcase,
  Layers,
} from "lucide-react";

export default function InterviewSessionPage() {
  const { id } = useParams() as { id: string };
  const { user, isLoading: isAuthLoading } = useAuth();
  const router = useRouter();

  // State
  const [session, setSession] = useState<InterviewSessionDetail | null>(null);
  const [questions, setQuestions] = useState<IQuestion[]>([]);
  const [responsesMap, setResponsesMap] = useState<Record<string, string>>({});
  const [responseIdsMap, setResponseIdsMap] = useState<Record<string, string>>({});
  const [currentIndex, setCurrentIndex] = useState<number>(0);

  // UX & Loading State
  const [isLoadingSession, setIsLoadingSession] = useState<boolean>(true);
  const [isGeneratingQuestions, setIsGeneratingQuestions] = useState<boolean>(false);
  const [isStartingSession, setIsStartingSession] = useState<boolean>(false);
  const [isSubmittingAnswer, setIsSubmittingAnswer] = useState<boolean>(false);
  const [isCompletingSession, setIsCompletingSession] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Authentication check
  useEffect(() => {
    if (!isAuthLoading && !user) {
      router.push("/login");
    }
  }, [user, isAuthLoading, router]);

  // Load session data
  const loadSession = useCallback(async () => {
    if (!id || !user) return;

    try {
      setIsLoadingSession(true);
      setErrorMessage(null);

      const data = await apiFetch<InterviewSessionDetail>(`/interview/sessions/${id}`);
      setSession(data);

      const qs = data.questions || [];
      setQuestions(qs);

      // Build answers map and response IDs from existing responses
      const map: Record<string, string> = {};
      const idsMap: Record<string, string> = {};
      if (data.responses) {
        data.responses.forEach((r: IResponse) => {
          map[r.question_id] = r.transcribed_text;
          idsMap[r.question_id] = r.id;
        });
      }
      setResponsesMap(map);
      setResponseIdsMap(idsMap);

      // Set initial question index based on current progress
      if (qs.length > 0) {
        // If some questions are answered, position at first unanswered, or current_question_index
        const answeredCount = Object.keys(map).length;
        if (answeredCount > 0 && answeredCount < qs.length) {
          setCurrentIndex(answeredCount);
        } else if (answeredCount >= qs.length) {
          setCurrentIndex(qs.length - 1);
        } else {
          setCurrentIndex(0);
        }
      }
    } catch (err: any) {
      setErrorMessage(err.message || "Failed to load interview session.");
    } finally {
      setIsLoadingSession(false);
    }
  }, [id, user]);

  useEffect(() => {
    if (user) {
      loadSession();
    }
  }, [user, loadSession]);

  // Handle Question Generation if empty
  const handleGenerateQuestions = async () => {
    if (isGeneratingQuestions || !id) return;
    try {
      setIsGeneratingQuestions(true);
      setErrorMessage(null);

      const generated = await apiFetch<IQuestion[]>(`/interview/sessions/${id}/generate-questions`, {
        method: "POST",
      });

      setQuestions(generated);
      setCurrentIndex(0);
      if (session) {
        setSession({ ...session, questions: generated, question_count: generated.length });
      }
    } catch (err: any) {
      setErrorMessage(err.message || "Failed to generate interview questions. Please try again.");
    } finally {
      setIsGeneratingQuestions(false);
    }
  };

  // Start the session (transitions pending -> in_progress)
  const handleStartSession = async () => {
    if (isStartingSession || !id) return;
    try {
      setIsStartingSession(true);
      setErrorMessage(null);

      const updated = await apiFetch<InterviewSessionDetail>(`/interview/sessions/${id}/start`, {
        method: "POST",
      });

      setSession((prev) => (prev ? { ...prev, status: updated.status } : updated));

      // If questions are not yet generated, generate them now
      if (questions.length === 0) {
        await handleGenerateQuestions();
      }
    } catch (err: any) {
      setErrorMessage(err.message || "Failed to start interview session.");
    } finally {
      setIsStartingSession(false);
    }
  };

  // Submit Answer for the current question (Written or Voice)
  const handleSubmitAnswer = async (answerText: string, audioData?: RecordedAudioData) => {
    if (!session || questions.length === 0 || isSubmittingAnswer) return;

    const currentQuestion = questions[currentIndex];
    if (!currentQuestion) return;

    try {
      setIsSubmittingAnswer(true);
      setErrorMessage(null);

      let savedTranscript = answerText;

      if (audioData) {
        // Full Voice Pipeline: Upload -> STT -> Analysis -> Metrics -> Feedback -> Persistence
        const formData = new FormData();
        formData.append("question_id", currentQuestion.id);
        const audioFile = new File([audioData.blob], "recording.webm", {
          type: audioData.blob.type || "audio/webm",
        });
        formData.append("file", audioFile);
        formData.append("duration_seconds", String(audioData.durationSeconds));

        const existingRespId = responseIdsMap[currentQuestion.id];
        if (existingRespId) {
          formData.append("response_id", existingRespId);
        }

        const pipelineResult = await apiFetch<VoicePipelineResult>(
          `/voice/sessions/${session.id}/process-audio`,
          {
            method: "POST",
            body: formData,
          }
        );

        savedTranscript = pipelineResult.transcript || answerText;

        setResponsesMap((prev) => ({
          ...prev,
          [currentQuestion.id]: savedTranscript,
        }));
        setResponseIdsMap((prev) => ({
          ...prev,
          [currentQuestion.id]: pipelineResult.response_id,
        }));
      } else {
        // Written Answer Submission
        const response = await apiFetch<IResponse>(`/interview/sessions/${session.id}/responses`, {
          method: "POST",
          body: JSON.stringify({
            question_id: currentQuestion.id,
            answer_text: answerText,
            allow_retry: true,
          }),
        });

        savedTranscript = response.transcribed_text || answerText;

        setResponsesMap((prev) => ({
          ...prev,
          [currentQuestion.id]: savedTranscript,
        }));
        setResponseIdsMap((prev) => ({
          ...prev,
          [currentQuestion.id]: response.id,
        }));
      }

      // If not last question, smoothly advance to next question
      if (currentIndex < questions.length - 1) {
        setCurrentIndex((prev) => prev + 1);
      }
    } catch (err: any) {
      setErrorMessage(err.message || "Failed to submit and process answer. Please try again.");
      throw err;
    } finally {
      setIsSubmittingAnswer(false);
    }
  };

  // Complete Interview
  const handleFinishInterview = async () => {
    if (!session || isCompletingSession) return;
    try {
      setIsCompletingSession(true);
      setErrorMessage(null);

      const completed = await apiFetch<InterviewSessionDetail>(`/interview/sessions/${session.id}/complete`, {
        method: "POST",
      });

      setSession((prev) => (prev ? { ...prev, status: "completed", completed_at: completed.completed_at } : completed));

      // Redirect to results page
      router.push(`/interview/result/${session.id}`);
    } catch (err: any) {
      setErrorMessage(err.message || "Failed to finalize interview session.");
      setIsCompletingSession(false);
    }
  };

  // Navigation handlers
  const handlePreviousQuestion = () => {
    if (currentIndex > 0) {
      setCurrentIndex((prev) => prev - 1);
    }
  };

  const handleNextQuestion = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex((prev) => prev + 1);
    }
  };

  // Loading Screen
  if (isAuthLoading || isLoadingSession) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-3">
        <Loader2 className="w-8 h-8 animate-spin text-sky-400" />
        <p className="text-sm text-slate-400">Loading interview room...</p>
      </div>
    );
  }

  // Error / Not Found Screen
  if (!session) {
    return (
      <div className="max-w-xl mx-auto py-16 text-center space-y-4">
        <div className="p-4 rounded-2xl bg-rose-950/40 border border-rose-500/40 text-rose-400 inline-flex">
          <AlertCircle className="w-8 h-8" />
        </div>
        <h2 className="text-xl font-bold text-white">Interview Session Not Found</h2>
        <p className="text-sm text-slate-400">
          {errorMessage || "The interview session you requested does not exist or you do not have permission to view it."}
        </p>
        <div className="pt-2">
          <Link
            href="/interview"
            className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold border border-slate-700 transition"
          >
            <ArrowLeft className="w-4 h-4" />
            <span>Return to Interviews</span>
          </Link>
        </div>
      </div>
    );
  }

  // Already Completed Session Screen
  if (session.status === "completed") {
    return (
      <div className="max-w-xl mx-auto py-16 text-center space-y-4">
        <div className="p-4 rounded-2xl bg-emerald-950/50 border border-emerald-500/40 text-emerald-400 inline-flex">
          <CheckCircle2 className="w-8 h-8" />
        </div>
        <h2 className="text-2xl font-bold text-white">Interview Session Completed</h2>
        <p className="text-sm text-slate-400">
          This interview has already been submitted and finalized. You can view your detailed feedback and metrics below.
        </p>
        <div className="pt-4 flex items-center justify-center gap-3">
          <Link
            href={`/interview/result/${session.id}`}
            className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-sm shadow-lg shadow-sky-600/25 transition"
          >
            <span>View Interview Result</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
          <Link
            href="/interview"
            className="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm font-semibold border border-slate-700 transition"
          >
            <span>Back to Dashboard</span>
          </Link>
        </div>
      </div>
    );
  }

  // Pending State Screen: Ready to Begin
  if (session.status === "pending") {
    return (
      <div className="max-w-2xl mx-auto py-10 space-y-6">
        <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 shadow-xl text-center space-y-6">
          <div className="p-4 rounded-2xl bg-sky-500/10 text-sky-400 inline-flex border border-sky-500/20">
            <Sparkles className="w-8 h-8" />
          </div>

          <div>
            <h1 className="text-2xl md:text-3xl font-extrabold text-white tracking-tight">
              Ready to Begin Your Interview
            </h1>
            <p className="text-slate-400 text-sm mt-2">
              You are about to start a simulated mock interview for the{" "}
              <span className="text-sky-400 font-semibold">{session.target_role}</span> position.
            </p>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-left py-2">
            <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
              <span className="text-[11px] text-slate-400 block font-medium">Role</span>
              <span className="text-xs font-bold text-white line-clamp-1">{session.target_role}</span>
            </div>
            <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
              <span className="text-[11px] text-slate-400 block font-medium">Type</span>
              <span className="text-xs font-bold text-white">{session.interview_type}</span>
            </div>
            <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
              <span className="text-[11px] text-slate-400 block font-medium">Difficulty</span>
              <span className="text-xs font-bold text-amber-400">{session.difficulty}</span>
            </div>
            <div className="p-3.5 rounded-xl bg-slate-950 border border-slate-800">
              <span className="text-[11px] text-slate-400 block font-medium">Questions</span>
              <span className="text-xs font-bold text-white">{session.question_count} Questions</span>
            </div>
          </div>

          {errorMessage && (
            <div className="p-3.5 rounded-xl bg-rose-950/40 border border-rose-500/40 text-xs text-rose-300 text-left flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0" />
              <span>{errorMessage}</span>
            </div>
          )}

          <div className="pt-2">
            <button
              type="button"
              onClick={handleStartSession}
              disabled={isStartingSession || isGeneratingQuestions}
              className="w-full py-4 px-6 rounded-xl bg-gradient-to-r from-sky-600 to-indigo-600 hover:from-sky-500 hover:to-indigo-500 text-white font-bold text-base shadow-lg shadow-sky-600/30 transition flex items-center justify-center gap-2 disabled:opacity-50 cursor-pointer"
            >
              {isStartingSession || isGeneratingQuestions ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>Preparing AI Questions...</span>
                </>
              ) : (
                <>
                  <Play className="w-5 h-5 fill-current" />
                  <span>Start Interview Now</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    );
  }

  // In-Progress State: If questions are missing, generate them
  if (questions.length === 0) {
    return (
      <div className="max-w-xl mx-auto py-16 text-center space-y-5">
        <div className="p-4 rounded-2xl bg-sky-500/10 border border-sky-500/20 text-sky-400 inline-flex">
          <Sparkles className="w-8 h-8 animate-pulse" />
        </div>
        <h2 className="text-xl font-bold text-white">Generating Tailored Questions</h2>
        <p className="text-sm text-slate-400">
          Our AI is constructing personalized interview questions matching your role, experience level, and difficulty.
        </p>

        {errorMessage && (
          <div className="p-3.5 rounded-xl bg-rose-950/40 border border-rose-500/40 text-xs text-rose-300 text-left flex items-center gap-2">
            <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0" />
            <span>{errorMessage}</span>
          </div>
        )}

        <div className="pt-2">
          <button
            type="button"
            onClick={handleGenerateQuestions}
            disabled={isGeneratingQuestions}
            className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs transition cursor-pointer"
          >
            {isGeneratingQuestions ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                <span>Generating...</span>
              </>
            ) : (
              <span>Retry Generation</span>
            )}
          </button>
        </div>
      </div>
    );
  }

  const currentQuestion = questions[currentIndex];
  const initialAnswerForCurrent = currentQuestion ? responsesMap[currentQuestion.id] || "" : "";
  const isLast = currentIndex === questions.length - 1;

  return (
    <div className="max-w-4xl mx-auto py-4 space-y-6">
      {/* Session Breadcrumbs & Header */}
      <div className="flex items-center justify-between">
        <Link
          href="/interview"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-400 hover:text-slate-200 transition"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Exit to Dashboard</span>
        </Link>

        <div className="flex items-center gap-3 text-xs">
          <span className="text-slate-400 flex items-center gap-1">
            <Briefcase className="w-3.5 h-3.5 text-slate-500" />
            <span className="font-semibold text-white">{session.target_role}</span>
          </span>
          <span className="text-slate-600">•</span>
          <span className="text-slate-400 flex items-center gap-1">
            <Layers className="w-3.5 h-3.5 text-slate-500" />
            <span>{session.interview_type}</span>
          </span>
        </div>
      </div>

      {/* Error alert if any */}
      {errorMessage && (
        <div className="p-4 rounded-xl bg-rose-950/40 border border-rose-500/40 flex items-center gap-3 text-xs text-rose-300">
          <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0" />
          <span>{errorMessage}</span>
        </div>
      )}

      {/* Active Question Display */}
      {currentQuestion && (
        <InterviewQuestion
          key={currentQuestion.id}
          question={currentQuestion}
          questionNumber={currentIndex + 1}
          totalQuestions={questions.length}
          initialAnswer={initialAnswerForCurrent}
          isSubmitting={isSubmittingAnswer || isCompletingSession}
          isLastQuestion={isLast}
          canGoPrevious={currentIndex > 0}
          canGoNext={currentIndex < questions.length - 1}
          answerMode={session.answer_mode}
          onPreviousQuestion={handlePreviousQuestion}
          onNextQuestion={handleNextQuestion}
          onSubmitAnswer={handleSubmitAnswer}
          onFinishInterview={handleFinishInterview}
        />
      )}
    </div>
  );
}
