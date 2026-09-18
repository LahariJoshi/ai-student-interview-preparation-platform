"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import JobDescriptionForm from "@/components/ats/JobDescriptionForm";
import JobDescriptionList from "@/components/ats/JobDescriptionList";
import JobDescriptionSelector from "@/components/ats/JobDescriptionSelector";
import ResumeSelector from "@/components/ats/ResumeSelector";
import ATSResult from "@/components/ats/ATSResult";
import { JobDescription } from "@/types/ats";

export default function ATSPage() {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  const [refreshKey, setRefreshKey] = useState(0);
  const [selectedResumeId, setSelectedResumeId] = useState<string | null>(
    null
  );
  const [selectedJobDescriptionId, setSelectedJobDescriptionId] = useState<
    string | null
  >(null);

  const [atsResult, setAtsResult] = useState<any>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisError, setAnalysisError] = useState<string | null>(null);

  if (isLoading) {
    return (
        <div className="flex items-center justify-center min-h-[60vh]">
        <p className="text-slate-400">Loading...</p>
        </div>
    );
  }

  if (!user) {
    router.push("/login");
    return null;
  }

  const handleJobDescriptionCreated = (
    jobDescription: JobDescription
  ) => {
    setRefreshKey((prev) => prev + 1);
    setSelectedJobDescriptionId(jobDescription.id);
  };

  const canAnalyze =
    selectedResumeId !== null &&
    selectedJobDescriptionId !== null;

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

    console.log("ATS Analysis Result:", result);

    setAtsResult(result);
  } catch (error) {
    console.error("ATS analysis failed:", error);

    setAnalysisError(
      error instanceof Error
        ? error.message
        : "Failed to analyze resume."
    );
  } finally {
    setIsAnalyzing(false);
  }
};

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-white">
          ATS Resume Analyzer
        </h1>

        <p className="text-slate-400 mt-2">
          Compare your resume with a target job description and identify
          areas for improvement.
        </p>
      </div>

      {/* Job Description Management */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <JobDescriptionForm
          onCreated={handleJobDescriptionCreated}
        />

        <JobDescriptionList
          refreshKey={refreshKey}
          onDeleted={(jobDescriptionId) => {
            if (selectedJobDescriptionId === jobDescriptionId) {
              setSelectedJobDescriptionId(null);
            }
          }}
        />
      </div>

      {/* Resume Selection */}
      <ResumeSelector
        selectedResumeId={selectedResumeId}
        onSelect={setSelectedResumeId}
      />

      {/* Job Description Selection */}
      <JobDescriptionSelector
        selectedJobDescriptionId={selectedJobDescriptionId}
        onSelect={setSelectedJobDescriptionId}
      />

      {/* Analyze Button */}
      <div className="glass-card p-6">
        <button
          type="button"
          onClick={handleAnalyzeATS}
          disabled={!canAnalyze || isAnalyzing}
          className="w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-800 disabled:text-slate-500 disabled:cursor-not-allowed text-white font-semibold transition"
        >
          {isAnalyzing
            ? "Analyzing Resume..."
            : canAnalyze
            ? "Analyze Resume Against Job Description"
            : "Select a Resume and Job Description"}
        </button>

        {canAnalyze && (
          <div className="mt-4 text-center text-sm text-emerald-400">
            ✓ Resume and Job Description selected
          </div>
        )}
        {analysisError && (
          <p className="mt-4 text-center text-sm text-red-400">
            {analysisError}
          </p>
        )}
      </div>
      {atsResult && (
        <ATSResult result={atsResult} />
      )}
    </div>
  );
}