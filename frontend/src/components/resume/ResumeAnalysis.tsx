"use client";

import React, { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import {
  AlertCircle,
  CheckCircle2,
  FileSearch,
  Loader2,
  XCircle,
} from "lucide-react";

interface GapItem {
  message: string;
  category: string;
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
  quality_details_json: Record<string, any> | null;
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

export default function ResumeAnalysis({
  resumeId,
}: ResumeAnalysisProps) {
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
      const data = await apiFetch<ResumeAnalysisData>(
        `/resume/${resumeId}/analysis`
      );

      setAnalysis(data);
    } catch (err: any) {
      if (err?.status === 404) {
        setAnalysis(null);
      } else {
        setError(
          err?.message || "Failed to load resume analysis."
        );
      }
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return (
      <div className="glass-card p-6">
        <div className="flex items-center justify-center gap-3 py-8 text-slate-400">
          <Loader2 className="w-5 h-5 animate-spin text-sky-400" />
          Loading resume analysis...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="glass-card p-6">
        <div className="flex items-start gap-2 text-red-300 text-sm">
          <AlertCircle className="w-5 h-5 shrink-0 text-red-400" />
          <span>{error}</span>
        </div>
      </div>
    );
  }

  if (!analysis) {
    return (
      <div className="glass-card p-6">
        <div className="flex flex-col items-center justify-center text-center py-8">
          <FileSearch className="w-10 h-10 text-slate-600 mb-3" />

          <h3 className="text-white font-semibold">
            Resume not analyzed yet
          </h3>

          <p className="text-slate-400 text-sm mt-1">
            Extract the resume text and analyze it to see your
            resume quality, skills and improvement areas.
          </p>
        </div>
      </div>
    );
  }

  const sections = analysis.sections_json || {};
  const skills = analysis.skills_json || {};
  const gaps = analysis.gaps_json || [];

  return (
    <div className="space-y-6">

      {/* Analysis Status */}
      {analysis.analysis_status !== "completed" && (
        <div className="glass-card p-4">
          <div className="flex items-center gap-2 text-amber-300 text-sm">
            <AlertCircle className="w-5 h-5" />
            Analysis status: {analysis.analysis_status}
          </div>
        </div>
      )}

      {/* Quality Score */}
      <div className="glass-card p-6">
        <div className="text-center">
          <p className="text-slate-400 text-sm">
            Resume Quality Score
          </p>

          <div className="mt-3">
            <span className="text-5xl font-extrabold text-white">
              {analysis.quality_score ?? "--"}
            </span>

            <span className="text-slate-500 text-lg ml-1">
              / 100
            </span>
          </div>

          <p className="text-slate-500 text-xs mt-2">
            Based on resume structure, contact information and
            detected content quality.
          </p>
        </div>
      </div>

      {/* Section Analysis */}
      <div className="glass-card p-6">
        <div className="flex items-center gap-2 mb-5">
          <FileSearch className="w-5 h-5 text-sky-400" />

          <h3 className="text-lg font-bold text-white">
            Section Analysis
          </h3>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {Object.entries(SECTION_LABELS).map(
            ([key, label]) => {
              const detected = sections[key] === true;

              return (
                <div
                  key={key}
                  className="flex items-center justify-between bg-slate-900 border border-slate-800 rounded-lg p-3"
                >
                  <span className="text-sm text-slate-300">
                    {label}
                  </span>

                  {detected ? (
                    <span className="flex items-center gap-1 text-emerald-400 text-xs font-medium">
                      <CheckCircle2 className="w-4 h-4" />
                      Detected
                    </span>
                  ) : (
                    <span className="flex items-center gap-1 text-slate-500 text-xs font-medium">
                      <XCircle className="w-4 h-4" />
                      Not detected
                    </span>
                  )}
                </div>
              );
            }
          )}
        </div>
      </div>

      {/* Detected Skills */}
      <div className="glass-card p-6">
        <h3 className="text-lg font-bold text-white mb-5">
          Detected Skills
        </h3>

        {Object.keys(skills).length === 0 ? (
          <p className="text-slate-500 text-sm">
            No recognisable skills detected.
          </p>
        ) : (
          <div className="space-y-5">
            {Object.entries(skills).map(
              ([category, skillList]) => {
                if (!skillList || skillList.length === 0) {
                  return null;
                }

                return (
                  <div key={category}>
                    <p className="text-sm font-semibold text-slate-300 mb-2">
                      {SKILL_CATEGORY_LABELS[category] ||
                        category}
                    </p>

                    <div className="flex flex-wrap gap-2">
                      {skillList.map((skill) => (
                        <span
                          key={skill}
                          className="px-3 py-1 rounded-full bg-sky-950/70 border border-sky-800 text-sky-300 text-xs"
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                );
              }
            )}
          </div>
        )}
      </div>

      {/* Improvement Gaps */}
      <div className="glass-card p-6">
        <h3 className="text-lg font-bold text-white mb-5">
          Improvement Areas
        </h3>

        {gaps.length === 0 ? (
          <div className="flex items-center gap-2 text-emerald-400 text-sm">
            <CheckCircle2 className="w-5 h-5" />
            No major gaps detected by the current analysis.
          </div>
        ) : (
          <div className="space-y-3">
            {gaps.map((gap, index) => (
              <div
                key={`${gap.category}-${index}`}
                className="flex items-start gap-3 bg-slate-900 border border-slate-800 rounded-lg p-4"
              >
                <AlertCircle className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />

                <div>
                  <p className="text-sm text-slate-300">
                    {gap.message}
                  </p>

                  <span className="inline-block mt-2 px-2 py-0.5 rounded bg-slate-800 text-slate-500 text-xs capitalize">
                    {gap.category}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Analysis Metadata */}
      {analysis.analyzed_at && (
        <p className="text-center text-slate-600 text-xs">
          Analysis generated on{" "}
          {new Date(
            analysis.analyzed_at
          ).toLocaleString()}
        </p>
      )}
    </div>
  );
}