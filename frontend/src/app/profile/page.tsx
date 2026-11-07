"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import {
  User,
  Briefcase,
  Code,
  Link2,
  CheckCircle2,
  AlertCircle,
  Save,
  Award,
  Sparkles,
} from "lucide-react";

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
    } finally {
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
      <div className="py-20 text-center text-[#8993A0]">
        <div className="animate-spin w-8 h-8 border-2 border-[#123E63] border-t-transparent rounded-full mx-auto mb-4" />
        <p className="text-xs font-semibold">Loading student profile...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Top Profile Header Card */}
      <div className="bg-white rounded-2xl p-6 sm:p-7 shadow-card border border-[#E5E9EF] flex flex-col sm:flex-row sm:items-center justify-between gap-5">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-full bg-[#123E63] border-4 border-[#1E5685] flex items-center justify-center text-white text-xl font-bold shadow-md">
            {user?.full_name?.charAt(0).toUpperCase()}
          </div>
          <div>
            <h2 className="text-xl sm:text-2xl font-bold text-[#202B38] tracking-tight">
              {user?.full_name}
            </h2>
            <p className="text-xs sm:text-sm text-[#8993A0] mt-0.5">
              {user?.email} &bull; Student Account
            </p>
          </div>
        </div>

        <div className="px-3.5 py-1.5 rounded-full bg-[#FFF6E8] border border-[#F5A623]/30 text-[#F5A623] text-xs font-bold self-start sm:self-auto flex items-center gap-1.5">
          <Award className="w-3.5 h-3.5" />
          <span>Active Candidate</span>
        </div>
      </div>

      {statusMessage && (
        <div
          className={`p-4 rounded-xl flex items-center gap-2 text-xs font-semibold border ${
            statusMessage.type === "success"
              ? "bg-emerald-50 border-emerald-200 text-emerald-700"
              : "bg-red-50 border-red-200 text-red-700"
          }`}
        >
          {statusMessage.type === "success" ? (
            <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
          ) : (
            <AlertCircle className="w-4 h-4 text-red-600 shrink-0" />
          )}
          <span>{statusMessage.text}</span>
        </div>
      )}

      {/* Edit Profile Form */}
      <form onSubmit={handleSave} className="bg-white rounded-2xl p-6 sm:p-7 shadow-card border border-[#E5E9EF] space-y-6">
        <div className="flex items-center gap-2 border-b border-[#E5E9EF] pb-3">
          <Briefcase className="w-5 h-5 text-[#123E63]" />
          <div>
            <h3 className="text-base font-bold text-[#202B38]">Placement & Career Objectives</h3>
            <p className="text-xs text-[#8993A0]">Define your target role, experience level, and core skills to customize mock questions</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1.5">
            <label className="block text-[11px] font-bold text-[#8993A0] uppercase tracking-wider">
              Target Job Role
            </label>
            <input
              type="text"
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              placeholder="e.g. Software Engineer, Full Stack Developer"
              className="w-full bg-[#F8F9FA] border border-[#E5E9EF] focus:border-[#123E63] text-[#202B38] rounded-xl px-3.5 py-2.5 text-xs font-medium focus:outline-none transition"
            />
          </div>

          <div className="space-y-1.5">
            <label className="block text-[11px] font-bold text-[#8993A0] uppercase tracking-wider">
              Experience Level
            </label>
            <select
              value={experienceLevel}
              onChange={(e) => setExperienceLevel(e.target.value)}
              className="w-full bg-[#F8F9FA] border border-[#E5E9EF] focus:border-[#123E63] text-[#202B38] rounded-xl px-3.5 py-2.5 text-xs font-medium focus:outline-none transition"
            >
              <option value="Entry Level">Entry Level (College Fresher)</option>
              <option value="Internship">Internship / Co-op</option>
              <option value="Associate">Associate (0-2 years)</option>
            </select>
          </div>
        </div>

        <div className="space-y-1.5">
          <label className="block text-[11px] font-bold text-[#8993A0] uppercase tracking-wider flex items-center gap-1.5">
            <Code className="w-3.5 h-3.5 text-[#F5A623]" />
            Technical Stack & Skills (Comma Separated)
          </label>
          <input
            type="text"
            value={skillsInput}
            onChange={(e) => setSkillsInput(e.target.value)}
            placeholder="Python, Java, Data Structures, React, SQL, Algorithms"
            className="w-full bg-[#F8F9FA] border border-[#E5E9EF] focus:border-[#123E63] text-[#202B38] rounded-xl px-3.5 py-2.5 text-xs font-medium focus:outline-none transition"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-1.5">
            <label className="block text-[11px] font-bold text-[#8993A0] uppercase tracking-wider flex items-center gap-1.5">
              <Link2 className="w-3.5 h-3.5 text-[#123E63]" />
              GitHub Profile URL
            </label>
            <input
              type="url"
              value={githubUrl}
              onChange={(e) => setGithubUrl(e.target.value)}
              placeholder="https://github.com/username"
              className="w-full bg-[#F8F9FA] border border-[#E5E9EF] focus:border-[#123E63] text-[#202B38] rounded-xl px-3.5 py-2.5 text-xs font-medium focus:outline-none transition"
            />
          </div>

          <div className="space-y-1.5">
            <label className="block text-[11px] font-bold text-[#8993A0] uppercase tracking-wider flex items-center gap-1.5">
              <Link2 className="w-3.5 h-3.5 text-[#123E63]" />
              LinkedIn Profile URL
            </label>
            <input
              type="url"
              value={linkedinUrl}
              onChange={(e) => setLinkedinUrl(e.target.value)}
              placeholder="https://linkedin.com/in/username"
              className="w-full bg-[#F8F9FA] border border-[#E5E9EF] focus:border-[#123E63] text-[#202B38] rounded-xl px-3.5 py-2.5 text-xs font-medium focus:outline-none transition"
            />
          </div>
        </div>

        <div className="pt-3 flex justify-end">
          <button
            type="submit"
            disabled={isSaving}
            className="bg-[#123E63] hover:bg-[#0D3557] disabled:opacity-50 text-white font-bold px-6 py-2.5 rounded-xl transition text-xs shadow-md flex items-center gap-2"
          >
            <Save className="w-4 h-4" />
            <span>{isSaving ? "Saving Changes..." : "Save Profile"}</span>
          </button>
        </div>
      </form>
    </div>
  );
}
