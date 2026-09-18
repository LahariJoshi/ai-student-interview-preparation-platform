"use client";

import React, { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import { Briefcase, Loader2, AlertCircle, CheckCircle2 } from "lucide-react";
import { JobDescription, JobDescriptionListResponse } from "@/types/ats";

interface JobDescriptionSelectorProps {
  selectedJobDescriptionId: string | null;
  onSelect: (jobDescriptionId: string) => void;
}

export default function JobDescriptionSelector({
  selectedJobDescriptionId,
  onSelect,
}: JobDescriptionSelectorProps) {
  const [jobDescriptions, setJobDescriptions] = useState<JobDescription[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchJobDescriptions();
  }, []);

  const fetchJobDescriptions = async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await apiFetch<JobDescriptionListResponse>(
        "/ats/job-descriptions"
      );

      setJobDescriptions(data.job_descriptions);
    } catch (err: any) {
      setError(err.message || "Failed to load job descriptions.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="glass-card p-6 space-y-4">
      <div>
        <h2 className="text-lg font-bold text-white flex items-center gap-2">
          <Briefcase className="w-5 h-5 text-indigo-400" />
          Step 2: Select Job Description
        </h2>

        <p className="text-sm text-slate-400 mt-1">
          Choose the job description you want to compare with your resume.
        </p>
      </div>

      {isLoading && (
        <div className="flex items-center justify-center py-8 text-slate-400">
          <Loader2 className="w-5 h-5 animate-spin mr-2" />
          Loading job descriptions...
        </div>
      )}

      {error && (
        <div className="bg-red-950/80 border border-red-800 text-red-300 p-3 rounded-lg flex items-start gap-2 text-sm">
          <AlertCircle className="w-5 h-5 shrink-0 text-red-400" />
          <span>{error}</span>
        </div>
      )}

      {!isLoading && !error && jobDescriptions.length === 0 && (
        <div className="text-center py-8 text-slate-400 text-sm">
          <p>No job descriptions saved yet.</p>
          <p className="mt-1">
            Create a job description above before starting ATS analysis.
          </p>
        </div>
      )}

      {!isLoading && !error && jobDescriptions.length > 0 && (
        <div className="space-y-3">
          {jobDescriptions.map((jobDescription) => {
            const isSelected =
              selectedJobDescriptionId === jobDescription.id;

            return (
              <button
                key={jobDescription.id}
                type="button"
                onClick={() => onSelect(jobDescription.id)}
                className={`w-full text-left p-4 rounded-xl border transition ${
                  isSelected
                    ? "border-indigo-500 bg-indigo-950/40"
                    : "border-slate-800 bg-slate-900 hover:border-slate-600"
                }`}
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex items-start gap-3">
                    <div
                      className={`w-10 h-10 rounded-lg flex items-center justify-center shrink-0 ${
                        isSelected
                          ? "bg-indigo-900/60 text-indigo-300"
                          : "bg-slate-800 text-indigo-400"
                      }`}
                    >
                      <Briefcase className="w-5 h-5" />
                    </div>

                    <div>
                      <h3 className="text-white font-medium">
                        {jobDescription.title}
                      </h3>

                      {jobDescription.company_name && (
                        <p className="text-sm text-slate-400 mt-1">
                          {jobDescription.company_name}
                        </p>
                      )}

                      <p className="text-xs text-slate-500 mt-2 line-clamp-2">
                        {jobDescription.description_text}
                      </p>
                    </div>
                  </div>

                  {isSelected && (
                    <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
                  )}
                </div>
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}