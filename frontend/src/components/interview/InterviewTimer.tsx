"use client";

import React, { useState, useEffect } from "react";
import { Clock, AlertTriangle } from "lucide-react";

interface InterviewTimerProps {
  totalMinutes: number;
  onTimeExpired?: () => void;
}

export default function InterviewTimer({
  totalMinutes,
  onTimeExpired,
}: InterviewTimerProps) {
  const [remainingSeconds, setRemainingSeconds] = useState(totalMinutes * 60);

  useEffect(() => {
    const interval = setInterval(() => {
      setRemainingSeconds((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          if (onTimeExpired) onTimeExpired();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [onTimeExpired]);

  const mins = Math.floor(remainingSeconds / 60);
  const secs = remainingSeconds % 60;
  const isLowTime = remainingSeconds < 180; // under 3 minutes

  return (
    <div
      className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border text-sm font-mono font-medium ${
        isLowTime
          ? "bg-rose-950/60 border-rose-800 text-rose-300 animate-pulse"
          : "bg-slate-900 border-slate-800 text-slate-300"
      }`}
    >
      {isLowTime ? (
        <AlertTriangle className="w-4 h-4 text-rose-400" />
      ) : (
        <Clock className="w-4 h-4 text-sky-400" />
      )}
      <span>
        {mins}:{secs < 10 ? "0" : ""}{secs}
      </span>
    </div>
  );
}
