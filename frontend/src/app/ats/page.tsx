"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import JobDescriptionForm from "@/components/ats/JobDescriptionForm";
import JobDescriptionList from "@/components/ats/JobDescriptionList";
import JobDescriptionSelector from "@/components/ats/JobDescriptionSelector";
import ResumeSelector from "@/components/ats/ResumeSelector";
import ATSResult from "@/components/ats/ATSResult";
import { JobDescription } from "@/types/ats";
import { Target, ArrowRight, Loader2, Sparkles, CheckCircle2, AlertCircle } from "lucide-react";

export default function ATSPage() {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  const [refreshKey, setRefreshKey] = useState(0);
  const [selectedResumeId, setSelectedResumeId] = useState<string | null>(null);
  const [selectedJobDescriptionId, setSelectedJobDescriptionId] = useState<string | null>(null);
  const [atsResult, setAtsResult] = useState<any>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisError, setAnalysisError] = useState<string | null>(null);

  if (isLoading) {
    return (
      <div className="py-20 text-center text-[#8993A0]">
        <div className="animate-spin w-8 h-8 border-2 border-[#123E63] border-t-transparent rounded-full mx-auto mb-4" />
        <p className="text-xs font-semibold">Loading ATS Engine...</p>
      </div>
    );
  }

  if (!user) {
    router.push("/login");
    return null;
  }

  const handleJobDescriptionCreated = (jobDescription: JobDescription) => {
    setRefreshKey((prev) => prev + 1);
    setSelectedJobDescriptionId(jobDescription.id);
  };

  const canAnalyze = selectedResumeId !== null && selectedJobDescriptionId !== null;

  const handleAnalyzeATS = async () => {
    if (!canAnalyze) return;

    try {
      setIsAnalyzing(true);
      setAnalysisError(null);

      const result = await apiFetch("/ats/analyze", {
        method: "POST",
        body: JSON.stringify({
          resume_id: selectedResumeId,
          job_description_id: selectedJobDescriptionId,
        }),
      });

      setAtsResult(result);
    } catch (error) {
      setAnalysisError(
        error instanceof Error ? error.message : "Failed to analyze resume."
      );
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl">
      {/* Header */}
      <div className="bg-white rounded-2xl p-6 sm:p-7 shadow-card border border-[#E5E9EF] flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#123E63]/10 border border-[#123E63]/20 text-[#123E63] text-xs font-semibold mb-2">
            <Target className="w-3.5 h-3.5 text-[#F5A623]" />
            Multi-Dimensional Matcher
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-[#202B38] tracking-tight">
            ATS Resume Matcher
          </h2>
          <p className="text-xs sm:text-sm text-[#8993A0] mt-1">
            Compare your resume against real target job descriptions using keyword frequency and semantic sentence embeddings.
          </p>
        </div>

        <Link
          href="/resume"
          className="px-4 py-2.5 rounded-xl bg-[#F8F9FA] hover:bg-[#EAEFF5] text-[#123E63] border border-[#E5E9EF] text-xs font-bold transition flex items-center gap-1.5 self-start sm:self-auto"
        >
          <span>Manage Resumes</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>

      {/* Job Description Management */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <JobDescriptionForm onCreated={handleJobDescriptionCreated} />
        <JobDescriptionList
          refreshKey={refreshKey}
          onDeleted={(jobDescriptionId) => {
            if (selectedJobDescriptionId === jobDescriptionId) {
              setSelectedJobDescriptionId(null);
            }
          }}
        />
      </div>

      {/* Selectors */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <ResumeSelector
          selectedResumeId={selectedResumeId}
          onSelect={setSelectedResumeId}
        />
        <JobDescriptionSelector
          selectedJobDescriptionId={selectedJobDescriptionId}
          onSelect={setSelectedJobDescriptionId}
        />
      </div>

      {/* Analyze Action Trigger */}
      <div className="bg-white rounded-2xl p-6 shadow-card border border-[#E5E9EF]">
        <button
          type="button"
          onClick={handleAnalyzeATS}
          disabled={!canAnalyze || isAnalyzing}
          className="w-full py-3.5 rounded-xl bg-[#123E63] hover:bg-[#0D3557] disabled:bg-[#F1F3F6] disabled:text-[#8993A0] disabled:cursor-not-allowed text-white font-bold transition text-xs shadow-md flex items-center justify-center gap-2"
        >
          {isAnalyzing ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin text-[#F5A623]" />
              <span>Running Semantic & Keyword ATS Pipeline...</span>
            </>
          ) : canAnalyze ? (
            <>
              <Sparkles className="w-4 h-4 text-[#F5A623]" />
              <span>Run Complete ATS Match Analysis</span>
            </>
          ) : (
            <span>Select both a Resume and a Job Description above</span>
          )}
        </button>

        {canAnalyze && !isAnalyzing && (
          <div className="mt-3 text-center text-xs text-emerald-600 font-semibold flex items-center justify-center gap-1.5">
            <CheckCircle2 className="w-4 h-4" />
            <span>Target resume and job description selected and ready for analysis</span>
          </div>
        )}

        {analysisError && (
          <div className="mt-3 p-3 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs flex items-center justify-center gap-2">
            <AlertCircle className="w-4 h-4 text-red-500 shrink-0" />
            <span>{analysisError}</span>
          </div>
        )}
      </div>

      {/* ATS Result Display */}
      {atsResult && (
        <div className="bg-white rounded-2xl p-6 sm:p-7 shadow-card border border-[#E5E9EF]">
          <ATSResult result={atsResult} />
        </div>
      )}
    </div>
  );
}
