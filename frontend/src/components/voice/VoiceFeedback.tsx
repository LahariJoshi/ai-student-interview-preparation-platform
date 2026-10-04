"use client";

import React from "react";
import { MessageSquareText, ShieldCheck, Sparkles, AlertCircle, Info } from "lucide-react";

interface VoiceFeedbackProps {
  feedbackList: string[];
  communicationScore?: number;
  className?: string;
}

export default function VoiceFeedback({
  feedbackList,
  communicationScore,
  className = "",
}: VoiceFeedbackProps) {
  if (!feedbackList || feedbackList.length === 0) {
    return (
      <div className={`p-6 rounded-2xl bg-slate-900 border border-slate-800 text-center space-y-2 ${className}`}>
        <div className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center mx-auto text-slate-400">
          <MessageSquareText className="w-5 h-5" />
        </div>
        <h4 className="text-sm font-semibold text-white">No Delivery Feedback Available</h4>
        <p className="text-xs text-slate-400 max-w-md mx-auto">
          Detailed delivery coaching feedback is generated when candidates respond via audio recording mode.
        </p>
      </div>
    );
  }

  // Filter out coaching disclaimer paragraph to render it in a specialized callout
  const isDisclaimer = (text: string) => text.toLowerCase().includes("communication coaching note");
  const mainFeedbacks = feedbackList.filter((fb) => !isDisclaimer(fb));
  const disclaimer = feedbackList.find(isDisclaimer);

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Qualitative Feedback Cards */}
      <div className="space-y-3">
        {mainFeedbacks.map((paragraph, index) => {
          // Identify category title if present in text (e.g., "Pacing Rationale:", "Verbal Economy:")
          const parts = paragraph.split(":");
          const hasPrefix = parts.length > 1 && parts[0].length < 30;

          return (
            <div
              key={index}
              className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-1.5 transition hover:border-slate-700"
            >
              {hasPrefix ? (
                <>
                  <div className="flex items-center gap-2 text-xs font-bold text-sky-400">
                    <Sparkles className="w-3.5 h-3.5" />
                    <span>{parts[0].trim()}</span>
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed">
                    {parts.slice(1).join(":").trim()}
                  </p>
                </>
              ) : (
                <p className="text-xs text-slate-300 leading-relaxed flex items-start gap-2">
                  <span className="text-sky-400 font-bold shrink-0">•</span>
                  <span>{paragraph}</span>
                </p>
              )}
            </div>
          );
        })}
      </div>

      {/* Mandatory Ethical & Pedagogical Coaching Callout */}
      {disclaimer ? (
        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-400 space-y-1.5">
          <div className="flex items-center gap-2 text-slate-300 font-semibold">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>Ethical Delivery Coaching Standard</span>
          </div>
          <p className="text-[11px] leading-relaxed text-slate-400">
            {disclaimer.replace(/^communication coaching note:\s*/i, "")}
          </p>
        </div>
      ) : (
        <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-400 space-y-1.5">
          <div className="flex items-center gap-2 text-slate-300 font-semibold">
            <Info className="w-4 h-4 text-sky-400" />
            <span>Coaching Note</span>
          </div>
          <p className="text-[11px] leading-relaxed text-slate-400">
            Voice metrics analyze vocal pacing and clarity of articulation as an educational practice tool. They should always be evaluated alongside technical depth and problem-solving reasoning.
          </p>
        </div>
      )}
    </div>
  );
}
