"use client";

import React from "react";
import { Calendar as CalendarIcon, ChevronLeft, ChevronRight } from "lucide-react";
import { SkillDevelopmentData } from "@/types/dashboard";

interface SkillDevelopmentChartProps {
  data?: SkillDevelopmentData | null;
  isLoading?: boolean;
}

/**
 * Generate smooth SVG path string from an array of 4 score values (0-100).
 * Maps scores to viewBox 0 0 400 140.
 */
function generateSplinePath(scores: number[], isArea: boolean = false): string {
  // Safe default if scores array is missing or incomplete
  const safeScores = [
    scores[0] ?? 0,
    scores[1] ?? 0,
    scores[2] ?? 0,
    scores[3] ?? 0,
  ];

  // Map 0-100 to y coordinate: 0 -> 130 (near bottom), 100 -> 25 (near top)
  const toY = (val: number) => {
    const clamped = Math.max(0, Math.min(100, val));
    return 130 - (clamped / 100) * 105;
  };

  const p0 = { x: 0, y: toY(safeScores[0]) };
  const p1 = { x: 133, y: toY(safeScores[1]) };
  const p2 = { x: 266, y: toY(safeScores[2]) };
  const p3 = { x: 400, y: toY(safeScores[3]) };

  // Control points for cubic bezier curves
  const c1x = p0.x + (p1.x - p0.x) * 0.5;
  const c2x = p1.x - (p2.x - p0.x) * 0.2;
  const c3x = p1.x + (p2.x - p0.x) * 0.2;
  const c4x = p2.x - (p3.x - p1.x) * 0.2;
  const c5x = p2.x + (p3.x - p1.x) * 0.2;
  const c6x = p3.x - (p3.x - p2.x) * 0.5;

  const curve = `M ${p0.x} ${p0.y} C ${c1x} ${p0.y}, ${c2x} ${p1.y}, ${p1.x} ${p1.y} C ${c3x} ${p1.y}, ${c4x} ${p2.y}, ${p2.x} ${p2.y} C ${c5x} ${p2.y}, ${c6x} ${p3.y}, ${p3.x} ${p3.y}`;

  if (isArea) {
    return `${curve} L 400 140 L 0 140 Z`;
  }
  return curve;
}

export default function SkillDevelopmentChart({
  data,
  isLoading,
}: SkillDevelopmentChartProps) {
  const weekdays = ["S", "M", "T", "W", "T", "F", "S"];

  // 1. Weekly trendlines data
  const weeks = data?.weeks || [];
  const codingScores = weeks.map((w) => w.coding_proficiency);
  const interviewScores = weeks.map((w) => w.interview_fluency);

  const navyAreaPath = generateSplinePath(interviewScores, true);
  const navyLinePath = generateSplinePath(interviewScores, false);
  const orangeAreaPath = generateSplinePath(codingScores, true);
  const orangeLinePath = generateSplinePath(codingScores, false);

  const hasActivity =
    codingScores.some((s) => s > 0) || interviewScores.some((s) => s > 0);

  // 2. Calendar grid calculation
  const calendarInfo = data?.calendar;
  const monthName = calendarInfo?.month_name || "Current Month";
  const year = calendarInfo?.year || 2026;
  const daysInMonth = calendarInfo?.days_in_month || 30;

  // Convert Python Monday=0..Sunday=6 to Sunday=0..Saturday=6
  const pyFirstWeekday = calendarInfo?.first_weekday ?? 6;
  const sundayBasedFirstDay = (pyFirstWeekday + 1) % 7;

  // Create active days map for quick lookup: day -> activity
  const activeMap = new Map<number, { type: string; coding: number; interview: number }>();
  if (calendarInfo?.active_days) {
    calendarInfo.active_days.forEach((ad) => {
      activeMap.set(ad.day, {
        type: ad.activity_type,
        coding: ad.coding_count,
        interview: ad.interview_count,
      });
    });
  }

  // Construct calendar cells
  interface DayCell {
    day: number | "";
    empty: boolean;
    activity?: { type: string; coding: number; interview: number };
  }

  const calendarDays: DayCell[] = [];
  for (let i = 0; i < sundayBasedFirstDay; i++) {
    calendarDays.push({ day: "", empty: true });
  }
  for (let d = 1; d <= daysInMonth; d++) {
    calendarDays.push({
      day: d,
      empty: false,
      activity: activeMap.get(d),
    });
  }

  return (
    <div className="bg-white rounded-2xl p-5 sm:p-6 shadow-card border border-[#E5E9EF] grid grid-cols-1 md:grid-cols-12 gap-6">
      {/* LEFT PART: Smooth Wave Area Chart (~60% width) */}
      <div className="md:col-span-7 flex flex-col justify-between">
        {/* Legend */}
        <div className="flex items-center gap-4 mb-2">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-[#F5A623]" />
            <span className="text-xs font-semibold text-[#202B38]">
              Coding Proficiency
            </span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-[#123E63]" />
            <span className="text-xs font-semibold text-[#202B38]">
              Interview Fluency
            </span>
          </div>
        </div>

        {/* Dynamic Dual Smooth Wave Chart */}
        <div className="relative w-full h-[140px] sm:h-[150px] mt-2">
          {isLoading ? (
            <div className="w-full h-full flex items-center justify-center text-xs text-[#8993A0] animate-pulse">
              Computing skill curves...
            </div>
          ) : (
            <svg
              className="w-full h-full overflow-visible"
              viewBox="0 0 400 140"
              preserveAspectRatio="none"
            >
              <defs>
                {/* Navy Gradient for Interview Fluency */}
                <linearGradient id="navyWaveGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#123E63" stopOpacity="0.45" />
                  <stop offset="100%" stopColor="#123E63" stopOpacity="0.0" />
                </linearGradient>

                {/* Orange Gradient for Coding Proficiency */}
                <linearGradient id="orangeWaveGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#F5A623" stopOpacity="0.60" />
                  <stop offset="100%" stopColor="#F5A623" stopOpacity="0.05" />
                </linearGradient>
              </defs>

              {/* Back Wave: Navy Area Curve (Interview Fluency) */}
              <path
                d={navyAreaPath}
                fill="url(#navyWaveGrad)"
                className="transition-all duration-700 ease-in-out"
              />
              <path
                d={navyLinePath}
                fill="none"
                stroke="#123E63"
                strokeWidth="2.5"
                className="transition-all duration-700 ease-in-out"
              />

              {/* Front Wave: Orange Area Curve (Coding Proficiency) */}
              <path
                d={orangeAreaPath}
                fill="url(#orangeWaveGrad)"
                className="transition-all duration-700 ease-in-out"
              />
              <path
                d={orangeLinePath}
                fill="none"
                stroke="#F5A623"
                strokeWidth="2.5"
                className="transition-all duration-700 ease-in-out"
              />
            </svg>
          )}
        </div>

        {/* X-Axis Weekly Labels */}
        <div className="flex justify-between items-center text-[10px] text-[#8993A0] mt-1 pt-1 border-t border-[#E5E9EF]">
          {weeks.length > 0 ? (
            weeks.map((w, i) => <span key={i}>{w.label}</span>)
          ) : (
            <>
              <span>Week 1</span>
              <span>Week 2</span>
              <span>Week 3</span>
              <span>Week 4</span>
            </>
          )}
        </div>

        {!hasActivity && !isLoading && (
          <p className="text-[10px] text-[#8993A0] mt-1 text-center italic">
            Baseline curve shown. Practice questions and interviews will reflect your weekly skill growth.
          </p>
        )}
      </div>

      {/* RIGHT PART: Dynamic Preparation Activity Calendar (~40% width) */}
      <div className="md:col-span-5 md:border-l md:border-[#E5E9EF] md:pl-6 flex flex-col justify-between">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-1.5 text-xs font-bold text-[#202B38]">
            <CalendarIcon className="w-3.5 h-3.5 text-[#123E63]" />
            <span>Target Calendar</span>
          </div>
          <span className="text-[11px] font-semibold text-[#8993A0]">
            {monthName} {year}
          </span>
        </div>

        {/* Days of Week Header */}
        <div className="grid grid-cols-7 text-center text-[10px] font-bold text-[#8993A0] mb-1">
          {weekdays.map((w, i) => (
            <span key={i}>{w}</span>
          ))}
        </div>

        {/* Days Grid */}
        <div className="grid grid-cols-7 gap-y-1 text-center text-[10px]">
          {calendarDays.map((item, idx) => {
            if (item.empty) {
              return <span key={idx} />;
            }

            const act = item.activity;

            // Day with Mock Interview Session (Navy)
            if (act && act.type === "mock_session") {
              return (
                <div
                  key={idx}
                  className="flex justify-center items-center py-0.5"
                  title={`Mock Interviews: ${act.interview}`}
                >
                  <span className="w-5 h-5 rounded-md bg-[#123E63] text-white font-bold flex items-center justify-center shadow-xs">
                    {item.day}
                  </span>
                </div>
              );
            }

            // Day with Coding Practice (Orange)
            if (act && act.type === "coding_practice") {
              return (
                <div
                  key={idx}
                  className="flex justify-center items-center py-0.5"
                  title={`Coding Submissions: ${act.coding}`}
                >
                  <span className="w-5 h-5 rounded-md bg-[#F5A623] text-white font-bold flex items-center justify-center shadow-xs">
                    {item.day}
                  </span>
                </div>
              );
            }

            // Day with Both Coding and Interview (Navy with Orange Ring)
            if (act && act.type === "both") {
              return (
                <div
                  key={idx}
                  className="flex justify-center items-center py-0.5"
                  title={`Coding: ${act.coding} | Interviews: ${act.interview}`}
                >
                  <span className="w-5 h-5 rounded-md bg-[#123E63] text-white font-bold flex items-center justify-center shadow-xs ring-2 ring-[#F5A623]">
                    {item.day}
                  </span>
                </div>
              );
            }

            return (
              <div key={idx} className="flex justify-center items-center py-0.5">
                <span className="text-[#8993A0] hover:text-[#202B38] font-medium transition cursor-default">
                  {item.day}
                </span>
              </div>
            );
          })}
        </div>

        {/* Calendar Key */}
        <div className="flex items-center justify-between text-[10px] text-[#8993A0] pt-2 border-t border-[#E5E9EF] mt-2">
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-sm bg-[#123E63]" /> Mock Session
          </span>
          <span className="flex items-center gap-1">
            <span className="w-2 h-2 rounded-sm bg-[#F5A623]" /> Coding Practice
          </span>
        </div>
      </div>
    </div>
  );
}
