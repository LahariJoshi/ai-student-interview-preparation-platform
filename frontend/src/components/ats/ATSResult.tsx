"use client";

import React from "react";
import { CheckCircle2, AlertTriangle, TrendingUp, Sparkles, Award } from "lucide-react";

interface ATSResultProps {
  result: {
    ats_score: number;
    formatting_score: number;
    keyword_match_score: number;
    semantic_similarity_score: number;
    action_impact_score: number;
    matched_skills: string[];
    missing_skills: string[];
    analysis_status: string;
  };
}

export default function ATSResult({ result }: ATSResultProps) {
  const atsScore = Math.round(result.ats_score || 0);

  return (
    <div className="space-y-6">
      {/* Top Banner (Solid Navy Card matching Reference Dashboard Style) */}
      <div className="rounded-2xl bg-[#123E63] text-white p-6 shadow-navy-card flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="text-xs font-semibold text-[#BCD3E6] uppercase tracking-wider">
            Job Description Alignment
          </span>
          <div className="text-4xl font-extrabold mt-1">
            {atsScore}
            <span className="text-xl text-[#BCD3E6] font-normal ml-1">/ 100</span>
          </div>
          <p className="text-xs text-[#BCD3E6] mt-1">
            {atsScore >= 75
              ? "Strong alignment with role requirements and screening keywords."
              : "Moderate alignment. Incorporate missing keywords to pass ATS automated filters."}
          </p>
        </div>

        <div className="flex items-center gap-2 self-start sm:self-auto">
          <div className="px-3.5 py-1.5 rounded-full bg-white/10 border border-white/20 text-xs font-bold text-white flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span>ATS Certified</span>
          </div>
        </div>
      </div>

      {/* Component Scores */}
      <div className="space-y-3">
        <h4 className="text-xs font-bold text-[#8993A0] uppercase tracking-wider">
          Multi-Factor Score Components
        </h4>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div className="p-4 rounded-xl border border-[#E5E9EF] bg-[#F8F9FA]">
            <p className="text-[11px] font-semibold text-[#8993A0]">Formatting</p>
            <p className="text-xl font-bold text-[#202B38] mt-0.5">
              {Math.round(result.formatting_score || 0)}%
            </p>
          </div>

          <div className="p-4 rounded-xl border border-[#E5E9EF] bg-[#F8F9FA]">
            <p className="text-[11px] font-semibold text-[#8993A0]">Keyword Match</p>
            <p className="text-xl font-bold text-[#202B38] mt-0.5">
              {Math.round(result.keyword_match_score || 0)}%
            </p>
          </div>

          <div className="p-4 rounded-xl border border-[#E5E9EF] bg-[#F8F9FA]">
            <p className="text-[11px] font-semibold text-[#8993A0]">Semantic Similarity</p>
            <p className="text-xl font-bold text-[#202B38] mt-0.5">
              {Math.round(result.semantic_similarity_score || 0)}%
            </p>
          </div>

          <div className="p-4 rounded-xl border border-[#E5E9EF] bg-[#F8F9FA]">
            <p className="text-[11px] font-semibold text-[#8993A0]">Action & Impact</p>
            <p className="text-xl font-bold text-[#202B38] mt-0.5">
              {Math.round(result.action_impact_score || 0)}%
            </p>
          </div>
        </div>
      </div>

      {/* Matched vs Missing Skills */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {/* Matched */}
        <div className="p-5 rounded-xl border border-emerald-200 bg-emerald-50/50 space-y-3">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <h4 className="text-xs font-bold text-emerald-800 uppercase tracking-wider">
              Matched Skills ({result.matched_skills?.length || 0})
            </h4>
          </div>

          <div className="flex flex-wrap gap-1.5">
            {result.matched_skills && result.matched_skills.length > 0 ? (
              result.matched_skills.map((skill, i) => (
                <span
                  key={i}
                  className="px-2.5 py-1 rounded-md bg-white border border-emerald-200 text-xs font-semibold text-emerald-700 shadow-2xs"
                >
                  ✓ {skill}
                </span>
              ))
            ) : (
              <p className="text-xs text-[#8993A0]">No direct keyword matches found.</p>
            )}
          </div>
        </div>

        {/* Missing */}
        <div className="p-5 rounded-xl border border-amber-200 bg-[#FFF6E8] space-y-3">
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-[#F5A623]" />
            <h4 className="text-xs font-bold text-amber-900 uppercase tracking-wider">
              Missing Target Skills ({result.missing_skills?.length || 0})
            </h4>
          </div>

          <div className="flex flex-wrap gap-1.5">
            {result.missing_skills && result.missing_skills.length > 0 ? (
              result.missing_skills.map((skill, i) => (
                <span
                  key={i}
                  className="px-2.5 py-1 rounded-md bg-white border border-amber-200 text-xs font-semibold text-[#202B38] shadow-2xs"
                >
                  + {skill}
                </span>
              ))
            ) : (
              <p className="text-xs text-[#8993A0]">Great job! All target job skills detected.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
