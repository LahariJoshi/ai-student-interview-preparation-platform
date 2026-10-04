"use client";

import React, { useEffect, useState, useCallback } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import { InterviewResultData } from "@/types/interview";
import InterviewResult from "@/components/interview/InterviewResult";
import {
  Loader2,
  AlertCircle,
  ArrowLeft,
  RotateCcw,
  Sparkles,
  Award,
} from "lucide-react";

export default function InterviewResultPage() {
  const { id } = useParams() as { id: string };
  const { user, isLoading: isAuthLoading } = useAuth();
  const router = useRouter();

  const [result, setResult] = useState<InterviewResultData | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const loadResult = useCallback(async () => {
    if (!id || !user) return;
    try {
      setIsLoading(true);
      setErrorMessage(null);

      const data = await apiFetch<InterviewResultData>(`/interview/sessions/${id}/result`);
      setResult(data);
    } catch (err: any) {
      setErrorMessage(err.message || "Failed to load interview evaluation results.");
    } finally {
      setIsLoading(false);
    }
  }, [id, user]);

  useEffect(() => {
    if (user) {
      loadResult();
    }
  }, [user, loadResult]);

  // Loading State
  if (isAuthLoading || isLoading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-3">
        <Loader2 className="w-8 h-8 animate-spin text-sky-400" />
        <p className="text-sm text-slate-400">Loading interview results & AI performance metrics...</p>
      </div>
    );
  }

  // Error State
  if (errorMessage) {
    return (
      <div className="max-w-xl mx-auto py-16 text-center space-y-4">
        <div className="w-12 h-12 rounded-full bg-rose-500/10 text-rose-400 flex items-center justify-center mx-auto border border-rose-500/20">
          <AlertCircle className="w-6 h-6" />
        </div>
        <h2 className="text-xl font-bold text-white">Evaluation Report Unavailable</h2>
        <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">
          {errorMessage}
        </p>
        <div className="flex items-center justify-center gap-3 pt-2">
          <button
            type="button"
            onClick={loadResult}
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-sky-500 text-slate-950 font-bold text-xs hover:bg-sky-400 transition cursor-pointer"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Try Again</span>
          </button>
          <Link
            href="/interview"
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-slate-800 text-slate-300 font-semibold text-xs hover:bg-slate-700 transition"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Return to Hub</span>
          </Link>
        </div>
      </div>
    );
  }

  // Empty State (Result not found or not returned)
  if (!result) {
    return (
      <div className="max-w-xl mx-auto py-16 text-center space-y-4">
        <div className="w-12 h-12 rounded-full bg-slate-800 text-slate-400 flex items-center justify-center mx-auto">
          <Award className="w-6 h-6" />
        </div>
        <h2 className="text-xl font-bold text-white">Interview Result Not Found</h2>
        <p className="text-xs sm:text-sm text-slate-400">
          We could not find performance records for this interview session.
        </p>
        <div className="pt-2">
          <Link
            href="/interview"
            className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-slate-800 text-slate-300 font-semibold text-xs hover:bg-slate-700 transition"
          >
            <ArrowLeft className="w-3.5 h-3.5" />
            <span>Back to Interview Hub</span>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto py-8 px-4 sm:px-6 space-y-6">
      {/* Breadcrumb Navigation */}
      <div className="flex items-center justify-between text-xs text-slate-400 pb-2 border-b border-slate-800/80">
        <div className="flex items-center gap-2">
          <Link href="/interview" className="hover:text-slate-200 transition">
            Interview Hub
          </Link>
          <span>/</span>
          <span className="text-slate-200 font-medium">Session Results</span>
        </div>

        <Link
          href="/interview"
          className="inline-flex items-center gap-1.5 text-slate-400 hover:text-white transition font-medium"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          <span>Exit to Hub</span>
        </Link>
      </div>

      {/* Main Result Component */}
      <InterviewResult result={result} />
    </div>
  );
}
