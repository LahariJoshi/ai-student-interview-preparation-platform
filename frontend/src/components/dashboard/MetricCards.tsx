"use client";

import React from "react";
import { FileText, Code2, Mic, Award, TrendingUp, Sparkles } from "lucide-react";

export interface MetricData {
  atsScore: number | null;
  codingSolved: number;
  codingTotal: number;
  codingAccuracy: number;
  interviewCount: number;
  interviewAvgScore: number | null;
  readinessScore: number;
}

interface MetricCardsProps {
  data: MetricData;
  isLoading?: boolean;
}

export default function MetricCards({ data, isLoading }: MetricCardsProps) {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-5 mb-6">
        {[1, 2, 3, 4].map((i) => (
          <div
            key={i}
            className="h-32 rounded-2xl bg-white border border-[#E5E9EF] p-5 animate-pulse flex flex-col justify-between"
          >
            <div className="h-4 bg-slate-200 rounded w-1/3" />
            <div className="h-8 bg-slate-200 rounded w-1/2" />
            <div className="h-3 bg-slate-200 rounded w-2/3" />
          </div>
        ))}
      </div>
    );
  }

  // Card 1: ATS Resume Score (Deep Navy Background matching Card 1 in reference)
  // Card 2: Coding Progress (White Card with Orange icon)
  // Card 3: Mock Interviews (White Card with Orange icon)
  // Card 4: Interview Readiness (White Card with Orange icon)

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-5 mb-6">
      {/* CARD 1: ATS Resume Score (SOLID NAVY CARD matching reference image) */}
      <div className="rounded-2xl bg-[#123E63] text-white p-5 shadow-navy-card relative overflow-hidden flex flex-col justify-between min-h-[135px] border border-[#0D3557]">
        {/* Top row */}
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-slate-200 tracking-wide uppercase">
            ATS Resume Score
          </span>
          <div className="w-8 h-8 rounded-full bg-white/10 flex items-center justify-center text-white backdrop-blur-sm border border-white/20">
            <FileText className="w-4 h-4 text-[#F5A623]" />
          </div>
        </div>

        {/* Big Metric Number */}
        <div className="my-1">
          <div className="text-3xl sm:text-4xl font-extrabold tracking-tight font-sans">
            {data.atsScore !== null ? `${Math.round(data.atsScore)}%` : "N/A"}
          </div>
        </div>

        {/* Subtext Status */}
        <div className="flex items-center gap-1.5 text-[11px] text-[#BCD3E6]">
          <TrendingUp className="w-3.5 h-3.5 text-[#F5A623]" />
          <span>
            {data.atsScore !== null
              ? data.atsScore >= 75
                ? "Optimal match for target roles"
                : "Needs keyword optimization"
              : "Upload resume to calculate"}
          </span>
        </div>
      </div>

      {/* CARD 2: Coding Progress (WHITE CARD with ORANGE ICON) */}
      <div className="rounded-2xl bg-white text-[#202B38] p-5 shadow-card border border-[#E5E9EF] flex flex-col justify-between min-h-[135px] hover:shadow-card-hover transition-shadow">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-[#8993A0] tracking-wide uppercase">
            Coding Solved
          </span>
          <div className="w-8 h-8 rounded-full bg-[#FFF6E8] flex items-center justify-center text-[#F5A623]">
            <Code2 className="w-4 h-4" />
          </div>
        </div>

        <div className="my-1">
          <div className="text-3xl sm:text-4xl font-extrabold tracking-tight text-[#202B38]">
            {data.codingSolved}
            <span className="text-sm font-normal text-[#8993A0] ml-1.5">
              / {data.codingTotal || 25}
            </span>
          </div>
        </div>

        <div className="flex items-center justify-between text-[11px] text-[#8993A0]">
          <span>Accuracy: {Math.round(data.codingAccuracy)}%</span>
          <span className="text-[#123E63] font-semibold">DSA Practice</span>
        </div>
      </div>

      {/* CARD 3: Mock Interviews (WHITE CARD with ORANGE ICON) */}
      <div className="rounded-2xl bg-white text-[#202B38] p-5 shadow-card border border-[#E5E9EF] flex flex-col justify-between min-h-[135px] hover:shadow-card-hover transition-shadow">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-[#8993A0] tracking-wide uppercase">
            Mock Interviews
          </span>
          <div className="w-8 h-8 rounded-full bg-[#FFF6E8] flex items-center justify-center text-[#F5A623]">
            <Mic className="w-4 h-4" />
          </div>
        </div>

        <div className="my-1">
          <div className="text-3xl sm:text-4xl font-extrabold tracking-tight text-[#202B38]">
            {data.interviewCount}
            <span className="text-sm font-normal text-[#8993A0] ml-1.5">
              Sessions
            </span>
          </div>
        </div>

        <div className="flex items-center justify-between text-[11px] text-[#8993A0]">
          <span>
            Avg: {data.interviewAvgScore !== null ? `${Math.round(data.interviewAvgScore)}%` : "0%"}
          </span>
          <span className="text-[#123E63] font-semibold">AI Speech & Rubric</span>
        </div>
      </div>

      {/* CARD 4: Interview Readiness (WHITE CARD with ORANGE STAR ICON) */}
      <div className="rounded-2xl bg-white text-[#202B38] p-5 shadow-card border border-[#E5E9EF] flex flex-col justify-between min-h-[135px] hover:shadow-card-hover transition-shadow">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold text-[#8993A0] tracking-wide uppercase">
            Overall Readiness
          </span>
          <div className="w-8 h-8 rounded-full bg-[#FFF6E8] flex items-center justify-center text-[#F5A623]">
            <Award className="w-4 h-4" />
          </div>
        </div>

        <div className="my-1 flex items-baseline gap-1">
          <div className="text-3xl sm:text-4xl font-extrabold tracking-tight text-[#202B38]">
            {(data.readinessScore / 10).toFixed(1)}
          </div>
          <span className="text-sm font-bold text-[#8993A0]">/ 10</span>
        </div>

        <div className="flex items-center justify-between text-[11px]">
          <span className="text-[#F5A623] font-semibold">
            {data.readinessScore >= 75
              ? "Interview Ready"
              : data.readinessScore >= 50
              ? "Good Progress"
              : "Prep In Progress"}
          </span>
          <span className="text-[#8993A0]">360&deg; Metric</span>
        </div>
      </div>
    </div>
  );
}
