"use client";

import { useEffect, useState } from "react";
import { Trash2, Briefcase, Building2, Loader2 } from "lucide-react";
import { apiFetch } from "@/lib/api";
import { JobDescription, JobDescriptionListResponse } from "@/types/ats";

interface JobDescriptionListProps {
  refreshKey: number;
  onDeleted: (jobDescriptionId: string) => void;
}

export default function JobDescriptionList({
  refreshKey,
  onDeleted,
}: JobDescriptionListProps) {
  const [jobDescriptions, setJobDescriptions] = useState<JobDescription[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [deletingId, setDeletingId] = useState<string | null>(null);
  const [error, setError] = useState("");

  const fetchJobDescriptions = async () => {
    try {
      setIsLoading(true);
      setError("");
      const response = await apiFetch<JobDescriptionListResponse>("/ats/job-descriptions");
      setJobDescriptions(response.job_descriptions || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load job descriptions.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchJobDescriptions();
  }, [refreshKey]);

  const handleDelete = async (jobDescriptionId: string) => {
    try {
      setDeletingId(jobDescriptionId);
      setError("");
      await apiFetch<{ message: string }>(`/ats/job-descriptions/${jobDescriptionId}`, {
        method: "DELETE",
      });
      setJobDescriptions((current) => current.filter((job) => job.id !== jobDescriptionId));
      onDeleted(jobDescriptionId);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete job description.");
    } finally {
      setDeletingId(null);
    }
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-2xl p-6 shadow-card border border-[#E5E9EF] animate-pulse space-y-3">
        <div className="h-4 bg-slate-100 rounded w-1/3" />
        <div className="h-16 bg-slate-100 rounded-xl" />
        <div className="h-16 bg-slate-100 rounded-xl" />
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl p-6 shadow-card border border-[#E5E9EF] space-y-4">
      <div className="flex items-center justify-between border-b border-[#E5E9EF] pb-3">
        <div className="flex items-center gap-2">
          <Building2 className="w-4 h-4 text-[#123E63]" />
          <h3 className="text-base font-bold text-[#202B38]">Saved Target Roles</h3>
        </div>
        <span className="text-xs text-[#8993A0]">{jobDescriptions.length} Available</span>
      </div>

      {error && (
        <div className="p-3 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs font-semibold">
          {error}
        </div>
      )}

      {jobDescriptions.length === 0 ? (
        <div className="py-10 text-center text-[#8993A0] text-xs">
          No job descriptions saved yet. Use the form to add one.
        </div>
      ) : (
        <div className="space-y-2.5 max-h-[320px] overflow-y-auto pr-1">
          {jobDescriptions.map((job) => (
            <div
              key={job.id}
              className="p-3.5 rounded-xl border border-[#E5E9EF] bg-[#F8F9FA] hover:bg-white hover:border-[#BCD3E6] transition flex items-center justify-between gap-3"
            >
              <div className="min-w-0">
                <h4 className="text-xs font-bold text-[#202B38] truncate">{job.title}</h4>
                <p className="text-[11px] text-[#8993A0] truncate">
                  {job.company_name || "Company Not Specified"}
                </p>
              </div>

              <button
                type="button"
                onClick={() => handleDelete(job.id)}
                disabled={deletingId === job.id}
                className="p-1.5 rounded-lg text-[#8993A0] hover:text-red-600 hover:bg-red-50 transition shrink-0"
                title="Delete Job Description"
              >
                {deletingId === job.id ? (
                  <Loader2 className="w-4 h-4 animate-spin text-red-500" />
                ) : (
                  <Trash2 className="w-4 h-4" />
                )}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
