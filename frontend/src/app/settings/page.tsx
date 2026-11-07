"use client";

import React, { useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { apiFetch } from "@/lib/api";
import {
  Settings,
  Bell,
  Lock,
  User,
  Shield,
  CheckCircle2,
  Save,
  AlertCircle,
  Eye,
  EyeOff,
  KeyRound,
} from "lucide-react";

export default function SettingsPage() {
  const { user } = useAuth();
  const [emailAlerts, setEmailAlerts] = useState(true);
  const [weeklyReport, setWeeklyReport] = useState(true);
  const [isSaved, setIsSaved] = useState(false);

  // Change password state
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showCurrentPassword, setShowCurrentPassword] = useState(false);
  const [showNewPassword, setShowNewPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isPasswordSubmitting, setIsPasswordSubmitting] = useState(false);
  const [passwordError, setPasswordError] = useState<string | null>(null);
  const [passwordSuccess, setPasswordSuccess] = useState<string | null>(null);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSaved(true);
    setTimeout(() => setIsSaved(false), 3000);
  };

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    setPasswordError(null);
    setPasswordSuccess(null);

    if (newPassword.length < 6) {
      setPasswordError("New password must be at least 6 characters in length.");
      return;
    }

    if (newPassword !== confirmPassword) {
      setPasswordError("New passwords do not match. Please verify both fields.");
      return;
    }

    setIsPasswordSubmitting(true);

    try {
      const response = await apiFetch<{ message: string }>("/auth/change-password", {
        method: "POST",
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      });
      setPasswordSuccess(response.message || "Your password has been changed successfully.");
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch (err: any) {
      setPasswordError(
        err.message || "Failed to change password. Please ensure your current password is correct."
      );
    } finally {
      setIsPasswordSubmitting(false);
    }
  };

  const isMinLength = newPassword.length >= 6;
  const isMatch = newPassword.length > 0 && newPassword === confirmPassword;

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Header */}
      <div>
        <h2 className="text-2xl sm:text-3xl font-extrabold text-[#202B38] tracking-tight">
          Application Settings
        </h2>
        <p className="text-xs sm:text-sm text-[#8993A0] mt-0.5">
          Configure notification preferences, preparation goals, and account security
        </p>
      </div>

      {isSaved && (
        <div className="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-700 flex items-center gap-2 text-xs font-semibold">
          <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          <span>Your preferences have been saved successfully!</span>
        </div>
      )}

      {/* Account Info */}
      <section className="bg-white rounded-2xl p-6 shadow-card border border-[#E5E9EF] space-y-4">
        <div className="flex items-center gap-2.5 pb-3 border-b border-[#E5E9EF]">
          <User className="w-5 h-5 text-[#123E63]" />
          <h3 className="text-base font-bold text-[#202B38]">Student Profile</h3>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
          <div>
            <label className="block text-[#8993A0] font-semibold mb-1">Full Name</label>
            <input
              type="text"
              readOnly
              value={user?.full_name || "Student User"}
              className="w-full px-3.5 py-2.5 rounded-xl border border-[#E5E9EF] bg-[#F8F9FA] text-[#202B38] font-medium"
            />
          </div>
          <div>
            <label className="block text-[#8993A0] font-semibold mb-1">Email Address</label>
            <input
              type="email"
              readOnly
              value={user?.email || "student@college.edu"}
              className="w-full px-3.5 py-2.5 rounded-xl border border-[#E5E9EF] bg-[#F8F9FA] text-[#202B38] font-medium"
            />
          </div>
        </div>
      </section>

      {/* Account Security & Password Management */}
      <section className="bg-white rounded-2xl p-6 shadow-card border border-[#E5E9EF] space-y-4">
        <div className="flex items-center gap-2.5 pb-3 border-b border-[#E5E9EF]">
          <Shield className="w-5 h-5 text-[#123E63]" />
          <div>
            <h3 className="text-base font-bold text-[#202B38]">Account Security & Password</h3>
            <p className="text-xs text-[#8993A0]">Update your account credentials using your current password</p>
          </div>
        </div>

        {passwordError && (
          <div className="p-3 rounded-xl bg-red-50 border border-red-200 text-red-600 flex items-start gap-2.5 text-xs">
            <AlertCircle className="w-4 h-4 text-red-500 shrink-0 mt-0.5" />
            <span>{passwordError}</span>
          </div>
        )}

        {passwordSuccess && (
          <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-700 flex items-center gap-2 text-xs font-semibold">
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
            <span>{passwordSuccess}</span>
          </div>
        )}

        <form onSubmit={handlePasswordChange} className="space-y-3.5 max-w-xl">
          {/* Current Password */}
          <div className="space-y-1">
            <label className="block text-[11px] font-bold text-[#8993A0] uppercase tracking-wider">
              Current Password
            </label>
            <div className="relative">
              <Lock className="w-4 h-4 text-[#8993A0] absolute left-3.5 top-3" />
              <input
                type={showCurrentPassword ? "text" : "password"}
                required
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                placeholder="Enter current password"
                className="w-full bg-[#F8F9FA] border border-[#E5E9EF] focus:border-[#123E63] text-[#202B38] rounded-xl pl-10 pr-10 py-2.5 text-xs font-medium focus:outline-none transition"
              />
              <button
                type="button"
                onClick={() => setShowCurrentPassword(!showCurrentPassword)}
                className="absolute right-3 top-2.5 text-[#8993A0] hover:text-[#202B38] transition p-0.5"
                aria-label={showCurrentPassword ? "Hide password" : "Show password"}
              >
                {showCurrentPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          {/* New Password */}
          <div className="space-y-1">
            <label className="block text-[11px] font-bold text-[#8993A0] uppercase tracking-wider">
              New Password
            </label>
            <div className="relative">
              <KeyRound className="w-4 h-4 text-[#8993A0] absolute left-3.5 top-3" />
              <input
                type={showNewPassword ? "text" : "password"}
                required
                minLength={6}
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                placeholder="At least 6 characters"
                className="w-full bg-[#F8F9FA] border border-[#E5E9EF] focus:border-[#123E63] text-[#202B38] rounded-xl pl-10 pr-10 py-2.5 text-xs font-medium focus:outline-none transition"
              />
              <button
                type="button"
                onClick={() => setShowNewPassword(!showNewPassword)}
                className="absolute right-3 top-2.5 text-[#8993A0] hover:text-[#202B38] transition p-0.5"
                aria-label={showNewPassword ? "Hide password" : "Show password"}
              >
                {showNewPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          {/* Confirm New Password */}
          <div className="space-y-1">
            <label className="block text-[11px] font-bold text-[#8993A0] uppercase tracking-wider">
              Confirm New Password
            </label>
            <div className="relative">
              <KeyRound className="w-4 h-4 text-[#8993A0] absolute left-3.5 top-3" />
              <input
                type={showConfirmPassword ? "text" : "password"}
                required
                minLength={6}
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="Re-enter new password"
                className="w-full bg-[#F8F9FA] border border-[#E5E9EF] focus:border-[#123E63] text-[#202B38] rounded-xl pl-10 pr-10 py-2.5 text-xs font-medium focus:outline-none transition"
              />
              <button
                type="button"
                onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                className="absolute right-3 top-2.5 text-[#8993A0] hover:text-[#202B38] transition p-0.5"
                aria-label={showConfirmPassword ? "Hide password" : "Show password"}
              >
                {showConfirmPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>

          {/* Password Validation Indicator */}
          {newPassword && (
            <div className="bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl p-2.5 space-y-1 text-[11px]">
              <div className={`flex items-center gap-1.5 ${isMinLength ? "text-emerald-600 font-semibold" : "text-[#8993A0]"}`}>
                <CheckCircle2 className={`w-3.5 h-3.5 ${isMinLength ? "text-emerald-500" : "text-gray-300"}`} />
                <span>Minimum 6 characters long</span>
              </div>
              <div className={`flex items-center gap-1.5 ${isMatch ? "text-emerald-600 font-semibold" : "text-[#8993A0]"}`}>
                <CheckCircle2 className={`w-3.5 h-3.5 ${isMatch ? "text-emerald-500" : "text-gray-300"}`} />
                <span>Passwords match</span>
              </div>
            </div>
          )}

          <div className="pt-1">
            <button
              type="submit"
              disabled={isPasswordSubmitting || !currentPassword || !isMinLength || !isMatch}
              className="px-5 py-2.5 rounded-xl bg-[#123E63] hover:bg-[#0D3557] disabled:opacity-50 text-white text-xs font-bold transition shadow-sm flex items-center gap-2"
            >
              <span>{isPasswordSubmitting ? "Updating..." : "Update Password"}</span>
            </button>
          </div>
        </form>
      </section>

      {/* Notifications */}
      <section className="bg-white rounded-2xl p-6 shadow-card border border-[#E5E9EF] space-y-4">
        <div className="flex items-center gap-2.5 pb-3 border-b border-[#E5E9EF]">
          <Bell className="w-5 h-5 text-[#F5A623]" />
          <h3 className="text-base font-bold text-[#202B38]">Notifications & Reminders</h3>
        </div>

        <div className="space-y-3">
          <label className="flex items-center justify-between p-3 rounded-xl border border-[#E5E9EF] bg-[#F8F9FA] cursor-pointer">
            <div>
              <p className="text-xs font-bold text-[#202B38]">Email Preparation Reminders</p>
              <p className="text-[11px] text-[#8993A0]">Receive daily coding challenges and practice prompts</p>
            </div>
            <input
              type="checkbox"
              checked={emailAlerts}
              onChange={(e) => setEmailAlerts(e.target.checked)}
              className="w-4 h-4 text-[#123E63] rounded border-gray-300 focus:ring-[#123E63]"
            />
          </label>

          <label className="flex items-center justify-between p-3 rounded-xl border border-[#E5E9EF] bg-[#F8F9FA] cursor-pointer">
            <div>
              <p className="text-xs font-bold text-[#202B38]">Weekly Readiness Report</p>
              <p className="text-[11px] text-[#8993A0]">Summary of your mock interview feedback and ATS score trends</p>
            </div>
            <input
              type="checkbox"
              checked={weeklyReport}
              onChange={(e) => setWeeklyReport(e.target.checked)}
              className="w-4 h-4 text-[#123E63] rounded border-gray-300 focus:ring-[#123E63]"
            />
          </label>
        </div>

        <div className="pt-2">
          <button
            onClick={handleSave}
            className="px-5 py-2.5 rounded-xl bg-[#123E63] hover:bg-[#0D3557] text-white text-xs font-bold transition shadow-sm flex items-center gap-2"
          >
            <Save className="w-4 h-4" />
            <span>Save Preferences</span>
          </button>
        </div>
      </section>
    </div>
  );
}
