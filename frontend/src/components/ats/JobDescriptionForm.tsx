"use client";

import { FormEvent, useState } from "react";
import { apiFetch } from "@/lib/api";
import {
  JobDescription,
  JobDescriptionCreate,
} from "@/types/ats";

interface JobDescriptionFormProps {
  onCreated: (jobDescription: JobDescription) => void;
}

export default function JobDescriptionForm({
  onCreated,
}: JobDescriptionFormProps) {
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

      const createdJobDescription = await apiFetch<JobDescription>(
        "/ats/job-descriptions",
        {
          method: "POST",
          body: JSON.stringify(data),
        }
      );

      onCreated(createdJobDescription);

      setTitle("");
      setCompanyName("");
      setDescriptionText("");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Failed to save job description."
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="glass-card p-6 space-y-5">
      <div>
        <h2 className="text-xl font-bold text-white">
          Add Job Description
        </h2>

        <p className="text-sm text-slate-400 mt-1">
          Enter a target job description for ATS compatibility analysis.
        </p>
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium text-slate-200">
          Job Title
        </label>

        <input
          type="text"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          placeholder="e.g. Machine Learning Engineer"
          className="w-full rounded-xl bg-slate-900 border border-slate-700 px-4 py-3 text-white outline-none focus:border-sky-500"
          disabled={isSubmitting}
        />
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium text-slate-200">
          Company Name
          <span className="text-slate-500"> (optional)</span>
        </label>

        <input
          type="text"
          value={companyName}
          onChange={(event) => setCompanyName(event.target.value)}
          placeholder="e.g. Tech Solutions"
          className="w-full rounded-xl bg-slate-900 border border-slate-700 px-4 py-3 text-white outline-none focus:border-sky-500"
          disabled={isSubmitting}
        />
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium text-slate-200">
          Job Description
        </label>

        <textarea
          value={descriptionText}
          onChange={(event) => setDescriptionText(event.target.value)}
          placeholder="Paste the complete job description here..."
          rows={10}
          className="w-full rounded-xl bg-slate-900 border border-slate-700 px-4 py-3 text-white outline-none focus:border-sky-500 resize-y"
          disabled={isSubmitting}
        />
      </div>

      {error && (
        <div className="rounded-xl border border-red-800 bg-red-950/40 px-4 py-3 text-sm text-red-300">
          {error}
        </div>
      )}

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full rounded-xl bg-sky-600 hover:bg-sky-500 disabled:bg-slate-700 disabled:text-slate-400 text-white font-medium px-5 py-3 transition"
      >
        {isSubmitting ? "Saving..." : "Save Job Description"}
      </button>
    </form>
  );
}