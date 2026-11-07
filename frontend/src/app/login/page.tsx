"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { Mail, Lock, AlertCircle, ArrowRight, User, Eye, EyeOff } from "lucide-react";

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      await login(email, password);
      router.push("/dashboard");
    } catch (err: any) {
      setError(err.message || "Failed to sign in. Please check your credentials.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="w-full">
      <div className="bg-white rounded-2xl p-8 shadow-card border border-[#E5E9EF] space-y-6">
        {/* Brand Icon & Heading */}
        <div className="text-center space-y-2">
          <div className="w-16 h-16 rounded-full bg-[#123E63] border-4 border-[#1E5685] flex items-center justify-center mx-auto shadow-md mb-2">
            <div className="w-10 h-10 rounded-full bg-white flex items-center justify-center text-[#123E63]">
              <User className="w-6 h-6 stroke-[2.2]" />
            </div>
          </div>
          <h2 className="text-2xl font-extrabold text-[#202B38] tracking-tight">Student Login</h2>
          <p className="text-[#8993A0] text-xs">
            Sign in to access your AI interview preparation workspace
          </p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-600 p-3 rounded-xl flex items-start gap-2.5 text-xs">
            <AlertCircle className="w-4 h-4 shrink-0 text-red-500 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1.5">
            <label className="block text-[11px] font-bold text-[#8993A0] uppercase tracking-wider">
              Email Address
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

          <div className="space-y-1.5">
            <div className="flex items-center justify-between">
              <label className="block text-[11px] font-bold text-[#8993A0] uppercase tracking-wider">
                Password
              </label>
              <Link
                href="/forgot-password"
                className="text-[11px] font-semibold text-[#123E63] hover:text-[#F5A623] transition focus:outline-none focus:underline"
              >
                Forgot Password?
              </Link>
            </div>
            <div className="relative">
              <Lock className="w-4 h-4 text-[#8993A0] absolute left-3.5 top-3" />
              <input
                type={showPassword ? "text" : "password"}
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
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

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full bg-[#123E63] hover:bg-[#0D3557] disabled:opacity-50 text-white font-bold py-3 rounded-xl transition text-xs shadow-md flex items-center justify-center gap-2 mt-2"
          >
            <span>{isSubmitting ? "Authenticating..." : "Sign In to Workspace"}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>

        <div className="pt-2 text-center text-xs text-[#8993A0] border-t border-[#E5E9EF]">
          Don&apos;t have a student account?{" "}
          <Link href="/register" className="text-[#F5A623] hover:text-[#E09212] font-bold">
            Register here
          </Link>
        </div>
      </div>
    </div>
  );
}
