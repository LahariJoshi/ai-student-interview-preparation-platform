"use client";

import React, { useState } from "react";
import Link from "next/link";
import { ArrowUpRight } from "lucide-react";

interface BarDataPoint {
  label: string;
  navy: number; // e.g., technical assessment score 0-50 scale
  orange: number; // e.g., mock interview score 0-50 scale
  peak?: boolean;
  peakValue?: string;
}

interface PreparationProgressChartProps {
  onCheckNow?: () => void;
}

export default function PreparationProgressChart({ onCheckNow }: PreparationProgressChartProps) {
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null);

  // 9 periods exactly matching the reference image layout:
  // JAN, FEB, MAR, APR, MAY, JUNE, JULY, AUG, SEP
  // JUNE has the peak bar with the dark navy tooltip banner "28.79" (or 45.8)
  const data: BarDataPoint[] = [
    { label: "JAN", navy: 20, orange: 28 },
    { label: "FEB", navy: 35, orange: 22 },
    { label: "MAR", navy: 40, orange: 26 },
    { label: "APR", navy: 32, orange: 24 },
    { label: "MAY", navy: 12, orange: 34 },
    { label: "JUNE", navy: 46, orange: 23, peak: true, peakValue: "28.79" },
    { label: "JULY", navy: 18, orange: 35 },
    { label: "AUG", navy: 21, orange: 22 },
    { label: "SEP", navy: 20, orange: 33 },
  ];

  const yTicks = [50, 40, 30, 20, 10];

  return (
    <div className="bg-white rounded-2xl p-5 sm:p-6 shadow-card border border-[#E5E9EF] flex flex-col justify-between">
      {/* Top Header Row with Title and Accent Orange 'Check Now' Button */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-base sm:text-lg font-bold text-[#202B38] tracking-tight">
            Preparation Progress
          </h3>
          <p className="text-xs text-[#8993A0]">
            Performance comparison across assessment periods
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
              {data.map((item, idx) => {
                const navyHeight = (item.navy / 50) * 100;
                const orangeHeight = (item.orange / 50) * 100;
                const isHovered = hoveredIndex === idx;

                return (
                  <div
                    key={item.label}
                    className="relative flex flex-col items-center h-full justify-end group cursor-pointer"
                    onMouseEnter={() => setHoveredIndex(idx)}
                    onMouseLeave={() => setHoveredIndex(null)}
                  >
                    {/* Hover Tooltip or Peak Banner (Matching Reference Image Dark Pill) */}
                    {(item.peak || isHovered) && (
                      <div className="absolute -top-7 z-20 flex flex-col items-center animate-fade-in">
                        <div className="bg-[#09253F] text-white text-[10px] font-bold px-2 py-0.5 rounded shadow-md whitespace-nowrap">
                          {isHovered ? `Tech: ${item.navy} | Mock: ${item.orange}` : item.peakValue}
                        </div>
                        <div className="w-0 h-0 border-x-4 border-x-transparent border-t-4 border-t-[#09253F]" />
                      </div>
                    )}

                    {/* Bars pair: Navy and Orange */}
                    <div className="flex items-end gap-1 sm:gap-1.5 h-full pb-0.5">
                      {/* Deep Navy Bar */}
                      <div
                        style={{ height: `${navyHeight}%` }}
                        className={`w-2 sm:w-3 md:w-3.5 bg-[#123E63] rounded-t-sm transition-all duration-300 ${
                          isHovered ? "brightness-125" : ""
                        }`}
                      />
                      {/* Vibrant Orange Bar */}
                      <div
                        style={{ height: `${orangeHeight}%` }}
                        className={`w-2 sm:w-3 md:w-3.5 bg-[#F5A623] rounded-t-sm transition-all duration-300 ${
                          isHovered ? "brightness-110" : ""
                        }`}
                      />
                    </div>

                    {/* X-Axis Month Label */}
                    <span className="absolute -bottom-5 text-[9px] sm:text-[10px] font-medium text-[#8993A0] uppercase group-hover:text-[#123E63]">
                      {item.label}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Legend (Right side, matching 2019 / 2020 tags from reference image) */}
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
      </div>
    </div>
  );
}
