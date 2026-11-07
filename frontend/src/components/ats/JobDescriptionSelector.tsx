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
      const data = await apiFetch<JobDescriptionListResponse>("/ats/job-descriptions");
      setJobDescriptions(data.job_descriptions || []);
      if (!selectedJobDescriptionId && data.job_descriptions && data.job_descriptions.length > 0) {
        onSelect(data.job_descriptions[0].id);
      }
    } catch (err: any) {
      setError(err.message || "Failed to load job descriptions.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl p-6 shadow-card border border-[#E5E9EF] space-y-4">
      <div className="flex items-center justify-between border-b border-[#E5E9EF] pb-3">
        <div className="flex items-center gap-2">
          <Briefcase className="w-4 h-4 text-[#123E63]" />
          <h3 className="text-base font-bold text-[#202B38]">2. Select Target Role</h3>
        </div>
        <span className="text-xs text-[#8993A0]">{jobDescriptions.length} available</span>
      </div>

      {isLoading ? (
        <div className="py-6 text-center text-[#8993A0] text-xs">Loading roles...</div>
      ) : error ? (
        <div className="p-3 rounded-xl bg-red-50 text-red-600 text-xs">{error}</div>
      ) : jobDescriptions.length === 0 ? (
        <div className="py-6 text-center text-[#8993A0] text-xs">
          No job descriptions added yet. Add one in the form above.
        </div>
      ) : (
        <div className="space-y-2 max-h-[220px] overflow-y-auto pr-1">
          {jobDescriptions.map((job) => {
            const isSelected = selectedJobDescriptionId === job.id;
            return (
              <div
                key={job.id}
                onClick={() => onSelect(job.id)}
                className={`p-3 rounded-xl border cursor-pointer transition flex items-center justify-between text-xs ${
                  isSelected
                    ? "bg-[#FFF6E8] border-[#F5A623] shadow-xs"
                    : "bg-[#F8F9FA] border-[#E5E9EF] hover:border-[#BCD3E6]"
                }`}
              >
                <div className="flex items-center gap-2.5 truncate">
                  <Briefcase className={`w-4 h-4 shrink-0 ${isSelected ? "text-[#F5A623]" : "text-[#123E63]"}`} />
                  <div className="truncate">
                    <span className="font-bold text-[#202B38] block truncate">{job.title}</span>
                    <span className="text-[10px] text-[#8993A0] truncate">{job.company_name || "Target Company"}</span>
                  </div>
                </div>
                {isSelected && (
                  <CheckCircle2 className="w-4 h-4 text-[#F5A623] shrink-0" />
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
