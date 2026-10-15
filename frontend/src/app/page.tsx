"use client";

import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { Sparkles, ArrowRight, UserCheck, ShieldCheck, Target, Code, Cpu } from "lucide-react";

export default function HomePage() {
  const { user } = useAuth();

  return (
    <div className="space-y-12 py-8">
      {/* Hero Section */}
      <section className="text-center space-y-6 max-w-3xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-950/80 border border-sky-800 text-sky-300 text-xs font-semibold">
          <Sparkles className="w-4 h-4 text-sky-400" />
          Placement & Technical Interview Prep Platform
        </div>
        <h1 className="text-4xl md:text-5xl font-extrabold text-white tracking-tight leading-tight">
          Master Your Placement Interviews with <span className="text-sky-400">AI Guidance</span>
        </h1>
        <p className="text-slate-400 text-base md:text-lg leading-relaxed">
          Designed specifically for students to identify weaknesses, improve resume ATS quality, practice coding problems, conduct AI mock interviews, and track readiness.
        </p>

        <div className="flex items-center justify-center gap-4 pt-2">
          {user ? (
            <Link
              href="/profile"
              className="inline-flex items-center gap-2 bg-sky-600 hover:bg-sky-500 text-white font-medium px-6 py-3 rounded-xl transition"
            >
              Go to Your Profile
              <ArrowRight className="w-5 h-5" />
            </Link>
          ) : (
            <>
              <Link
                href="/register"
                className="inline-flex items-center gap-2 bg-sky-600 hover:bg-sky-500 text-white font-medium px-6 py-3 rounded-xl transition"
              >
                Register as Student
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link
                href="/login"
                className="inline-flex items-center gap-2 bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium px-6 py-3 rounded-xl border border-slate-700 transition"
              >
                Sign In
              </Link>
            </>
          )}
        </div>
      </section>

      {/* Core Features Grid */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-6">
        <div className="glass-card p-6 space-y-3">
          <div className="w-10 h-10 rounded-lg bg-sky-900/50 border border-sky-700 flex items-center justify-center text-sky-400">
            <UserCheck className="w-5 h-5" />
          </div>
          <h3 className="text-lg font-bold text-white">Student Profile & Goal Setting</h3>
          <p className="text-slate-400 text-sm">
            Define your target role, experience level, tech stack, and target companies to personalize your prep path.
          </p>
        </div>

        <div className="glass-card p-6 space-y-3">
          <div className="w-10 h-10 rounded-lg bg-indigo-900/50 border border-indigo-700 flex items-center justify-center text-indigo-400">
            <Target className="w-5 h-5" />
          </div>
          <h3 className="text-lg font-bold text-white">Multi-Factor ATS Analysis</h3>
          <p className="text-slate-400 text-sm">
            Multi-dimensional evaluation measuring formatting, keyword match, impact metrics, and semantic alignment.
          </p>
        </div>

        <div className="glass-card p-6 space-y-3">
          <div className="w-10 h-10 rounded-lg bg-emerald-900/50 border border-emerald-700 flex items-center justify-center text-emerald-400">
            <Code className="w-5 h-5" />
          </div>
          <h3 className="text-lg font-bold text-white">Coding Assessment Sandbox</h3>
          <p className="text-slate-400 text-sm">
            Practice technical problem-solving with Monaco editor and instant test case execution.
          </p>
        </div>

        <div className="glass-card p-6 space-y-3 md:col-span-3">
          <div className="flex items-center justify-between">
            <div className="w-10 h-10 rounded-lg bg-amber-900/50 border border-amber-700 flex items-center justify-center text-amber-400">
              <Sparkles className="w-5 h-5" />
            </div>
            <Link
              href="/interview"
              className="inline-flex items-center gap-1.5 text-xs text-sky-400 hover:text-sky-300 font-semibold"
            >
              Start Session &rarr;
            </Link>
          </div>
          <h3 className="text-lg font-bold text-white">Interactive AI Mock Interview Studio</h3>
          <p className="text-slate-400 text-sm">
            Realistic mock interview simulations for SDE, Python, Java, and AI roles. Features voice answer mode, transparent rubric evaluations, delivery metrics, and customized revision roadmaps.
          </p>
        </div>
      </section>
    </div>
  );
}
