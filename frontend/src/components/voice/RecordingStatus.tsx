"use client";

import React from "react";
import { Mic, MicOff, AlertCircle, CheckCircle2, Play, Square, Pause } from "lucide-react";

export type RecordingState = "idle" | "requesting" | "recording" | "paused" | "recorded" | "error";

interface RecordingStatusProps {
  status: RecordingState;
  durationSeconds: number;
  audioLevel?: number; // 0 to 100
  errorMessage?: string | null;
  className?: string;
}

export function formatTime(seconds: number): string {
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
}

export default function RecordingStatus({
  status,
  durationSeconds,
  audioLevel = 0,
  errorMessage,
  className = "",
}: RecordingStatusProps) {
  return (
    <div className={`flex flex-col items-center justify-center p-4 rounded-2xl bg-slate-900/60 border border-slate-800 ${className}`}>
      {/* Visual Indicator & Badge */}
      <div className="flex items-center gap-3 mb-3">
        {status === "idle" && (
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-800 border border-slate-700 text-xs font-medium text-slate-300">
            <Mic className="w-3.5 h-3.5 text-slate-400" />
            <span>Ready to Record</span>
          </div>
        )}

        {status === "requesting" && (
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-500/10 border border-sky-500/30 text-xs font-medium text-sky-400 animate-pulse">
            <Mic className="w-3.5 h-3.5" />
            <span>Requesting Microphone Permission...</span>
          </div>
        )}

        {status === "recording" && (
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-500/10 border border-rose-500/30 text-xs font-semibold text-rose-400">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500 animate-ping" />
            <span>Recording Live</span>
          </div>
        )}

        {status === "paused" && (
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-xs font-medium text-amber-400">
            <Pause className="w-3.5 h-3.5" />
            <span>Recording Paused</span>
          </div>
        )}

        {status === "recorded" && (
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-xs font-medium text-emerald-400">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Recording Complete</span>
          </div>
        )}

        {status === "error" && (
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-rose-500/10 border border-rose-500/30 text-xs font-medium text-rose-400">
            <AlertCircle className="w-3.5 h-3.5" />
            <span>Microphone Error</span>
          </div>
        )}
      </div>

      {/* Timer Display */}
      <div className="text-3xl font-mono font-bold tracking-wider text-white mb-2">
        {formatTime(durationSeconds)}
      </div>

      {/* Live Audio Level Waveform (while recording) */}
      {status === "recording" && (
        <div className="flex items-center gap-1.5 h-10 px-4 py-1.5 rounded-xl bg-slate-950/60 border border-slate-800/80 my-2">
          {Array.from({ length: 16 }).map((_, i) => {
            // Generate dynamic waveform bars scaled by audioLevel and index
            const waveModifier = Math.sin((i / 16) * Math.PI);
            const heightPercent = Math.max(
              15,
              Math.min(100, Math.round((audioLevel || 20) * waveModifier * (0.8 + 0.4 * Math.random())))
            );
            return (
              <span
                key={i}
                className="w-1 bg-gradient-to-t from-rose-500 to-amber-400 rounded-full transition-all duration-75"
                style={{ height: `${heightPercent}%` }}
              />
            );
          })}
        </div>
      )}

      {/* Error Message banner */}
      {status === "error" && errorMessage && (
        <div className="mt-2 text-xs text-rose-400 bg-rose-950/30 border border-rose-500/20 px-3 py-1.5 rounded-lg text-center max-w-sm">
          {errorMessage}
        </div>
      )}
    </div>
  );
}
