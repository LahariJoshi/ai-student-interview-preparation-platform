"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { LogIn, Mail, Lock, AlertCircle } from "lucide-react";

export default function LoginPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      await login(email, password);
      router.push("/profile");
    } catch (err: any) {
      setError(err.message || "Failed to sign in. Please check your credentials.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-md mx-auto py-12">
      <div className="glass-card p-8 space-y-6">
        <div className="text-center space-y-2">
          <div className="w-12 h-12 bg-sky-950/80 border border-sky-800 rounded-xl flex items-center justify-center mx-auto text-sky-400">
            <LogIn className="w-6 h-6" />
          </div>
          <h2 className="text-2xl font-bold text-white">Student Login</h2>
          <p className="text-slate-400 text-sm">Sign in to access your interview preparation dashboard</p>
        </div>

        {error && (
          <div className="bg-red-950/80 border border-red-800 text-red-300 p-3 rounded-lg flex items-start gap-2 text-sm">
            <AlertCircle className="w-5 h-5 shrink-0 text-red-400 mt-0.5" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1.5">
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider">Email Address</label>
            <div className="relative">
              <Mail className="w-5 h-5 text-slate-500 absolute left-3 top-2.5" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="student@college.edu"
                className="w-full bg-slate-900 border border-slate-700 focus:border-sky-500 text-white rounded-lg pl-10 pr-4 py-2 text-sm focus:outline-none transition"
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider">Password</label>
            <div className="relative">
              <Lock className="w-5 h-5 text-slate-500 absolute left-3 top-2.5" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full bg-slate-900 border border-slate-700 focus:border-sky-500 text-white rounded-lg pl-10 pr-4 py-2 text-sm focus:outline-none transition"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full bg-sky-600 hover:bg-sky-500 disabled:opacity-50 text-white font-medium py-2.5 rounded-lg transition text-sm flex items-center justify-center gap-2"
          >
            {isSubmitting ? "Signing in..." : "Sign In"}
          </button>
        </form>

        <p className="text-center text-xs text-slate-400">
          Don't have a student account?{" "}
          <Link href="/register" className="text-sky-400 hover:underline font-medium">
            Register here
          </Link>
        </p>
      </div>
    </div>
  );
}
