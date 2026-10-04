"use client";

import React from "react";
import {
  Mic,
  Gauge,
  MessageSquare,
  Clock,
  Volume2,
  Sparkles,
  Info,
} from "lucide-react";
import { AggregateVoiceMetrics } from "@/types/interview";

interface VoiceMetricsProps {
  metrics: AggregateVoiceMetrics;
  className?: string;
}

export default function VoiceMetrics({ metrics, className = "" }: VoiceMetricsProps) {
  if (!metrics.has_voice_data) {
    return (
      <div className={`p-6 rounded-2xl bg-slate-900 border border-slate-800 text-center space-y-2 ${className}`}>
        <div className="w-10 h-10 rounded-full bg-slate-800 flex items-center justify-center mx-auto text-slate-400">
          <Mic className="w-5 h-5" />
        </div>
        <h4 className="text-sm font-semibold text-white">No Voice Telemetry Recorded</h4>
        <p className="text-xs text-slate-400 max-w-md mx-auto">
          This session was conducted via written responses. Voice metrics, pacing cadence, and filler-word detection are generated during audio response mode.
        </p>
      </div>
    );
  }

  const {
    average_speaking_rate_wpm,
    total_filler_word_count,
    filler_words_detected,
    average_clarity_score,
    total_pause_count,
    total_pause_duration_seconds,
    tone_evaluation,
  } = metrics;

  // Pace Classification
  const getPaceStatus = (wpm: number) => {
    if (wpm >= 120 && wpm <= 160) {
      return { label: "Optimal Cadence", color: "text-emerald-400 bg-emerald-500/10 border-emerald-500/30" };
    }
    if (wpm > 160) {
      return { label: "Fast Paced", color: "text-amber-400 bg-amber-500/10 border-amber-500/30" };
    }
    if (wpm > 0) {
      return { label: "Measured / Slow", color: "text-sky-400 bg-sky-500/10 border-sky-500/30" };
    }
    return { label: "Unavailable", color: "text-slate-400 bg-slate-800 border-slate-700" };
  };

  // Filler Status
  const getFillerStatus = (count: number) => {
    if (count <= 2) {
      return { label: "Exceptional Economy", color: "text-emerald-400" };
    }
    if (count <= 6) {
      return { label: "Moderate Crutches", color: "text-amber-400" };
    }
    return { label: "Frequent Fillers", color: "text-rose-400" };
  };

  const paceStatus = getPaceStatus(average_speaking_rate_wpm);
  const fillerStatus = getFillerStatus(total_filler_word_count);

  return (
    <div className={`space-y-4 ${className}`}>
      {/* Metric Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Speaking Pace Card */}
        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span className="font-semibold flex items-center gap-1.5">
              <Gauge className="w-4 h-4 text-sky-400" />
              Speaking Pace
            </span>
            <span className={`px-2 py-0.5 rounded-full text-[10px] font-semibold border ${paceStatus.color}`}>
              {paceStatus.label}
            </span>
          </div>
          <div className="flex items-baseline gap-1.5">
            <span className="text-2xl font-bold text-white">{average_speaking_rate_wpm}</span>
            <span className="text-xs text-slate-400 font-medium">WPM</span>
          </div>
          <p className="text-[11px] text-slate-400">
            Recommended interview baseline is 120–160 words per minute.
          </p>
        </div>

        {/* Filler Words Card */}
        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span className="font-semibold flex items-center gap-1.5">
              <MessageSquare className="w-4 h-4 text-amber-400" />
              Filler Words
            </span>
            <span className={`text-[11px] font-semibold ${fillerStatus.color}`}>
              {fillerStatus.label}
            </span>
          </div>
          <div className="flex items-baseline gap-1.5">
            <span className="text-2xl font-bold text-white">{total_filler_word_count}</span>
            <span className="text-xs text-slate-400 font-medium">detected</span>
          </div>
          <p className="text-[11px] text-slate-400">
            Includes verbal bridges such as &ldquo;um&rdquo;, &ldquo;like&rdquo;, and &ldquo;basically&rdquo;.
          </p>
        </div>

        {/* Pause Cadence Card */}
        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span className="font-semibold flex items-center gap-1.5">
              <Clock className="w-4 h-4 text-indigo-400" />
              Pause Spacing
            </span>
            <span className="text-[10px] font-semibold text-slate-400 bg-slate-800 px-2 py-0.5 rounded-full">
              {total_pause_count} pauses
            </span>
          </div>
          <div className="flex items-baseline gap-1.5">
            <span className="text-2xl font-bold text-white">{total_pause_duration_seconds}</span>
            <span className="text-xs text-slate-400 font-medium">sec total</span>
          </div>
          <p className="text-[11px] text-slate-400">
            Transitional silent spaces allow thoughts to structure naturally.
          </p>
        </div>

        {/* Clarity & Tone Card */}
        <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span className="font-semibold flex items-center gap-1.5">
              <Volume2 className="w-4 h-4 text-emerald-400" />
              Delivery Clarity
            </span>
            {tone_evaluation && (
              <span className="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                {tone_evaluation}
              </span>
            )}
          </div>
          <div className="flex items-baseline gap-1.5">
            <span className="text-2xl font-bold text-emerald-400">{average_clarity_score}</span>
            <span className="text-xs text-slate-400 font-medium">/ 100</span>
          </div>
          <p className="text-[11px] text-slate-400">
            Normalized articulation, pacing, and verbal clarity rating.
          </p>
        </div>
      </div>

      {/* Filler Words Breakdown Pill List */}
      {Object.keys(filler_words_detected).length > 0 && (
        <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-2.5">
          <div className="flex items-center gap-2 text-xs font-semibold text-slate-300">
            <Sparkles className="w-3.5 h-3.5 text-amber-400" />
            <span>Detected Filler Crutches Breakdown:</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {Object.entries(filler_words_detected)
              .sort((a, b) => b[1] - a[1])
              .map(([word, count]) => (
                <span
                  key={word}
                  className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs bg-slate-900 border border-slate-700 text-slate-200"
                >
                  <strong className="text-amber-300">&ldquo;{word}&rdquo;</strong>
                  <span className="text-slate-400 text-[11px] font-mono">({count}x)</span>
                </span>
              ))}
          </div>
        </div>
      )}
    </div>
  );
}
