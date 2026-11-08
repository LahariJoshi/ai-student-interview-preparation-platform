"use client";

import React, { useState } from "react";
import Link from "next/link";
import { ProgressChartData } from "@/types/dashboard";

interface BarDataPoint {
  label: string;
  navy: number; // technical/coding assessment score on 0-50 scale
  orange: number; // mock interview score on 0-50 scale
  peak?: boolean;
  peakValue?: string;
  codingCount?: number;
  interviewCount?: number;
}

interface PreparationProgressChartProps {
  data?: ProgressChartData | null;
  isLoading?: boolean;
  onCheckNow?: () => void;
}

export default function PreparationProgressChart({
  data,
  isLoading,
  onCheckNow,
}: PreparationProgressChartProps) {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  // Map incoming dynamic periods if available
  const barData: BarDataPoint[] = data && data.periods && data.periods.length > 0
    ? data.periods.map((p) => ({
        label: p.label,
        navy: p.coding_score,
        orange: p.interview_score,
        peak: p.peak,
        peakValue: p.peak_value || `${Math.round(p.coding_score + p.interview_score)}`,
        codingCount: p.coding_submissions_count,
        interviewCount: p.interview_sessions_count,
      }))
    : [
        { label: "W1", navy: 0, orange: 0 },
        { label: "W2", navy: 0, orange: 0 },
        { label: "W3", navy: 0, orange: 0 },
        { label: "W4", navy: 0, orange: 0 },
        { label: "W5", navy: 0, orange: 0 },
        { label: "W6", navy: 0, orange: 0 },
        { label: "W7", navy: 0, orange: 0 },
        { label: "W8", navy: 0, orange: 0 },
      ];

  const yTicks = [50, 40, 30, 20, 10];
  const hasAnyActivity = barData.some((b) => b.navy > 0 || b.orange > 0);

  return (
    <div className="bg-white rounded-2xl p-5 sm:p-6 shadow-card border border-[#E5E9EF] flex flex-col justify-between">
      {/* Top Header Row with Title and Accent Orange 'Check Now' Button */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-base sm:text-lg font-bold text-[#202B38] tracking-tight">
            Preparation Progress
          </h3>
          <p className="text-xs text-[#8993A0]">
            Performance comparison across verified assessment periods
          </p>
        </div>

        <Link
          href="/dashboard"
          onClick={onCheckNow}
          className="px-4 py-1.5 rounded-full bg-[#F5A623] hover:bg-[#E09212] text-white text-xs font-semibold shadow-sm transition-all flex items-center gap-1"
        >
          <span>Check Now</span>
        </Link>
      </div>

      {/* Main Chart Area */}
      <div className="relative w-full pt-4 pb-2">
        {isLoading ? (
          <div className="h-[180px] flex items-center justify-center text-xs text-[#8993A0] animate-pulse">
            Loading assessment telemetry...
          </div>
        ) : (
          <div className="flex items-start">
            {/* Y-Axis Labels */}
            <div className="flex flex-col justify-between h-[180px] text-[10px] text-[#8993A0] pr-3 select-none pb-5">
              {yTicks.map((tick) => (
                <span key={tick}>{tick}</span>
              ))}
            </div>

            {/* Chart Graphic Area */}
            <div className="relative flex-1 h-[180px] pb-6 flex flex-col justify-between">
              {/* Background Grid Lines */}
              <div className="absolute inset-x-0 top-0 bottom-6 flex flex-col justify-between pointer-events-none">
                {yTicks.map((tick) => (
                  <div
                    key={tick}
                    className="w-full border-b border-[#E5E9EF] opacity-75"
                  />
                ))}
              </div>

              {/* Bars Container */}
              <div className="relative z-10 h-full flex items-end justify-between px-2 sm:px-4">
                {barData.map((item, idx) => {
                  const navyHeight = Math.min(100, (item.navy / 50) * 100);
                  const orangeHeight = Math.min(100, (item.orange / 50) * 100);
                  const isHovered = hoveredIndex === idx;

                  return (
                    <div
                      key={item.label}
                      className="relative flex flex-col items-center h-full justify-end group cursor-pointer"
                      onMouseEnter={() => setHoveredIndex(idx)}
                      onMouseLeave={() => setHoveredIndex(null)}
                    >
                      {/* Hover Tooltip or Peak Banner */}
                      {(item.peak || isHovered) && (
                        <div className="absolute -top-7 z-20 flex flex-col items-center animate-fade-in pointer-events-none">
                          <div className="bg-[#09253F] text-white text-[10px] font-bold px-2 py-0.5 rounded shadow-md whitespace-nowrap">
                            {isHovered
                              ? `Coding: ${item.navy} | Mock: ${item.orange}`
                              : item.peakValue}
                          </div>
                          <div className="w-0 h-0 border-x-4 border-x-transparent border-t-4 border-t-[#09253F]" />
                        </div>
                      )}

                      {/* Bars pair: Navy and Orange */}
                      <div className="flex items-end gap-1 sm:gap-1.5 h-full pb-0.5">
                        {/* Deep Navy Bar (Technical Coding) */}
                        <div
                          style={{ height: `${navyHeight > 0 ? Math.max(navyHeight, 4) : 0}%` }}
                          className={`w-2 sm:w-3 md:w-3.5 bg-[#123E63] rounded-t-sm transition-all duration-300 ${
                            isHovered ? "brightness-125" : ""
                          }`}
                        />
                        {/* Vibrant Orange Bar (Mock Interview) */}
                        <div
                          style={{ height: `${orangeHeight > 0 ? Math.max(orangeHeight, 4) : 0}%` }}
                          className={`w-2 sm:w-3 md:w-3.5 bg-[#F5A623] rounded-t-sm transition-all duration-300 ${
                            isHovered ? "brightness-110" : ""
                          }`}
                        />
                      </div>

                      {/* X-Axis Period Label */}
                      <span className="absolute -bottom-5 text-[9px] sm:text-[10px] font-medium text-[#8993A0] uppercase group-hover:text-[#123E63]">
                        {item.label}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* Legend */}
            <div className="hidden sm:flex flex-col gap-2.5 pl-4 justify-center text-[11px] text-[#8993A0] shrink-0 border-l border-[#E5E9EF] my-auto">
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-sm bg-[#123E63] shadow-sm" />
                <span className="font-medium text-[#202B38]">Technical</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-sm bg-[#F5A623] shadow-sm" />
                <span className="font-medium text-[#202B38]">Mock Prep</span>
              </div>
            </div>
          </div>
        )}

        {!hasAnyActivity && !isLoading && (
          <p className="text-center text-[11px] text-[#8993A0] mt-4 pt-2 border-t border-[#E5E9EF]">
            Complete coding assessments and mock interviews to track your preparation across weekly periods.
          </p>
        )}
      </div>
    </div>
  );
}
