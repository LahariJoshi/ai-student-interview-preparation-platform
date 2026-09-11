"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import { User, Briefcase, Code, Link2, CheckCircle2, AlertCircle, Save } from "lucide-react";

interface ProfileData {
  id: string;
  user_id: string;
  target_role: string | null;
  experience_level: string | null;
  target_companies: string[];
  tech_skills: string[];
  github_url: string | null;
  linkedin_url: string | null;
}

export default function ProfilePage() {
  const router = useRouter();
  const { user, isLoading: authLoading } = useAuth();
  const [profile, setProfile] = useState<ProfileData | null>(null);
  const [targetRole, setTargetRole] = useState("");
  const [experienceLevel, setExperienceLevel] = useState("Entry Level");
  const [skillsInput, setSkillsInput] = useState("");
  const [githubUrl, setGithubUrl] = useState("");
  const [linkedinUrl, setLinkedinUrl] = useState("");
  const [statusMessage, setStatusMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [isFetching, setIsFetching] = useState(true);

  useEffect(() => {
    if (!authLoading && !user) {
      router.push("/login");
      return;
    }

    if (user) {
      fetchProfile();
    }
  }, [user, authLoading]);

  const fetchProfile = async () => {
    setIsFetching(true);
    try {
      const data = await apiFetch<ProfileData>("/profile");
      setProfile(data);
      setTargetRole(data.target_role || "");
      setExperienceLevel(data.experience_level || "Entry Level");
      setSkillsInput(data.tech_skills ? data.tech_skills.join(", ") : "");
      setGithubUrl(data.github_url || "");
      setLinkedinUrl(data.linkedin_url || "");
    } catch (err: any) {
      setStatusMessage({ type: "error", text: err.message || "Failed to load profile." });
    } fontFinally: {
      setIsFetching(false);
    }
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaving(true);
    setStatusMessage(null);

    const parsedSkills = skillsInput
      .split(",")
      .map((s) => s.trim())
      .filter((s) => s.length > 0);

    try {
      const updated = await apiFetch<ProfileData>("/profile", {
        method: "PUT",
        body: JSON.stringify({
          target_role: targetRole,
          experience_level: experienceLevel,
          tech_skills: parsedSkills,
          github_url: githubUrl,
          linkedin_url: linkedinUrl,
        }),
      });
      setProfile(updated);
      setStatusMessage({ type: "success", text: "Profile updated successfully!" });
    } catch (err: any) {
      setStatusMessage({ type: "error", text: err.message || "Failed to update profile." });
    } finally {
      setIsSaving(false);
    }
  };

  if (authLoading || isFetching) {
    return (
      <div className="py-20 text-center text-slate-400">
        <div className="animate-spin w-8 h-8 border-2 border-sky-400 border-t-transparent rounded-full mx-auto mb-4" />
        Loading student profile...
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto py-8 space-y-8">
      {/* Header Info */}
      <div className="glass-card p-6 flex items-center gap-4">
        <div className="w-16 h-16 rounded-full bg-sky-900/60 border border-sky-700 flex items-center justify-center text-sky-400 text-2xl font-bold">
          {user?.full_name?.charAt(0).toUpperCase()}
        </div>
        <div>
          <h1 className="text-2xl font-bold text-white">{user?.full_name}</h1>
          <p className="text-slate-400 text-sm">{user?.email} • Student Account</p>
        </div>
      </div>

      {statusMessage && (
        <div
          className={`p-4 rounded-lg flex items-center gap-2 text-sm border ${
            statusMessage.type === "success"
              ? "bg-emerald-950/80 border-emerald-800 text-emerald-300"
              : "bg-red-950/80 border-red-800 text-red-300"
          }`}
        >
          {statusMessage.type === "success" ? (
            <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
          ) : (
            <AlertCircle className="w-5 h-5 text-red-400 shrink-0" />
          )}
          <span>{statusMessage.text}</span>
        </div>
      )}

      {/* Edit Profile Form */}
      <form onSubmit={handleSave} className="glass-card p-6 space-y-6">
        <h2 className="text-xl font-bold text-white flex items-center gap-2 border-b border-slate-800 pb-3">
          <Briefcase className="w-5 h-5 text-sky-400" />
          Career & Placement Goals
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1.5">
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider">Target Job Role</label>
            <input
              type="text"
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              placeholder="e.g. Software Engineer, Data Analyst"
              className="w-full bg-slate-900 border border-slate-700 focus:border-sky-500 text-white rounded-lg px-3 py-2 text-sm focus:outline-none"
            />
          </div>

          <div className="space-y-1.5">
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider">Experience Level</label>
            <select
              value={experienceLevel}
              onChange={(e) => setExperienceLevel(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 focus:border-sky-500 text-white rounded-lg px-3 py-2 text-sm focus:outline-none"
            >
              <option value="Entry Level">Entry Level (College Fresher)</option>
              <option value="Internship">Internship / Co-op</option>
              <option value="Associate">Associate (0-2 years)</option>
            </select>
          </div>
        </div>

        <div className="space-y-1.5">
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-1">
            <Code className="w-4 h-4 text-sky-400" />
            Technical Skills (Comma Separated)
          </label>
          <input
            type="text"
            value={skillsInput}
            onChange={(e) => setSkillsInput(e.target.value)}
            placeholder="Python, React, TypeScript, PostgreSQL, Data Structures"
            className="w-full bg-slate-900 border border-slate-700 focus:border-sky-500 text-white rounded-lg px-3 py-2 text-sm focus:outline-none"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1.5">
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-1">
              <Link2 className="w-4 h-4 text-sky-400" />
              GitHub Profile URL
            </label>
            <input
              type="url"
              value={githubUrl}
              onChange={(e) => setGithubUrl(e.target.value)}
              placeholder="https://github.com/username"
              className="w-full bg-slate-900 border border-slate-700 focus:border-sky-500 text-white rounded-lg px-3 py-2 text-sm focus:outline-none"
            />
          </div>

          <div className="space-y-1.5">
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider flex items-center gap-1">
              <Link2 className="w-4 h-4 text-sky-400" />
              LinkedIn Profile URL
            </label>
            <input
              type="url"
              value={linkedinUrl}
              onChange={(e) => setLinkedinUrl(e.target.value)}
              placeholder="https://linkedin.com/in/username"
              className="w-full bg-slate-900 border border-slate-700 focus:border-sky-500 text-white rounded-lg px-3 py-2 text-sm focus:outline-none"
            />
          </div>
        </div>

        <div className="pt-2 flex justify-end">
          <button
            type="submit"
            disabled={isSaving}
            className="bg-sky-600 hover:bg-sky-500 disabled:opacity-50 text-white font-medium px-6 py-2.5 rounded-lg transition text-sm flex items-center gap-2"
          >
            <Save className="w-4 h-4" />
            {isSaving ? "Saving Changes..." : "Save Profile"}
          </button>
        </div>
      </form>
    </div>
  );
}
