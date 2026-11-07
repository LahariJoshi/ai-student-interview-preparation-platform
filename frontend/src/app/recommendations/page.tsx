"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import {
  Compass,
  AlertTriangle,
  ArrowRight,
  Code2,
  FileText,
  Mic,
  CheckCircle2,
  Sparkles,
  BookOpen,
  Target,
} from "lucide-react";

interface WeakTopic {
  topic: string;
  attempted_count: number;
  solved_count: number;
  average_score: number;
  accuracy: number;
}

export default function RecommendationsPage() {
  const { user, isLoading: authLoading } = useAuth();
  const [weakTopics, setWeakTopics] = useState<WeakTopic[]>([]);
  const [missingSkills, setMissingSkills] = useState<string[]>([]);
  const [resumeGaps, setResumeGaps] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    async function fetchRecommendations() {
      setLoading(true);
      try {
        // 1. Weak coding topics
        try {
          const weakData = await apiFetch<WeakTopic[]>("/coding/performance/weak-topics");
          if (Array.isArray(weakData)) {
            setWeakTopics(weakData);
          }
        } catch {}

        // 2. Missing skills from latest ATS
        try {
          const atsData = await apiFetch<any>("/ats/latest");
          if (atsData && Array.isArray(atsData.missing_skills)) {
            setMissingSkills(atsData.missing_skills);
          }
        } catch {}

        // 3. Resume gaps from latest analysis
        try {
          const resumeData = await apiFetch<any>("/resume/latest/analysis");
          if (resumeData && Array.isArray(resumeData.gaps_json)) {
            setResumeGaps(resumeData.gaps_json);
          }
        } catch {}
      } catch (err) {
        console.error("Error loading recommendations:", err);
      } finally {
        setLoading(false);
      }
    }

    if (user) {
      fetchRecommendations();
    } else if (!authLoading) {
      setLoading(false);
    }
  }, [user, authLoading]);

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-[#202B38] tracking-tight">
            Learning Recommendations
          </h2>
          <p className="text-xs sm:text-sm text-[#8993A0] mt-0.5">
            Targeted practice modules prioritized based on your actual performance gaps
          </p>
        </div>

        <div className="px-3.5 py-1.5 rounded-full bg-[#123E63]/10 border border-[#123E63]/20 text-[#123E63] text-xs font-semibold flex items-center gap-1.5 self-start sm:self-auto">
          <Sparkles className="w-3.5 h-3.5 text-[#F5A623]" />
          <span>Real-time Diagnosis Active</span>
        </div>
      </div>

      {/* 1. High Priority Coding Weak Spots */}
      <section className="bg-white rounded-2xl p-5 sm:p-6 shadow-card border border-[#E5E9EF]">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-8 h-8 rounded-lg bg-[#FFF6E8] text-[#F5A623] flex items-center justify-center">
            <Code2 className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-base font-bold text-[#202B38] tracking-tight">
              Algorithmic Weak Problem Areas
            </h3>
            <p className="text-xs text-[#8993A0]">
              Identified by your lower solve rates or time-complexity bottlenecks
            </p>
          </div>
        </div>

        {weakTopics.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {weakTopics.map((item, idx) => (
              <div
                key={idx}
                className="p-4 rounded-xl border border-[#E5E9EF] bg-[#F8F9FA] flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-[10px] font-bold text-[#F5A623] uppercase tracking-wider px-2 py-0.5 rounded bg-[#FFF6E8]">
                      Accuracy: {Math.round(item.accuracy)}%
                    </span>
                    <span className="text-xs text-[#8993A0]">
                      Solved: {item.solved_count}/{item.attempted_count}
                    </span>
                  </div>
                  <h4 className="text-sm font-bold text-[#202B38]">
                    {item.topic}
                  </h4>
                  <p className="text-xs text-[#8993A0] mt-1">
                    Master key patterns and solve medium-tier problems in this topic to boost overall DSA readiness.
                  </p>
                </div>

                <Link
                  href="/coding"
                  className="mt-4 inline-flex items-center gap-1 text-xs font-bold text-[#123E63] hover:text-[#0D3557]"
                >
                  <span>Practice {item.topic} Problems</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            ))}
          </div>
        ) : (
          <div className="p-6 rounded-xl border border-dashed border-[#E5E9EF] text-center bg-[#F8F9FA]">
            <CheckCircle2 className="w-6 h-6 text-emerald-500 mx-auto mb-2" />
            <p className="text-xs font-bold text-[#202B38]">No Critical Algorithmic Weaknesses Detected</p>
            <p className="text-[11px] text-[#8993A0] mt-0.5">
              Keep solving daily problems in Dynamic Programming, Graphs, and Trees to maintain peak proficiency.
            </p>
          </div>
        )}
      </section>

      {/* 2. Resume & ATS Keyword Optimization Recommendations */}
      <section className="bg-white rounded-2xl p-5 sm:p-6 shadow-card border border-[#E5E9EF]">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-8 h-8 rounded-lg bg-[#123E63]/10 text-[#123E63] flex items-center justify-center">
            <FileText className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-base font-bold text-[#202B38] tracking-tight">
              Resume Structural & Keyword Enhancements
            </h3>
            <p className="text-xs text-[#8993A0]">
              Missing technical skills and structural gaps discovered in your uploaded resumes
            </p>
          </div>
        </div>

        {missingSkills.length > 0 || resumeGaps.length > 0 ? (
          <div className="space-y-4">
            {missingSkills.length > 0 && (
              <div className="p-4 rounded-xl border border-[#E5E9EF] bg-[#F8F9FA]">
                <h4 className="text-xs font-bold text-[#202B38] mb-2 uppercase tracking-wider">
                  Target Job Missing Keywords:
                </h4>
                <div className="flex flex-wrap gap-2">
                  {missingSkills.map((skill, i) => (
                    <span
                      key={i}
                      className="px-2.5 py-1 rounded-md text-xs font-semibold bg-white border border-[#E5E9EF] text-[#123E63] shadow-xs"
                    >
                      + {skill}
                    </span>
                  ))}
                </div>
                <p className="text-xs text-[#8993A0] mt-3">
                  Integrating these skills into your Projects and Skills sections will directly elevate your ATS compatibility.
                </p>
              </div>
            )}

            {resumeGaps.length > 0 && (
              <div className="space-y-2">
                {resumeGaps.slice(0, 3).map((gap, i) => (
                  <div
                    key={i}
                    className="p-3 rounded-xl border border-amber-200 bg-[#FFF6E8] flex items-start gap-2.5 text-xs text-[#202B38]"
                  >
                    <AlertTriangle className="w-4 h-4 text-[#F5A623] shrink-0 mt-0.5" />
                    <div>
                      <span className="font-bold">{gap.category || "Structure"}: </span>
                      <span>{gap.message || JSON.stringify(gap)}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}

            <div className="pt-2">
              <Link
                href="/resume"
                className="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-[#123E63] hover:bg-[#0D3557] text-white text-xs font-bold shadow-sm transition"
              >
                <span>Edit and Re-Analyze Resume</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        ) : (
          <div className="p-6 rounded-xl border border-dashed border-[#E5E9EF] text-center bg-[#F8F9FA]">
            <CheckCircle2 className="w-6 h-6 text-emerald-500 mx-auto mb-2" />
            <p className="text-xs font-bold text-[#202B38]">Resume Structure Meets All High Standards</p>
            <p className="text-[11px] text-[#8993A0] mt-0.5">
              Run an ATS scan against specific job descriptions to uncover company-specific keyword suggestions.
            </p>
          </div>
        )}
      </section>

      {/* 3. AI Mock Interview Practice Roadmap */}
      <section className="bg-white rounded-2xl p-5 sm:p-6 shadow-card border border-[#E5E9EF] flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div className="space-y-2 max-w-2xl">
          <div className="flex items-center gap-2">
            <Mic className="w-5 h-5 text-[#F5A623]" />
            <h3 className="text-base font-bold text-[#202B38] tracking-tight">
              Behavioral & Technical Mock Interview Roadmap
            </h3>
          </div>
          <p className="text-xs text-[#8993A0] leading-relaxed">
            Practice structuring answers using the STAR method (Situation, Task, Action, Result). Get automated feedback on pace, vocabulary diversity, and technical accuracy.
          </p>
        </div>

        <Link
          href="/interview"
          className="px-5 py-2.5 rounded-xl bg-[#F5A623] hover:bg-[#E09212] text-white text-xs font-bold shadow-md transition shrink-0 flex items-center gap-2"
        >
          <span>Launch AI Mock Interview</span>
          <ArrowRight className="w-4 h-4" />
        </Link>
      </section>
    </div>
  );
}
