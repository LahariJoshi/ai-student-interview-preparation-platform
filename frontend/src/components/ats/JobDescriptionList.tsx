"use client";

import { useEffect, useState } from "react";
import { Trash2, Briefcase, Building2 } from "lucide-react";

import { apiFetch } from "@/lib/api";
import {
  JobDescription,
  JobDescriptionListResponse,
} from "@/types/ats";

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

      const response = await apiFetch<JobDescriptionListResponse>(
        "/ats/job-descriptions"
      );

      setJobDescriptions(response.job_descriptions);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to load job descriptions."
      );
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

      await apiFetch<{ message: string }>(
        `/ats/job-descriptions/${jobDescriptionId}`,
        {
          method: "DELETE",
        }
      );

      setJobDescriptions((current) =>
        current.filter((job) => job.id !== jobDescriptionId)
      );

      onDeleted(jobDescriptionId);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to delete job description."
      );
    } finally {
      setDeletingId(null);
    }
  };

  if (isLoading) {
    return (
      <div className="glass-card p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-5 bg-slate-800 rounded w-1/3" />
          <div className="h-20 bg-slate-800 rounded" />
          <div className="h-20 bg-slate-800 rounded" />
        </div>
      </div>
    );
  }

  return (
    <div className="glass-card p-6 space-y-5">
      <div>
        <h2 className="text-xl font-bold text-white">
          Saved Job Descriptions
        </h2>

        <p className="text-sm text-slate-400 mt-1">
          Your saved target roles for ATS analysis.
        </p>
      </div>

      {error && (
        <div className="rounded-xl border border-red-800 bg-red-950/40 px-4 py-3 text-sm text-red-300">
          {error}
        </div>
      )}

      {jobDescriptions.length === 0 ? (
        <div className="rounded-xl border border-dashed border-slate-700 p-8 text-center">
          <Briefcase className="w-8 h-8 text-slate-500 mx-auto mb-3" />

          <p className="text-slate-300 font-medium">
            No job descriptions saved yet.
          </p>

          <p className="text-sm text-slate-500 mt-1">
            Add a target job description to begin ATS preparation.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {jobDescriptions.map((job) => (
            <div
              key={job.id}
              className="rounded-xl border border-slate-700 bg-slate-900/60 p-4"
            >
              <div className="flex items-start justify-between gap-4">
                <div className="min-w-0 space-y-2">
                  <h3 className="text-base font-semibold text-white">
                    {job.title}
                  </h3>

                  {job.company_name && (
                    <div className="flex items-center gap-2 text-sm text-slate-400">
                      <Building2 className="w-4 h-4" />
                      <span>{job.company_name}</span>
                    </div>
                  )}

                  <p className="text-sm text-slate-400 line-clamp-3">
                    {job.description_text}
                  </p>
                </div>

                <button
                  type="button"
                  onClick={() => handleDelete(job.id)}
                  disabled={deletingId === job.id}
                  className="shrink-0 p-2 rounded-lg text-slate-400 hover:text-red-400 hover:bg-red-950/40 transition disabled:opacity-50"
                  title="Delete job description"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}