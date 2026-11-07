"use client";

import React from "react";
import Link from "next/link";
import { ArrowRight, CheckCircle2, AlertCircle } from "lucide-react";

interface ReadinessSidePanelProps {
  score: number;
  atsScore?: number | null;
  codingAccuracy?: number;
  interviewScore?: number | null;
}

export default function ReadinessSidePanel({
  score,
  atsScore,
  codingAccuracy = 75,
  interviewScore,
}: ReadinessSidePanelProps) {
  const percentage = Math.min(100, Math.max(0, Math.round(score)));

  // SVG Circular progress math
  const size = 150;
  const strokeWidth = 18;
  const center = size / 2;
  const radius = center - strokeWidth;
  const circumference = 2 * Math.PI * radius;

  // Split into Navy and Orange segments matching reference image donut
  const orangeShare = 0.45; // Orange arc
  const navyShare = 0.55; // Navy arc
  const orangeOffset = circumference * (1 - (percentage / 100) * orangeShare);
  const navyOffset = circumference * (1 - (percentage / 100));

  const items = [
    {
      label: "Resume ATS Match",
      value: atsScore !== null && atsScore !== undefined ? `${Math.round(atsScore)}%` : "Pending",
      status: (atsScore || 0) >= 70 ? "good" : "warning",
    },
    {
      label: "DSA Problem Solving",
      value: `${Math.round(codingAccuracy)}%`,
      status: codingAccuracy >= 60 ? "good" : "warning",
    },
    {
      label: "Mock Interview Delivery",
      value: interviewScore !== null && interviewScore !== undefined ? `${Math.round(interviewScore)}%` : "Pending",
      status: (interviewScore || 0) >= 70 ? "good" : "warning",
    },
    {
      label: "Behavioral & Soft Skills",
      value: "80%",
      status: "good",
    },
  ];

  return (
    <div className="bg-white rounded-2xl p-5 sm:p-6 shadow-card border border-[#E5E9EF] flex flex-col justify-between h-full">
      {/* Top Circular Donut Ring Chart matching Reference Image */}
      <div className="flex flex-col items-center justify-center pt-2 pb-4">
        <div className="relative w-[150px] h-[150px] flex items-center justify-center">
          <svg className="w-full h-full -rotate-90 transform" viewBox={`0 0 ${size} ${size}`}>
            {/* Background Circle */}
            <circle
              cx={center}
              cy={center}
              r={radius}
              fill="transparent"
              stroke="#F1F3F6"
              strokeWidth={strokeWidth}
            />
            {/* Navy Base Arc */}
            <circle
              cx={center}
              cy={center}
              r={radius}
              fill="transparent"
              stroke="#123E63"
              strokeWidth={strokeWidth}
              strokeDasharray={circumference}
              strokeDashoffset={circumference * (1 - (percentage / 100) * 0.7)}
              strokeLinecap="round"
              className="transition-all duration-1000 ease-out"
            />
            {/* Vibrant Orange Accent Arc */}
            <circle
              cx={center}
              cy={center}
              r={radius}
              fill="transparent"
              stroke="#F5A623"
              strokeWidth={strokeWidth}
              strokeDasharray={circumference}
              strokeDashoffset={circumference * (1 - (percentage / 100) * 0.35)}
              strokeLinecap="round"
              className="transition-all duration-1000 ease-out"
            />
          </svg>

          {/* Center Percentage Display matching reference "45%" */}
          <div className="absolute inset-0 flex flex-col items-center justify-center text-center">
            <span className="text-3xl font-extrabold text-[#202B38] tracking-tight">
              {percentage}%
            </span>
            <span className="text-[10px] font-semibold text-[#8993A0] uppercase tracking-wider">
              Readiness
            </span>
          </div>
        </div>
      </div>

      {/* Breakdown List with subtle dividers (Matching Reference Image 4 lines) */}
      <div className="space-y-3 my-4">
        {items.map((item, index) => (
          <div
            key={index}
            className="flex items-center justify-between py-2 border-b border-[#E5E9EF] text-xs font-medium"
          >
            <span className="text-[#8993A0] hover:text-[#202B38] transition truncate max-w-[150px]">
              {item.label}
            </span>
            <span
              className={`font-semibold ${
                item.status === "good" ? "text-[#123E63]" : "text-[#F5A623]"
              }`}
            >
              {item.value}
            </span>
          </div>
        ))}
      </div>

      {/* Prominent Amber/Orange 'Check Now' Button matching reference image */}
      <div className="pt-2">
        <Link
          href="/recommendations"
          className="w-full py-2.5 px-4 rounded-xl bg-[#F5A623] hover:bg-[#E09212] text-white text-xs font-bold tracking-wide shadow-md transition-all flex items-center justify-center gap-1.5"
        >
          <span>Check Now</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>
    </div>
  );
}
