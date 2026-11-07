"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { apiFetch } from "@/lib/api";
import {
  Mail,
  KeyRound,
  AlertCircle,
  CheckCircle2,
  ArrowRight,
  ArrowLeft,
  ShieldCheck,
  User,
  Lock,
  Eye,
  EyeOff,
  Code2,
} from "lucide-react";

interface RecoveryStatus {
  smtp_configured: boolean;
  environment: string;
  dev_recovery_available: boolean;
}

export default function ForgotPasswordPage() {
  const [activeTab, setActiveTab] = useState<"email" | "dev">("email");
  const [statusChecked, setStatusChecked] = useState(false);
  const [recoveryStatus, setRecoveryStatus] = useState<RecoveryStatus | null>(null);

  // Email recovery state
  const [email, setEmail] = useState("");
  const [isEmailSubmitting, setIsEmailSubmitting] = useState(false);
  const [emailError, setEmailError] = useState<string | null>(null);
  const [emailSuccess, setEmailSuccess] = useState<string | null>(null);

  // Development recovery state
  const [devEmail, setDevEmail] = useState("");
  const [devFullName, setDevFullName] = useState("");
  const [devKey, setDevKey] = useState("InterviewReadyDev2026!");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isDevSubmitting, setIsDevSubmitting] = useState(false);
  const [devError, setDevError] = useState<string | null>(null);
  const [devSuccess, setDevSuccess] = useState<string | null>(null);

  useEffect(() => {
    async function checkStatus() {
      try {
        const data = await apiFetch<RecoveryStatus>("/auth/recovery-status");
        setRecoveryStatus(data);
        // If SMTP is not configured and dev recovery is available, default to dev mode
        if (!data.smtp_configured && data.dev_recovery_available) {
          setActiveTab("dev");
        }
      } catch {
        // Fallback to email tab
      } finally {
        setStatusChecked(true);
      }
    }
    checkStatus();
  }, []);

  const handleEmailSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setEmailError(null);
    setEmailSuccess(null);
    setIsEmailSubmitting(true);

    try {
      const response = await apiFetch<{ message: string }>("/auth/forgot-password", {
        method: "POST",
        body: JSON.stringify({ email: email.trim().toLowerCase() }),
      });
      setEmailSuccess(
        response.message ||
          "If an account is associated with this email address, a password reset link has been sent."
      );
    } catch (err: any) {
      setEmailError(
        err.message ||
          "Failed to request password reset. Please verify your connection and try again."
      );
    } finally {
      setIsEmailSubmitting(false);
    }
  };

  const handleDevSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setDevError(null);
    setDevSuccess(null);

    if (newPassword.length < 6) {
      setDevError("Password must be at least 6 characters in length.");
      return;
    }

    if (newPassword !== confirmPassword) {
      setDevError("Passwords do not match. Please ensure both password fields are identical.");
      return;
    }

    setIsDevSubmitting(true);

    try {
      const response = await apiFetch<{ message: string }>("/auth/dev-reset-password", {
        method: "POST",
        body: JSON.stringify({
          email: devEmail.trim().toLowerCase(),
          full_name: devFullName.trim(),
          dev_recovery_key: devKey.trim(),
          new_password: newPassword,
        }),
      });
      setDevSuccess(
        response.message ||
          "Password successfully updated via development recovery. You can now log in with your new password."
      );
    } catch (err: any) {
      setDevError(
        err.message ||
          "Failed to reset password in development mode. Please verify the identity information and try again."
      );
    } finally {
      setIsDevSubmitting(false);
    }
  };

  const isDevMinLength = newPassword.length >= 6;
  const isDevMatch = newPassword.length > 0 && newPassword === confirmPassword;

  return (
    <div className="w-full">
      <div className="bg-white rounded-2xl p-8 shadow-card border border-[#E5E9EF] space-y-6">
        {/* Brand Icon & Heading */}
        <div className="text-center space-y-2">
          <div className="w-16 h-16 rounded-full bg-[#123E63] border-4 border-[#1E5685] flex items-center justify-center mx-auto shadow-md mb-2">
            <div className="w-10 h-10 rounded-full bg-white flex items-center justify-center text-[#123E63]">
              <KeyRound className="w-6 h-6 stroke-[2.2]" />
            </div>
          </div>
          <h2 className="text-2xl font-extrabold text-[#202B38] tracking-tight">Forgot Password?</h2>
          <p className="text-[#8993A0] text-xs max-w-sm mx-auto">
            Choose your preferred recovery method to reset your InterviewReady AI account password.
          </p>
        </div>

        {/* Development vs Email Recovery Tabs (Available in Development Mode) */}
        {recoveryStatus?.dev_recovery_available && (
          <div className="flex rounded-xl bg-[#F1F3F6] p-1 border border-[#E5E9EF]">
            <button
              type="button"
              onClick={() => {
                setActiveTab("email");
                setEmailError(null);
              }}
              className={`flex-1 py-2 text-xs font-bold rounded-lg transition flex items-center justify-center gap-1.5 ${
                activeTab === "email"
                  ? "bg-white text-[#123E63] shadow-xs"
                  : "text-[#8993A0] hover:text-[#202B38]"
              }`}
            >
              <Mail className="w-3.5 h-3.5" />
              <span>Email Reset Link</span>
            </button>

            <button
              type="button"
              onClick={() => {
                setActiveTab("dev");
                setDevError(null);
                // Pre-fill email from email tab if entered
                if (email && !devEmail) setDevEmail(email);
              }}
              className={`flex-1 py-2 text-xs font-bold rounded-lg transition flex items-center justify-center gap-1.5 ${
                activeTab === "dev"
                  ? "bg-[#123E63] text-white shadow-xs"
                  : "text-[#8993A0] hover:text-[#202B38]"
              }`}
            >
              <Code2 className="w-3.5 h-3.5 text-[#F5A623]" />
              <span>Local Dev Recovery</span>
              <span className="px-1.5 py-0.2 rounded bg-[#F5A623] text-white text-[9px] font-black uppercase">
                Dev
              </span>
            </button>
          </div>
        )}

        {/* ----------------- TAB 1: EMAIL RECOVERY (SMTP) ----------------- */}
        {activeTab === "email" && (
          <div className="space-y-4">
            {/* Informational banner if SMTP is unconfigured */}
            {recoveryStatus && !recoveryStatus.smtp_configured && (
              <div className="bg-[#FFF6E8] border border-[#F5A623]/40 text-[#734800] p-3.5 rounded-xl text-xs space-y-1.5">
                <div className="flex items-center gap-2 font-bold text-xs text-[#202B38]">
                  <AlertCircle className="w-4 h-4 text-[#F5A623]" />
                  <span>SMTP Email Delivery Unconfigured</span>
                </div>
                <p className="text-[11px] leading-relaxed">
                  SMTP credentials are not configured in your local environment. In development mode, you can safely recover your account using the{" "}
                  <button
                    type="button"
                    onClick={() => {
                      setActiveTab("dev");
                      if (email && !devEmail) setDevEmail(email);
                    }}
                    className="font-bold underline text-[#123E63] hover:text-[#F5A623]"
                  >
                    Local Dev Recovery
                  </button>{" "}
                  option.
                </p>
              </div>
            )}

            {emailError && (
              <div className="bg-red-50 border border-red-200 text-red-600 p-3 rounded-xl flex items-start gap-2.5 text-xs">
                <AlertCircle className="w-4 h-4 shrink-0 text-red-500 mt-0.5" />
                <div className="space-y-1.5">
                  <span className="font-semibold block">Password Recovery Notice</span>
                  <span className="text-[11px] leading-relaxed block">{emailError}</span>
                  {recoveryStatus?.dev_recovery_available && (
                    <button
                      type="button"
                      onClick={() => {
                        setActiveTab("dev");
                        if (email && !devEmail) setDevEmail(email);
                      }}
                      className="inline-flex items-center gap-1 font-bold text-xs text-[#123E63] hover:text-[#0D3557] underline mt-1"
                    >
                      <span>Switch to Local Dev Recovery</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  )}
                </div>
              </div>
            )}

            {emailSuccess ? (
              <div className="space-y-5">
                <div className="bg-emerald-50 border border-emerald-200 text-emerald-800 p-4 rounded-xl flex items-start gap-3 text-xs">
                  <CheckCircle2 className="w-5 h-5 shrink-0 text-emerald-600 mt-0.5" />
                  <div className="space-y-1">
                    <span className="font-bold text-sm block">Check Your Inbox</span>
                    <p className="text-emerald-700 leading-relaxed text-xs">
                      {emailSuccess}
                    </p>
                    <p className="text-[11px] text-emerald-600/80 mt-1">
                      The recovery link will expire in 15 minutes. Be sure to check your spam or junk folder if you don&apos;t see it shortly.
                    </p>
                  </div>
                </div>

                <div className="space-y-3 pt-2">
                  <button
                    type="button"
                    onClick={() => {
                      setEmailSuccess(null);
                      setEmail("");
                    }}
                    className="w-full bg-[#F8F9FA] hover:bg-[#E5E9EF] text-[#202B38] font-bold py-2.5 rounded-xl transition text-xs border border-[#E5E9EF]"
                  >
                    Send to a different email
                  </button>

                  <Link
                    href="/login"
                    className="w-full bg-[#123E63] hover:bg-[#0D3557] text-white font-bold py-3 rounded-xl transition text-xs shadow-md flex items-center justify-center gap-2"
                  >
                    <ArrowLeft className="w-4 h-4" />
                    <span>Return to Sign In</span>
                  </Link>
                </div>
              </div>
            ) : (
              <form onSubmit={handleEmailSubmit} className="space-y-4">
                <div className="space-y-1.5">
                  <label className="block text-[11px] font-bold text-[#8993A0] uppercase tracking-wider">
                    Student Email Address
                  </label>
                  <div className="relative">
                    <Mail className="w-4 h-4 text-[#8993A0] absolute left-3.5 top-3" />
                    <input
                      type="email"
                      required
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="student@college.edu"
                      className="w-full bg-[#F8F9FA] border border-[#E5E9EF] focus:border-[#123E63] text-[#202B38] rounded-xl pl-10 pr-4 py-2.5 text-xs font-medium focus:outline-none transition"
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={isEmailSubmitting || !email.trim()}
                  className="w-full bg-[#123E63] hover:bg-[#0D3557] disabled:opacity-50 text-white font-bold py-3 rounded-xl transition text-xs shadow-md flex items-center justify-center gap-2 mt-2"
                >
                  <span>{isEmailSubmitting ? "Generating Secure Link..." : "Send Reset Link"}</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </form>
            )}
          </div>
        )}

        {/* ----------------- TAB 2: LOCAL DEV RECOVERY (NO SMTP) ----------------- */}
        {activeTab === "dev" && (
          <div className="space-y-4">
            <div className="bg-[#123E63]/5 border border-[#123E63]/20 rounded-xl p-3.5 text-xs space-y-1">
              <div className="flex items-center gap-1.5 font-bold text-[#123E63]">
                <ShieldCheck className="w-4 h-4 text-[#F5A623]" />
                <span>Identity Verification Required</span>
              </div>
              <p className="text-[11px] text-[#505D6F] leading-relaxed">
                To prevent unauthorized password resets in development without email, you must verify both the account holder&apos;s registered full name and the local server recovery authorization key.
              </p>
            </div>

            {devError && (
              <div className="bg-red-50 border border-red-200 text-red-600 p-3 rounded-xl flex items-start gap-2.5 text-xs">
                <AlertCircle className="w-4 h-4 shrink-0 text-red-500 mt-0.5" />
                <div className="space-y-1">
                  <span className="font-semibold block">Recovery Verification Failed</span>
                  <span className="text-[11px] leading-relaxed block">{devError}</span>
                </div>
              </div>
            )}

            {devSuccess ? (
              <div className="space-y-5">
                <div className="bg-emerald-50 border border-emerald-200 text-emerald-800 p-4 rounded-xl flex items-start gap-3 text-xs">
                  <CheckCircle2 className="w-5 h-5 shrink-0 text-emerald-600 mt-0.5" />
                  <div className="space-y-1">
                    <span className="font-bold text-sm block">Password Updated Successfully!</span>
                    <p className="text-emerald-700 leading-relaxed text-xs">
                      {devSuccess}
                    </p>
                  </div>
                </div>

                <div className="pt-2">
                  <Link
                    href="/login"
                    className="w-full bg-[#123E63] hover:bg-[#0D3557] text-white font-bold py-3 rounded-xl transition text-xs shadow-md flex items-center justify-center gap-2"
                  >
                    <span>Sign In with New Password</span>
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>
              </div>
            ) : (
              <form onSubmit={handleDevSubmit} className="space-y-3.5">
                {/* Email Address */}
                <div className="space-y-1">
                  <label className="block text-[11px] font-bold text-[#8993A0] uppercase tracking-wider">
                    Registered Student Email
                  </label>
                  <div className="relative">
                    <Mail className="w-4 h-4 text-[#8993A0] absolute left-3.5 top-3" />
                    <input
                      type="email"
                      required
                      value={devEmail}
                      onChange={(e) => setDevEmail(e.target.value)}
                      placeholder="student@college.edu"
                      className="w-full bg-[#F8F9FA] border border-[#E5E9EF] focus:border-[#123E63] text-[#202B38] rounded-xl pl-10 pr-4 py-2.5 text-xs font-medium focus:outline-none transition"
                    />
                  </div>
                </div>

                {/* Account Full Name (Identity Verification) */}
                <div className="space-y-1">
                  <label className="block text-[11px] font-bold text-[#8993A0] uppercase tracking-wider">
                    Full Name (Identity Verification)
                  </label>
                  <div className="relative">
                    <User className="w-4 h-4 text-[#8993A0] absolute left-3.5 top-3" />
                    <input
                      type="text"
                      required
                      value={devFullName}
                      onChange={(e) => setDevFullName(e.target.value)}
                      placeholder="Exact name registered on account"
                      className="w-full bg-[#F8F9FA] border border-[#E5E9EF] focus:border-[#123E63] text-[#202B38] rounded-xl pl-10 pr-4 py-2.5 text-xs font-medium focus:outline-none transition"
                    />
                  </div>
                </div>

                {/* Development Recovery Key */}
                <div className="space-y-1">
                  <label className="block text-[11px] font-bold text-[#8993A0] uppercase tracking-wider">
                    Development Recovery Key
                  </label>
                  <div className="relative">
                    <KeyRound className="w-4 h-4 text-[#8993A0] absolute left-3.5 top-3" />
                    <input
                      type="text"
                      required
                      value={devKey}
                      onChange={(e) => setDevKey(e.target.value)}
                      placeholder="Configured in server .env (DEV_RECOVERY_KEY)"
                      className="w-full bg-[#F8F9FA] border border-[#E5E9EF] focus:border-[#123E63] text-[#202B38] rounded-xl pl-10 pr-4 py-2.5 text-xs font-mono font-medium focus:outline-none transition"
                    />
                  </div>
                </div>

                {/* New Password */}
                <div className="space-y-1">
                  <label className="block text-[11px] font-bold text-[#8993A0] uppercase tracking-wider">
                    New Password
                  </label>
                  <div className="relative">
                    <Lock className="w-4 h-4 text-[#8993A0] absolute left-3.5 top-3" />
                    <input
                      type={showPassword ? "text" : "password"}
                      required
                      minLength={6}
                      value={newPassword}
                      onChange={(e) => setNewPassword(e.target.value)}
                      placeholder="At least 6 characters"
                      className="w-full bg-[#F8F9FA] border border-[#E5E9EF] focus:border-[#123E63] text-[#202B38] rounded-xl pl-10 pr-10 py-2.5 text-xs font-medium focus:outline-none transition"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-2.5 text-[#8993A0] hover:text-[#202B38] transition p-0.5"
                      aria-label={showPassword ? "Hide password" : "Show password"}
                    >
                      {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                </div>

                {/* Confirm New Password */}
                <div className="space-y-1">
                  <label className="block text-[11px] font-bold text-[#8993A0] uppercase tracking-wider">
                    Confirm New Password
                  </label>
                  <div className="relative">
                    <Lock className="w-4 h-4 text-[#8993A0] absolute left-3.5 top-3" />
                    <input
                      type={showConfirmPassword ? "text" : "password"}
                      required
                      minLength={6}
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      placeholder="Re-enter your new password"
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

                {/* Validation Checklist */}
                <div className="bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl p-2.5 space-y-1 text-[11px]">
                  <div className={`flex items-center gap-1.5 ${isDevMinLength ? "text-emerald-600 font-semibold" : "text-[#8993A0]"}`}>
                    <CheckCircle2 className={`w-3.5 h-3.5 ${isDevMinLength ? "text-emerald-500" : "text-gray-300"}`} />
                    <span>Minimum 6 characters long</span>
                  </div>
                  <div className={`flex items-center gap-1.5 ${isDevMatch ? "text-emerald-600 font-semibold" : "text-[#8993A0]"}`}>
                    <CheckCircle2 className={`w-3.5 h-3.5 ${isDevMatch ? "text-emerald-500" : "text-gray-300"}`} />
                    <span>Passwords match</span>
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={isDevSubmitting || !isDevMinLength || !isDevMatch || !devEmail || !devFullName}
                  className="w-full bg-[#123E63] hover:bg-[#0D3557] disabled:opacity-50 text-white font-bold py-3 rounded-xl transition text-xs shadow-md flex items-center justify-center gap-2 mt-2"
                >
                  <span>{isDevSubmitting ? "Verifying & Updating..." : "Verify Identity & Reset Password"}</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              </form>
            )}
          </div>
        )}

        {/* Back to Sign In Footer */}
        <div className="pt-2 text-center text-xs text-[#8993A0] border-t border-[#E5E9EF] flex items-center justify-center gap-1">
          <span>Remember your password?</span>
          <Link
            href="/login"
            className="text-[#123E63] hover:text-[#F5A623] font-bold transition inline-flex items-center gap-1"
          >
            <span>Sign in</span>
          </Link>
        </div>
      </div>
    </div>
  );
}
