"use client";

import React, { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import {
  AlertCircle,
  CheckCircle2,
  FileSearch,
  Loader2,
  XCircle,
  Award,
  Sparkles,
} from "lucide-react";

interface GapItem {
  message: string;
  category: string;
}

interface M4AdvancedQuality {
  total_score: number;
  length_score: number;
  action_verb_score: number;
  metrics_score: number;
  project_quality_score: number;
  skill_breadth_score: number;
  skill_category_diversity_score: number;
  summary_quality_score: number;
  section_completeness_score: number;
  contact_score: number;
  sections_found: number;
  sections_checked: number;
  contact_fields_found: number;
  total_skills_detected: number;
}

interface ResumeAnalysisData {
  id: string;
  resume_id: string;
  user_id: string;
  analysis_status: string;
  quality_score: number | null;
  sections_json: Record<string, boolean> | null;
  skills_json: Record<string, string[]> | null;
  gaps_json: GapItem[] | null;
  quality_details_json: {
    m3_structural?: Record<string, any>;
    m4_advanced?: M4AdvancedQuality;
  } | null;
  analyzed_at: string | null;
  created_at: string;
  updated_at: string;
}

interface ResumeAnalysisProps {
  resumeId: string;
}

const SECTION_LABELS: Record<string, string> = {
  contact: "Contact Information",
  summary: "Summary / Objective",
  education: "Education",
  skills: "Skills",
  projects: "Projects",
  experience: "Experience",
  internships: "Internships",
  certifications: "Certifications",
  achievements: "Achievements",
  publications: "Publications",
  extracurricular: "Extracurricular Activities",
};

const SKILL_CATEGORY_LABELS: Record<string, string> = {
  programming_languages: "Programming Languages",
  web_technologies: "Web Technologies",
  ai_ml: "AI / Machine Learning",
  databases: "Databases",
  cloud_devops: "Cloud / DevOps",
  tools_platforms: "Tools / Platforms",
  core_cs: "Core Computer Science",
  soft_skills: "Soft Skills",
};

export default function ResumeAnalysis({ resumeId }: ResumeAnalysisProps) {
  const [analysis, setAnalysis] = useState<ResumeAnalysisData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAnalysis();
  }, [resumeId]);

  const fetchAnalysis = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await apiFetch<ResumeAnalysisData>(`/resume/${resumeId}/analysis`);
      setAnalysis(data);
    } catch (err: any) {
      if (err?.status === 404) {
        setAnalysis(null);
      } else {
        setError(err?.message || "Failed to load resume analysis.");
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="bg-[#F8F9FA] rounded-xl p-8 border border-[#E5E9EF] text-center text-[#8993A0] space-y-2">
        <Loader2 className="w-6 h-6 animate-spin text-[#123E63] mx-auto" />
        <p className="text-xs font-semibold">Evaluating resume metrics...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 flex items-start gap-2 text-xs">
        <AlertCircle className="w-4 h-4 shrink-0 text-red-500 mt-0.5" />
        <span>{error}</span>
      </div>
    );
  }

  if (!analysis) {
    return (
      <div className="bg-[#F8F9FA] rounded-xl p-8 text-center border border-[#E5E9EF] space-y-2">
        <FileSearch className="w-8 h-8 text-[#BCD3E6] mx-auto" />
        <h4 className="text-sm font-bold text-[#202B38]">Resume not analyzed yet</h4>
        <p className="text-xs text-[#8993A0]">
          Click &apos;Analyze&apos; on this resume above to generate your score breakdown.
        </p>
      </div>
    );
  }

  const sections = analysis.sections_json || {};
  const skills = analysis.skills_json || {};
  const gaps = analysis.gaps_json || [];
  const m4Advanced = analysis.quality_details_json?.m4_advanced;

  return (
    <div className="space-y-6">
      {/* Top Overall Quality Score Card (Navy Style) */}
      <div className="rounded-2xl bg-[#123E63] text-white p-6 shadow-navy-card flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="text-xs font-semibold text-[#BCD3E6] uppercase tracking-wider">
            Resume Overall Quality Score
          </span>
          <div className="text-4xl font-extrabold mt-1">
            {analysis.quality_score !== null ? `${Math.round(analysis.quality_score)} / 100` : "Processing"}
          </div>
          <p className="text-xs text-[#BCD3E6] mt-1">
            {analysis.quality_score && analysis.quality_score >= 75
              ? "Strong resume draft with balanced technical keywords."
              : "Room for improvement in metrics and project descriptions."}
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="px-4 py-2 rounded-xl bg-white/10 border border-white/20 text-center">
            <div className="text-lg font-bold text-[#F5A623]">
              {m4Advanced ? m4Advanced.total_skills_detected : 0}
            </div>
            <div className="text-[10px] text-[#BCD3E6]">Skills Detected</div>
          </div>
          <div className="px-4 py-2 rounded-xl bg-white/10 border border-white/20 text-center">
            <div className="text-lg font-bold text-white">
              {m4Advanced ? `${m4Advanced.sections_found}/${m4Advanced.sections_checked}` : "0"}
            </div>
            <div className="text-[10px] text-[#BCD3E6]">Sections Validated</div>
          </div>
        </div>
      </div>

      {/* M4 Quality Breakdown */}
      {m4Advanced && (
        <div className="space-y-3">
          <h4 className="text-sm font-bold text-[#202B38] uppercase tracking-wider">
            Evaluation Breakdown
          </h4>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="p-3.5 rounded-xl border border-[#E5E9EF] bg-[#F8F9FA]">
              <span className="text-[10px] font-semibold text-[#8993A0]">Length Score</span>
              <p className="text-base font-bold text-[#202B38] mt-0.5">{m4Advanced.length_score} / 10</p>
            </div>
            <div className="p-3.5 rounded-xl border border-[#E5E9EF] bg-[#F8F9FA]">
              <span className="text-[10px] font-semibold text-[#8993A0]">Action Verbs</span>
              <p className="text-base font-bold text-[#202B38] mt-0.5">{m4Advanced.action_verb_score} / 10</p>
            </div>
            <div className="p-3.5 rounded-xl border border-[#E5E9EF] bg-[#F8F9FA]">
              <span className="text-[10px] font-semibold text-[#8993A0]">Metrics & Data</span>
              <p className="text-base font-bold text-[#202B38] mt-0.5">{m4Advanced.metrics_score} / 10</p>
            </div>
            <div className="p-3.5 rounded-xl border border-[#E5E9EF] bg-[#F8F9FA]">
              <span className="text-[10px] font-semibold text-[#8993A0]">Project Quality</span>
              <p className="text-base font-bold text-[#202B38] mt-0.5">{m4Advanced.project_quality_score} / 15</p>
            </div>
          </div>
        </div>
      )}

      {/* Section Completeness */}
      <div className="space-y-3">
        <h4 className="text-sm font-bold text-[#202B38] uppercase tracking-wider">
          Section Completeness
        </h4>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5">
          {Object.entries(SECTION_LABELS).map(([key, label]) => {
            const detected = sections[key] === true;
            return (
              <div
                key={key}
                className={`p-2.5 rounded-xl border flex items-center justify-between text-xs font-medium ${
                  detected
                    ? "bg-emerald-50/70 border-emerald-200 text-[#202B38]"
                    : "bg-[#F8F9FA] border-[#E5E9EF] text-[#8993A0]"
                }`}
              >
                <span>{label}</span>
                {detected ? (
                  <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                ) : (
                  <XCircle className="w-4 h-4 text-slate-300" />
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Detected Skills by Category */}
      <div className="space-y-3">
        <h4 className="text-sm font-bold text-[#202B38] uppercase tracking-wider">
          Detected Technical Skills
        </h4>

        {Object.keys(skills).length === 0 ? (
          <p className="text-xs text-[#8993A0]">No recognized technical skills detected.</p>
        ) : (
          <div className="space-y-3">
            {Object.entries(skills).map(([category, skillList]) => {
              if (!skillList || skillList.length === 0) return null;
              return (
                <div key={category} className="p-3 rounded-xl border border-[#E5E9EF] bg-[#F8F9FA]">
                  <span className="text-[11px] font-bold text-[#123E63] uppercase tracking-wider block mb-1.5">
                    {SKILL_CATEGORY_LABELS[category] || category}
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {skillList.map((skill) => (
                      <span
                        key={skill}
                        className="px-2.5 py-0.5 rounded-md bg-white border border-[#E5E9EF] text-xs font-semibold text-[#202B38] shadow-2xs"
                      >
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Improvement Gaps */}
      <div className="space-y-3">
        <h4 className="text-sm font-bold text-[#202B38] uppercase tracking-wider">
          Targeted Improvement Areas
        </h4>

        {gaps.length === 0 ? (
          <div className="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-700 flex items-center gap-2 text-xs font-semibold">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span>No critical gaps detected by the evaluation analyzer!</span>
          </div>
        ) : (
          <div className="space-y-2">
            {gaps.map((gap, index) => (
              <div
                key={`${gap.category}-${index}`}
                className="p-3 rounded-xl border border-amber-200 bg-[#FFF6E8] flex items-start gap-2.5 text-xs text-[#202B38]"
              >
                <AlertCircle className="w-4 h-4 text-[#F5A623] shrink-0 mt-0.5" />
                <div>
                  <span className="font-bold uppercase tracking-wider text-[10px] text-[#F5A623] block">
                    {gap.category}
                  </span>
                  <p className="mt-0.5">{gap.message}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
