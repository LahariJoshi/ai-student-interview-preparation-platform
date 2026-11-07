"use client";

import React, { useState, useEffect, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { apiFetch } from "@/lib/api";
import {
  Lock,
  CheckCircle2,
  AlertCircle,
  ArrowRight,
  Eye,
  EyeOff,
  ShieldCheck,
  RotateCcw,
} from "lucide-react";

function ResetPasswordContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get("token");

  const [isVerifyingToken, setIsVerifyingToken] = useState(true);
  const [tokenError, setTokenError] = useState<string | null>(null);

  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [isSuccess, setIsSuccess] = useState(false);

  useEffect(() => {
    async function verifyToken() {
      if (!token) {
        setTokenError("Missing password reset token. Please request a new recovery link.");
        setIsVerifyingToken(false);
        return;
      }

      try {
        await apiFetch<{ valid: boolean }>(
          `/auth/verify-reset-token?token=${encodeURIComponent(token)}`
        );
        setTokenError(null);
      } catch (err: any) {
        setTokenError(
          err.message || "This password reset link is invalid or has expired. Please request a new one."
        );
      } finally {
        setIsVerifyingToken(false);
      }
    }

    verifyToken();
  }, [token]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitError(null);

    if (newPassword.length < 6) {
      setSubmitError("Password must be at least 6 characters in length.");
      return;
    }

    if (newPassword !== confirmPassword) {
      setSubmitError("Passwords do not match. Please ensure both fields are identical.");
      return;
    }

    if (!token) {
      setSubmitError("Reset token is missing. Please restart the recovery process.");
      return;
    }

    setIsSubmitting(true);

    try {
      await apiFetch<{ message: string }>("/auth/reset-password", {
        method: "POST",
        body: JSON.stringify({
          token,
          new_password: newPassword,
        }),
      });
      setIsSuccess(true);
    } catch (err: any) {
      setSubmitError(
        err.message || "Failed to reset password. The link may have expired. Please try again."
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  const isMinLength = newPassword.length >= 6;
  const isMatch = newPassword.length > 0 && newPassword === confirmPassword;

  if (isVerifyingToken) {
    return (
      <div className="bg-white rounded-2xl p-8 shadow-card border border-[#E5E9EF] text-center space-y-4">
        <div className="animate-spin w-8 h-8 border-3 border-[#123E63] border-t-transparent rounded-full mx-auto" />
        <p className="text-xs font-semibold text-[#8993A0]">
          Verifying secure password reset link...
        </p>
      </div>
    );
  }

  if (tokenError) {
    return (
      <div className="bg-white rounded-2xl p-8 shadow-card border border-[#E5E9EF] space-y-6 text-center">
        <div className="w-16 h-16 rounded-full bg-red-50 border-4 border-red-100 flex items-center justify-center mx-auto text-red-500 shadow-sm">
          <AlertCircle className="w-8 h-8" />
        </div>
        <div className="space-y-1.5">
          <h2 className="text-xl font-extrabold text-[#202B38] tracking-tight">
            Invalid or Expired Link
          </h2>
          <p className="text-xs text-[#8993A0] max-w-sm mx-auto leading-relaxed">
            {tokenError}
          </p>
        </div>
        <div className="space-y-3 pt-2">
          <Link
            href="/forgot-password"
            className="w-full bg-[#123E63] hover:bg-[#0D3557] text-white font-bold py-3 rounded-xl transition text-xs shadow-md flex items-center justify-center gap-2"
          >
            <RotateCcw className="w-4 h-4" />
            <span>Request a New Reset Link</span>
          </Link>
          <Link
            href="/login"
            className="block text-xs font-semibold text-[#8993A0] hover:text-[#202B38] transition"
          >
            Back to Sign In
          </Link>
        </div>
      </div>
    );
  }

  if (isSuccess) {
    return (
      <div className="bg-white rounded-2xl p-8 shadow-card border border-[#E5E9EF] space-y-6 text-center">
        <div className="w-16 h-16 rounded-full bg-emerald-50 border-4 border-emerald-100 flex items-center justify-center mx-auto text-emerald-600 shadow-sm">
          <CheckCircle2 className="w-8 h-8" />
        </div>
        <div className="space-y-2">
          <h2 className="text-2xl font-extrabold text-[#202B38] tracking-tight">
            Password Reset Complete!
          </h2>
          <p className="text-xs text-[#8993A0] max-w-sm mx-auto leading-relaxed">
            Your password has been successfully updated. You can now sign in to your InterviewReady AI workspace with your new password.
          </p>
        </div>
        <div className="pt-2">
          <Link
            href="/login"
            className="w-full bg-[#123E63] hover:bg-[#0D3557] text-white font-bold py-3 rounded-xl transition text-xs shadow-md flex items-center justify-center gap-2"
          >
            <span>Sign In to Workspace</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full">
      <div className="bg-white rounded-2xl p-8 shadow-card border border-[#E5E9EF] space-y-6">
        <div className="text-center space-y-2">
          <div className="w-16 h-16 rounded-full bg-[#123E63] border-4 border-[#1E5685] flex items-center justify-center mx-auto shadow-md mb-2">
            <div className="w-10 h-10 rounded-full bg-white flex items-center justify-center text-[#123E63]">
              <ShieldCheck className="w-6 h-6 stroke-[2.2]" />
            </div>
          </div>
          <h2 className="text-2xl font-extrabold text-[#202B38] tracking-tight">Create New Password</h2>
          <p className="text-[#8993A0] text-xs">
            Choose a strong password to safeguard your student preparation account
          </p>
        </div>

        {submitError && (
          <div className="bg-red-50 border border-red-200 text-red-600 p-3 rounded-xl flex items-start gap-2.5 text-xs">
            <AlertCircle className="w-4 h-4 shrink-0 text-red-500 mt-0.5" />
            <span>{submitError}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1.5">
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

          <div className="space-y-1.5">
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
          <div className="bg-[#F8F9FA] border border-[#E5E9EF] rounded-xl p-3 space-y-1.5 text-[11px]">
            <div className={`flex items-center gap-2 ${isMinLength ? "text-emerald-600 font-semibold" : "text-[#8993A0]"}`}>
              <CheckCircle2 className={`w-3.5 h-3.5 ${isMinLength ? "text-emerald-500" : "text-gray-300"}`} />
              <span>Minimum 6 characters long</span>
            </div>
            <div className={`flex items-center gap-2 ${isMatch ? "text-emerald-600 font-semibold" : "text-[#8993A0]"}`}>
              <CheckCircle2 className={`w-3.5 h-3.5 ${isMatch ? "text-emerald-500" : "text-gray-300"}`} />
              <span>Passwords match</span>
            </div>
          </div>

          <button
            type="submit"
            disabled={isSubmitting || !isMinLength || !isMatch}
            className="w-full bg-[#123E63] hover:bg-[#0D3557] disabled:opacity-50 text-white font-bold py-3 rounded-xl transition text-xs shadow-md flex items-center justify-center gap-2 mt-2"
          >
            <span>{isSubmitting ? "Updating Password..." : "Save & Reset Password"}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>

        <div className="pt-2 text-center text-xs text-[#8993A0] border-t border-[#E5E9EF]">
          Back to{" "}
          <Link href="/login" className="text-[#123E63] hover:text-[#F5A623] font-bold">
            Sign In
          </Link>
        </div>
      </div>
    </div>
  );
}

export default function ResetPasswordPage() {
  return (
    <Suspense
      fallback={
        <div className="bg-white rounded-2xl p-8 shadow-card border border-[#E5E9EF] text-center space-y-4">
          <div className="animate-spin w-8 h-8 border-3 border-[#123E63] border-t-transparent rounded-full mx-auto" />
          <p className="text-xs font-semibold text-[#8993A0]">Loading...</p>
        </div>
      }
    >
      <ResetPasswordContent />
    </Suspense>
  );
}
