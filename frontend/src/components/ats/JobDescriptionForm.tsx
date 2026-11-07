"use client";

import { FormEvent, useState } from "react";
import { apiFetch } from "@/lib/api";
import { JobDescription, JobDescriptionCreate } from "@/types/ats";
import { PlusCircle, Building, Briefcase, FileText, Loader2 } from "lucide-react";

interface JobDescriptionFormProps {
  onCreated: (jobDescription: JobDescription) => void;
}

export default function JobDescriptionForm({ onCreated }: JobDescriptionFormProps) {
  const [title, setTitle] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [descriptionText, setDescriptionText] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");

    if (!title.trim()) {
      setError("Job title is required.");
      return;
    }

    if (!descriptionText.trim()) {
      setError("Job description is required.");
      return;
    }

    const data: JobDescriptionCreate = {
      title: title.trim(),
      company_name: companyName.trim() || undefined,
      description_text: descriptionText.trim(),
    };

    try {
      setIsSubmitting(true);
      const createdJobDescription = await apiFetch<JobDescription>("/ats/job-descriptions", {
        method: "POST",
        body: JSON.stringify(data),
      });

      onCreated(createdJobDescription);
      setTitle("");
      setCompanyName("");
      setDescriptionText("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save job description.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-2xl p-6 shadow-card border border-[#E5E9EF] space-y-4">
      <div className="flex items-center gap-2 border-b border-[#E5E9EF] pb-3">
        <Briefcase className="w-4 h-4 text-[#123E63]" />
        <h3 className="text-base font-bold text-[#202B38]">Add Target Job Description</h3>
      </div>

      {error && (
        <div className="p-3 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs font-semibold">
          {error}
        </div>
      )}

      <div className="space-y-1">
        <label className="text-[11px] font-bold text-[#8993A0] uppercase tracking-wider">
          Job Title *
        </label>
        <input
          type="text"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          placeholder="e.g. Full Stack Engineer"
          className="w-full rounded-xl bg-[#F8F9FA] border border-[#E5E9EF] px-3.5 py-2.5 text-xs text-[#202B38] font-medium outline-none focus:border-[#123E63] transition"
          disabled={isSubmitting}
        />
      </div>

      <div className="space-y-1">
        <label className="text-[11px] font-bold text-[#8993A0] uppercase tracking-wider">
          Company Name (Optional)
        </label>
        <input
          type="text"
          value={companyName}
          onChange={(event) => setCompanyName(event.target.value)}
          placeholder="e.g. Google, Microsoft, Startup"
          className="w-full rounded-xl bg-[#F8F9FA] border border-[#E5E9EF] px-3.5 py-2.5 text-xs text-[#202B38] font-medium outline-none focus:border-[#123E63] transition"
          disabled={isSubmitting}
        />
      </div>

      <div className="space-y-1">
        <label className="text-[11px] font-bold text-[#8993A0] uppercase tracking-wider">
          Job Description Text *
        </label>
        <textarea
          rows={5}
          value={descriptionText}
          onChange={(event) => setDescriptionText(event.target.value)}
          placeholder="Paste full job requirements, qualifications, and tech stack here..."
          className="w-full rounded-xl bg-[#F8F9FA] border border-[#E5E9EF] px-3.5 py-2.5 text-xs text-[#202B38] font-medium outline-none focus:border-[#123E63] transition"
          disabled={isSubmitting}
        />
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full py-2.5 rounded-xl bg-[#123E63] hover:bg-[#0D3557] disabled:opacity-50 text-white font-bold transition text-xs shadow-sm flex items-center justify-center gap-2"
      >
        {isSubmitting && <Loader2 className="w-3.5 h-3.5 animate-spin" />}
        <span>Save Job Description</span>
      </button>
    </form>
  );
}
