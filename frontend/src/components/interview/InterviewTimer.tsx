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
      className={`flex items-center gap-2 px-3 py-1.5 rounded-xl border text-xs font-mono font-semibold transition ${
        isLowTime
          ? "bg-rose-50 border-rose-200 text-rose-600 animate-pulse"
          : "bg-[#F1F3F6] border-[#E5E9EF] text-[#123E63]"
      }`}
    >
      {isLowTime ? (
        <AlertTriangle className="w-3.5 h-3.5 text-rose-500" />
      ) : (
        <Clock className="w-3.5 h-3.5 text-[#F5A623]" />
      )}
      <span>
        {mins}:{secs < 10 ? "0" : ""}{secs}
      </span>
    </div>
  );
}