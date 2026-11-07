"use client";

import React from "react";
import { Calendar as CalendarIcon, ChevronLeft, ChevronRight } from "lucide-react";

export default function SkillDevelopmentChart() {
  // Calendar days grid calculation for current month
  const weekdays = ["S", "M", "T", "W", "T", "F", "S"];
  
  // Sample month representation matching reference layout
  // Days 1 through 31, with highlight markers
  const calendarDays = [
    { day: "", empty: true },
    { day: "", empty: true },
    { day: "1" },
    { day: "2" },
    { day: "3" },
    { day: "4" },
    { day: "5" },
    { day: "6" },
    { day: "7" },
    { day: "8" },
    { day: "9" },
    { day: "10", active: "navy" }, // Mock Interview scheduled
    { day: "11" },
    { day: "12" },
    { day: "13" },
    { day: "14" },
    { day: "15" },
    { day: "16" },
    { day: "17" },
    { day: "18", active: "navy" }, // Coding contest
    { day: "19" },
    { day: "20" },
    { day: "21" },
    { day: "22" },
    { day: "23" },
    { day: "24", active: "orange" }, // Placement Drive target date!
    { day: "25" },
    { day: "26" },
    { day: "27" },
    { day: "28" },
    { day: "29" },
    { day: "30" },
  ];

  return (
    <div className="bg-white rounded-2xl p-5 sm:p-6 shadow-card border border-[#E5E9EF] grid grid-cols-1 md:grid-cols-12 gap-6">
      {/* LEFT PART: Smooth Wave Area Chart (~65% width) */}
      <div className="md:col-span-7 flex flex-col justify-between">
        {/* Legend at Top Left matching reference image */}
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

        {/* SVG Dual Smooth Wave Chart */}
        <div className="relative w-full h-[140px] sm:h-[150px] mt-2">
          <svg
            className="w-full h-full overflow-visible"
            viewBox="0 0 400 140"
            preserveAspectRatio="none"
          >
            <defs>
              {/* Navy Gradient */}
              <linearGradient id="navyWaveGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#123E63" stopOpacity="0.45" />
                <stop offset="100%" stopColor="#123E63" stopOpacity="0.0" />
              </linearGradient>

              {/* Orange Gradient */}
              <linearGradient id="orangeWaveGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stopColor="#F5A623" stopOpacity="0.65" />
                <stop offset="100%" stopColor="#F5A623" stopOpacity="0.05" />
              </linearGradient>
            </defs>

            {/* Back Wave: Navy Area Curve */}
            <path
              d="M 0 95 C 40 85, 70 50, 110 55 C 150 60, 180 110, 220 90 C 260 70, 280 40, 320 48 C 360 55, 380 75, 400 80 L 400 140 L 0 140 Z"
              fill="url(#navyWaveGrad)"
            />
            <path
              d="M 0 95 C 40 85, 70 50, 110 55 C 150 60, 180 110, 220 90 C 260 70, 280 40, 320 48 C 360 55, 380 75, 400 80"
              fill="none"
              stroke="#123E63"
              strokeWidth="2.5"
            />

            {/* Front Wave: Orange Glowing Area Curve */}
            <path
              d="M 0 120 C 50 115, 80 85, 120 90 C 150 95, 165 40, 195 45 C 225 50, 240 125, 280 110 C 310 98, 340 75, 400 85 L 400 140 L 0 140 Z"
              fill="url(#orangeWaveGrad)"
            />
            <path
              d="M 0 120 C 50 115, 80 85, 120 90 C 150 95, 165 40, 195 45 C 225 50, 240 125, 280 110 C 310 98, 340 75, 400 85"
              fill="none"
              stroke="#F5A623"
              strokeWidth="2.5"
            />
          </svg>
        </div>

        <div className="flex justify-between items-center text-[10px] text-[#8993A0] mt-1 pt-1 border-t border-[#E5E9EF]">
          <span>Week 1</span>
          <span>Week 2</span>
          <span>Week 3</span>
          <span>Week 4</span>
        </div>
      </div>

      {/* RIGHT PART: Mini Preparation Activity Calendar (~35% width) */}
      <div className="md:col-span-5 md:border-l md:border-[#E5E9EF] md:pl-6 flex flex-col justify-between">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-1.5 text-xs font-bold text-[#202B38]">
            <CalendarIcon className="w-3.5 h-3.5 text-[#123E63]" />
            <span>Target Calendar</span>
          </div>
          <span className="text-[11px] font-semibold text-[#8993A0]">
            October 2026
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

            if (item.active === "navy") {
              return (
                <div key={idx} className="flex justify-center items-center py-0.5">
                  <span className="w-5 h-5 rounded-md bg-[#123E63] text-white font-bold flex items-center justify-center shadow-xs">
                    {item.day}
                  </span>
                </div>
              );
            }

            if (item.active === "orange") {
              return (
                <div key={idx} className="flex justify-center items-center py-0.5">
                  <span className="w-5 h-5 rounded-md bg-[#F5A623] text-white font-bold flex items-center justify-center shadow-xs ring-2 ring-[#FFF6E8]">
                    {item.day}
                  </span>
                </div>
              );
            }

            return (
              <div key={idx} className="flex justify-center items-center py-0.5">
                <span className="text-[#8993A0] hover:text-[#202B38] font-medium transition cursor-pointer">
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
            <span className="w-2 h-2 rounded-sm bg-[#F5A623]" /> Target Goal
          </span>
        </div>
      </div>
    </div>
  );
}
