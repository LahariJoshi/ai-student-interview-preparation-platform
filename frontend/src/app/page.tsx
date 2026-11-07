"use client";

import React from "react";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import {
  Sparkles,
  ArrowRight,
  FileSearch,
  Code2,
  Mic,
  Compass,
  BarChart3,
  CheckCircle2,
  Zap,
  Target,
  Brain,
  Layers,
  Award,
  ChevronRight,
  ShieldCheck,
  Terminal,
  Play,
  Volume2,
} from "lucide-react";

export default function PublicHomePage() {
  const { user } = useAuth();

  return (
    <div className="flex flex-col min-h-screen bg-[#F8FAFC]">
      {/* 1. Public Top Navigation Header */}
      <header className="sticky top-0 z-40 w-full bg-white/90 backdrop-blur-md border-b border-[#E5E9EF] transition-all">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
          {/* Logo & Brand */}
          <Link href="/" className="flex items-center gap-3 group">
            <div className="w-11 h-11 rounded-xl bg-[#0D3557] flex items-center justify-center text-white shadow-md group-hover:bg-[#123E63] transition">
              <Brain className="w-6 h-6 text-[#F5A623]" />
            </div>
            <div>
              <span className="text-xl font-black text-[#0D3557] tracking-tight">
                InterviewReady <span className="text-[#F5A623]">AI</span>
              </span>
              <span className="hidden sm:block text-[10px] text-[#8993A0] font-semibold uppercase tracking-wider">
                Student Interview Platform
              </span>
            </div>
          </Link>

          {/* Quick Jump Anchor Links */}
          <nav className="hidden md:flex items-center gap-8 text-sm font-semibold text-[#505D6F]">
            <a href="#features" className="hover:text-[#123E63] transition">
              Platform Features
            </a>
            <a href="#how-it-works" className="hover:text-[#123E63] transition">
              How It Works
            </a>
            <a href="#benefits" className="hover:text-[#123E63] transition">
              Benefits
            </a>
            <a href="#modules" className="hover:text-[#123E63] transition">
              Preparation Modules
            </a>
          </nav>

          {/* Auth Action Buttons */}
          <div className="flex items-center gap-3">
            {user ? (
              <div className="flex items-center gap-3">
                <Link
                  href="/dashboard"
                  className="px-5 py-2.5 rounded-xl bg-[#123E63] hover:bg-[#0D3557] text-white text-xs sm:text-sm font-bold shadow-md hover:shadow-lg transition flex items-center gap-2"
                >
                  <span>Go to Dashboard</span>
                  <ArrowRight className="w-4 h-4 text-[#F5A623]" />
                </Link>
              </div>
            ) : (
              <>
                <Link
                  href="/login"
                  className="px-4 py-2 sm:px-5 sm:py-2.5 rounded-xl text-xs sm:text-sm font-bold text-[#123E63] hover:text-[#0D3557] hover:bg-slate-100 transition"
                >
                  Sign In
                </Link>
                <Link
                  href="/register"
                  className="px-4 py-2 sm:px-5 sm:py-2.5 rounded-xl bg-[#F5A623] hover:bg-[#E09212] text-white text-xs sm:text-sm font-bold shadow-md hover:shadow-lg transition flex items-center gap-1.5"
                >
                  <span>Get Started</span>
                  <ArrowRight className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
                </Link>
              </>
            )}
          </div>
        </div>
      </header>

      {/* 2. Hero Section */}
      <section className="relative overflow-hidden pt-12 pb-20 lg:pt-20 lg:pb-28 bg-gradient-to-b from-[#F1F5F9] via-[#F8FAFC] to-white border-b border-[#E5E9EF]">
        {/* Subtle Decorative Background Elements */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full max-w-7xl h-96 bg-gradient-to-tr from-[#123E63]/5 via-[#F5A623]/10 to-transparent blur-3xl pointer-events-none" />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative">
          <div className="text-center max-w-3xl mx-auto space-y-6">
            {/* Pill Badge */}
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#123E63]/10 border border-[#123E63]/20 text-[#123E63] text-xs font-bold uppercase tracking-wider shadow-xs">
              <Sparkles className="w-4 h-4 text-[#F5A623]" />
              <span>AI-Powered Student Interview Preparation</span>
            </div>

            {/* Main Heading */}
            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-black text-[#0D3557] tracking-tight leading-[1.12]">
              Your AI-Powered Journey to{" "}
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#123E63] via-[#0D3557] to-[#F5A623]">
                Interview Success
              </span>
            </h1>

            {/* Description */}
            <p className="text-base sm:text-lg text-[#505D6F] font-normal leading-relaxed">
              Prepare smarter, identify your weaknesses, practice coding, analyze your resume, and experience AI-powered mock interviews. InterviewReady AI helps students build confidence and develop the skills needed to succeed in technical interviews.
            </p>

            {/* CTA Buttons */}
            <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link
                href="/register"
                className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-[#F5A623] hover:bg-[#E09212] text-white font-extrabold text-sm sm:text-base shadow-lg shadow-[#F5A623]/25 hover:shadow-xl transition flex items-center justify-center gap-2.5"
              >
                <span>Get Started</span>
                <ArrowRight className="w-5 h-5" />
              </Link>
              <Link
                href="/login"
                className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-[#0D3557] hover:bg-[#123E63] text-white font-extrabold text-sm sm:text-base shadow-md hover:shadow-lg transition flex items-center justify-center gap-2"
              >
                <span>Sign In</span>
                <ChevronRight className="w-4 h-4 text-[#BCD3E6]" />
              </Link>
            </div>

            {/* Trust Indicators */}
            <div className="pt-4 flex flex-wrap items-center justify-center gap-6 text-xs text-[#8993A0] font-medium">
              <span className="flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                Comprehensive ATS Analyzer
              </span>
              <span className="flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                Algorithmic Code Sandbox
              </span>
              <span className="flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                Interactive Voice Mock Interviews
              </span>
            </div>
          </div>

          {/* Product Visual Preview (Illustrating Platform Modules Without User Dashboard Data) */}
          <div className="mt-14 max-w-5xl mx-auto">
            <div className="bg-[#0D3557] rounded-3xl p-3 sm:p-5 shadow-2xl border-4 border-[#1E5685]/40 text-white relative overflow-hidden">
              {/* Window Bar Header */}
              <div className="flex items-center justify-between pb-3 px-3 border-b border-[#1E5685]/60 text-xs text-[#8AAEC8]">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 rounded-full bg-red-400/80" />
                  <div className="w-3 h-3 rounded-full bg-yellow-400/80" />
                  <div className="w-3 h-3 rounded-full bg-green-400/80" />
                  <span className="ml-2 font-mono text-[11px] text-[#BCD3E6]">
                    interviewready-ai-preview.app
                  </span>
                </div>
                <div className="flex items-center gap-2 font-mono text-[11px]">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                  <span>Interactive Preparation Engine Online</span>
                </div>
              </div>

              {/* Multi-Module Composite Interface Showcase */}
              <div className="mt-4 grid grid-cols-1 md:grid-cols-12 gap-4 text-[#202B38]">
                {/* 1. Resume ATS Scanner Preview (6 cols) */}
                <div className="md:col-span-6 bg-white rounded-2xl p-5 shadow-md border border-[#E5E9EF] flex flex-col justify-between">
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div className="p-2 rounded-lg bg-[#123E63]/10 text-[#123E63]">
                          <FileSearch className="w-4 h-4" />
                        </div>
                        <div>
                          <h4 className="text-xs font-bold text-[#0D3557]">AI Resume ATS Scanner</h4>
                          <p className="text-[10px] text-[#8993A0]">Keyword Matching & Gap Detection</p>
                        </div>
                      </div>
                      <span className="px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 font-extrabold text-xs border border-emerald-200">
                        88% Match
                      </span>
                    </div>

                    <div className="bg-[#F8F9FA] rounded-xl p-3 space-y-2 border border-[#E5E9EF]">
                      <div className="flex justify-between text-[11px] font-semibold text-[#505D6F]">
                        <span>ATS Formatting & Readability</span>
                        <span className="text-emerald-600 font-bold">92%</span>
                      </div>
                      <div className="w-full h-1.5 bg-gray-200 rounded-full overflow-hidden">
                        <div className="w-[92%] h-full bg-emerald-500 rounded-full" />
                      </div>
                      <div className="flex justify-between text-[11px] font-semibold text-[#505D6F]">
                        <span>Skill & Tech Keyword Alignment</span>
                        <span className="text-[#F5A623] font-bold">84%</span>
                      </div>
                      <div className="w-full h-1.5 bg-gray-200 rounded-full overflow-hidden">
                        <div className="w-[84%] h-full bg-[#F5A623] rounded-full" />
                      </div>
                    </div>

                    <div className="flex flex-wrap gap-1.5 pt-1">
                      <span className="px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-700 text-[10px] font-bold">
                        &bull; Python
                      </span>
                      <span className="px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-700 text-[10px] font-bold">
                        &bull; Fast API
                      </span>
                      <span className="px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-700 text-[10px] font-bold">
                        &bull; SQL
                      </span>
                      <span className="px-2 py-0.5 rounded-md bg-amber-50 text-amber-700 text-[10px] font-bold">
                        &Delta; Microservices (Suggested)
                      </span>
                    </div>
                  </div>
                </div>

                {/* 2. Coding Sandbox Preview (6 cols) */}
                <div className="md:col-span-6 bg-[#0B1726] rounded-2xl p-5 shadow-md border border-[#1E3A5F] flex flex-col justify-between text-white font-mono">
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div className="p-2 rounded-lg bg-[#F5A623]/20 text-[#F5A623]">
                          <Code2 className="w-4 h-4" />
                        </div>
                        <div>
                          <h4 className="text-xs font-bold text-white font-sans">Coding Sandbox</h4>
                          <p className="text-[10px] text-[#8AAEC8] font-sans">Multi-language Test Execution</p>
                        </div>
                      </div>
                      <span className="px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 font-bold text-[11px] border border-emerald-500/30">
                        10/10 Passed
                      </span>
                    </div>

                    <div className="bg-[#050D1A] rounded-xl p-3 text-[11px] space-y-1 text-slate-300 border border-[#1E3A5F]/60">
                      <p className="text-[#8AAEC8]"><span className="text-[#F5A623]">def</span> two_sum(nums, target):</p>
                      <p className="pl-4 text-[#8AAEC8]">seen = dict()</p>
                      <p className="pl-4 text-[#8AAEC8]"><span className="text-[#F5A623]">for</span> i, num <span className="text-[#F5A623]">in</span> enumerate(nums):</p>
                      <p className="pl-8 text-emerald-400">if target - num in seen: return [seen[...], i]</p>
                    </div>

                    <div className="flex items-center justify-between text-[11px] text-[#8AAEC8]">
                      <span className="flex items-center gap-1.5 font-sans">
                        <Play className="w-3 h-3 text-emerald-400 fill-emerald-400" />
                        Execution: 12ms
                      </span>
                      <span className="font-sans text-slate-400">Memory: 14.8 MB</span>
                    </div>
                  </div>
                </div>

                {/* 3. AI Mock Interview Simulation Preview (12 cols) */}
                <div className="md:col-span-12 bg-white rounded-2xl p-5 shadow-md border border-[#E5E9EF] flex flex-col sm:flex-row items-center justify-between gap-5">
                  <div className="flex items-center gap-3.5 w-full sm:w-auto">
                    <div className="w-12 h-12 rounded-2xl bg-[#0D3557] text-[#F5A623] flex items-center justify-center shrink-0 shadow-md">
                      <Mic className="w-6 h-6 animate-pulse" />
                    </div>
                    <div className="space-y-0.5">
                      <div className="inline-flex items-center gap-1.5 text-[10px] font-bold text-[#F5A623] uppercase tracking-wider">
                        <Volume2 className="w-3 h-3" />
                        <span>AI Mock Interview Voice Agent</span>
                      </div>
                      <h4 className="text-sm font-bold text-[#0D3557]">
                        &quot;Explain the trade-offs between SQL and NoSQL in distributed systems.&quot;
                      </h4>
                      <p className="text-xs text-[#8993A0]">
                        Real-time voice capture, tone analysis, STAR format rubric, and instant feedback.
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    <span className="px-3 py-1.5 rounded-xl bg-[#123E63]/10 text-[#123E63] font-bold text-xs border border-[#123E63]/20">
                      Technical Score: 94%
                    </span>
                    <span className="px-3 py-1.5 rounded-xl bg-[#FFF6E8] text-[#F5A623] font-bold text-xs border border-[#F5A623]/30">
                      Speech Clarity: High
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 3. Platform Features Section (5 Core Modules) */}
      <section id="features" className="py-20 lg:py-28 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
          <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-[#123E63]/10 text-[#123E63] text-xs font-bold uppercase tracking-wider">
            <Zap className="w-3.5 h-3.5 text-[#F5A623]" />
            Core Capabilities
          </div>
          <h2 className="text-3xl sm:text-4xl font-black text-[#0D3557] tracking-tight">
            Engineered for Comprehensive Student Preparation
          </h2>
          <p className="text-sm sm:text-base text-[#505D6F]">
            Everything you need to transform from an aspiring student into a confident, job-ready technical candidate.
          </p>
        </div>

        {/* 5 Feature Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Feature 1: AI Resume Analysis */}
          <div className="bg-white rounded-2xl p-7 shadow-card hover:shadow-card-hover border border-[#E5E9EF] transition-all flex flex-col justify-between group">
            <div className="space-y-4">
              <div className="w-14 h-14 rounded-2xl bg-[#123E63]/10 text-[#123E63] flex items-center justify-center group-hover:bg-[#123E63] group-hover:text-white transition">
                <FileSearch className="w-7 h-7" />
              </div>
              <h3 className="text-xl font-bold text-[#0D3557]">
                AI Resume Analysis
              </h3>
              <p className="text-xs sm:text-sm text-[#505D6F] leading-relaxed">
                Upload your resume in PDF or DOCX format to receive immediate diagnostic evaluation against real job descriptions.
              </p>
              <ul className="space-y-2 pt-2 text-xs text-[#505D6F]">
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                  <span>Automated ATS compatibility scoring with weighted rubrics</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                  <span>Identification of missing technical skills and experience gaps</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                  <span>Actionable suggestions to improve wording, metrics, and impact</span>
                </li>
              </ul>
            </div>
            <div className="pt-6 border-t border-[#E5E9EF] mt-6">
              <span className="text-xs font-bold text-[#123E63] flex items-center gap-1.5">
                ATS Engine v1.0 &bull; Ready for Evaluation
              </span>
            </div>
          </div>

          {/* Feature 2: Coding Practice */}
          <div className="bg-white rounded-2xl p-7 shadow-card hover:shadow-card-hover border border-[#E5E9EF] transition-all flex flex-col justify-between group">
            <div className="space-y-4">
              <div className="w-14 h-14 rounded-2xl bg-[#FFF6E8] text-[#F5A623] flex items-center justify-center group-hover:bg-[#F5A623] group-hover:text-white transition">
                <Code2 className="w-7 h-7" />
              </div>
              <h3 className="text-xl font-bold text-[#0D3557]">
                Coding Practice
              </h3>
              <p className="text-xs sm:text-sm text-[#505D6F] leading-relaxed">
                Tackle curated data structures, algorithms, and real technical interview challenges with real-time feedback.
              </p>
              <ul className="space-y-2 pt-2 text-xs text-[#505D6F]">
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-[#F5A623] shrink-0 mt-0.5" />
                  <span>Interactive code editor with syntax highlighting and keyboard shortcuts</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-[#F5A623] shrink-0 mt-0.5" />
                  <span>Instant multi-language code execution and test verification</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-[#F5A623] shrink-0 mt-0.5" />
                  <span>Strengthen algorithmic intuition and solve rate under time constraints</span>
                </li>
              </ul>
            </div>
            <div className="pt-6 border-t border-[#E5E9EF] mt-6">
              <span className="text-xs font-bold text-[#F5A623] flex items-center gap-1.5">
                Python, Java, C++, TypeScript &bull; Sandboxed
              </span>
            </div>
          </div>

          {/* Feature 3: AI-Powered Mock Interviews */}
          <div className="bg-white rounded-2xl p-7 shadow-card hover:shadow-card-hover border border-[#E5E9EF] transition-all flex flex-col justify-between group">
            <div className="space-y-4">
              <div className="w-14 h-14 rounded-2xl bg-[#123E63]/10 text-[#123E63] flex items-center justify-center group-hover:bg-[#123E63] group-hover:text-white transition">
                <Mic className="w-7 h-7" />
              </div>
              <h3 className="text-xl font-bold text-[#0D3557]">
                AI Mock Interviews
              </h3>
              <p className="text-xs sm:text-sm text-[#505D6F] leading-relaxed">
                Participate in realistic, AI-generated technical and behavioral interviews tailored to your target job profile.
              </p>
              <ul className="space-y-2 pt-2 text-xs text-[#505D6F]">
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                  <span>Voice interaction and audio response recording capabilities</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                  <span>Rigorous answer evaluation across technical depth and clarity</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                  <span>Personalized rubric feedback, strengths, and improvement suggestions</span>
                </li>
              </ul>
            </div>
            <div className="pt-6 border-t border-[#E5E9EF] mt-6">
              <span className="text-xs font-bold text-[#123E63] flex items-center gap-1.5">
                Dynamic Question Generator &bull; Audio Rubrics
              </span>
            </div>
          </div>

          {/* Feature 4: Personalized Feedback & Learning Recommendations */}
          <div className="bg-white rounded-2xl p-7 shadow-card hover:shadow-card-hover border border-[#E5E9EF] transition-all flex flex-col justify-between group">
            <div className="space-y-4">
              <div className="w-14 h-14 rounded-2xl bg-[#123E63]/10 text-[#123E63] flex items-center justify-center group-hover:bg-[#123E63] group-hover:text-white transition">
                <Compass className="w-7 h-7" />
              </div>
              <h3 className="text-xl font-bold text-[#0D3557]">
                Personalized Recommendations
              </h3>
              <p className="text-xs sm:text-sm text-[#505D6F] leading-relaxed">
                Stop guessing what to study next. Our diagnostic algorithms synthesize your session outcomes into a tailored roadmap.
              </p>
              <ul className="space-y-2 pt-2 text-xs text-[#505D6F]">
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                  <span>Detect specific weak topic areas across coding and mock interviews</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                  <span>Targeted suggestions prioritized by hiring manager weight</span>
                </li>
                <li className="flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />
                  <span>Focused learning milestones to maximize preparation efficiency</span>
                </li>
              </ul>
            </div>
            <div className="pt-6 border-t border-[#E5E9EF] mt-6">
              <span className="text-xs font-bold text-[#123E63] flex items-center gap-1.5">
                Intelligent Skill Diagnostics
              </span>
            </div>
          </div>

          {/* Feature 5: Progress Tracking (Informational Card - No Dashboard Embedding) */}
          <div className="bg-gradient-to-br from-[#0D3557] to-[#123E63] text-white rounded-2xl p-7 shadow-card hover:shadow-card-hover transition-all flex flex-col justify-between md:col-span-2 lg:col-span-2 group">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="w-14 h-14 rounded-2xl bg-white/10 text-[#F5A623] flex items-center justify-center group-hover:bg-white/20 transition">
                  <BarChart3 className="w-7 h-7" />
                </div>
                <span className="px-3 py-1 rounded-full bg-[#F5A623]/20 border border-[#F5A623]/30 text-[#F5A623] text-xs font-bold">
                  Personal Student Dashboard
                </span>
              </div>
              <h3 className="text-xl font-bold text-white">
                Comprehensive Progress Tracking
              </h3>
              <p className="text-xs sm:text-sm text-[#BCD3E6] leading-relaxed max-w-2xl">
                When you sign in to your authenticated student account, InterviewReady AI compiles all your resume evaluations, coding submissions, and interview scores into your private performance dashboard.
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-2 text-xs">
                <div className="bg-white/5 border border-white/10 rounded-xl p-3">
                  <span className="text-[#F5A623] font-bold block mb-1">Overall Readiness</span>
                  <span className="text-[#8AAEC8] text-[11px]">Weighted metric reflecting overall job qualification</span>
                </div>
                <div className="bg-white/5 border border-white/10 rounded-xl p-3">
                  <span className="text-[#F5A623] font-bold block mb-1">History & Logs</span>
                  <span className="text-[#8AAEC8] text-[11px]">Track chronological improvement across all assessments</span>
                </div>
                <div className="bg-white/5 border border-white/10 rounded-xl p-3">
                  <span className="text-[#F5A623] font-bold block mb-1">Interactive Analytics</span>
                  <span className="text-[#8AAEC8] text-[11px]">Visual charts comparing current mastery against target roles</span>
                </div>
              </div>
            </div>
            <div className="pt-6 border-t border-white/10 mt-6 flex items-center justify-between">
              <span className="text-xs text-[#8AAEC8] font-medium">
                Accessible securely upon authentication &bull; Private to your account
              </span>
              <Link
                href="/login"
                className="text-xs font-bold text-[#F5A623] hover:text-[#E09212] flex items-center gap-1"
              >
                <span>Access Dashboard</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* 4. How It Works Section (4-Step Workflow) */}
      <section id="how-it-works" className="py-20 lg:py-28 bg-[#F1F5F9] border-y border-[#E5E9EF]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16 space-y-3">
            <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-[#123E63]/10 text-[#123E63] text-xs font-bold uppercase tracking-wider">
              <Layers className="w-3.5 h-3.5 text-[#F5A623]" />
              Structured Pathway
            </div>
            <h2 className="text-3xl sm:text-4xl font-black text-[#0D3557] tracking-tight">
              How InterviewReady AI Works
            </h2>
            <p className="text-sm sm:text-base text-[#505D6F]">
              A proven 4-step workflow designed to take college students from initial skills assessment to complete interview confidence.
            </p>
          </div>

          {/* 4 Steps: Horizontal on md/lg, Vertical on mobile */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 relative">
            {/* Step 1 */}
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-[#E5E9EF] relative flex flex-col justify-between">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="w-12 h-12 rounded-xl bg-[#0D3557] text-white flex items-center justify-center font-extrabold text-lg shadow-sm">
                    1
                  </div>
                  <span className="text-[11px] font-bold text-[#8993A0] uppercase tracking-wider">
                    Step 01
                  </span>
                </div>
                <h3 className="text-lg font-bold text-[#0D3557]">
                  Create Your Account
                </h3>
                <p className="text-xs text-[#505D6F] leading-relaxed">
                  Sign up with your college email to access your personalized preparation workspace and initialize your target career profile.
                </p>
              </div>
              <div className="pt-4 border-t border-[#E5E9EF] mt-6">
                <span className="text-[11px] font-semibold text-[#123E63]">Fast &bull; 60 seconds setup</span>
              </div>
            </div>

            {/* Step 2 */}
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-[#E5E9EF] relative flex flex-col justify-between">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="w-12 h-12 rounded-xl bg-[#123E63] text-white flex items-center justify-center font-extrabold text-lg shadow-sm">
                    2
                  </div>
                  <span className="text-[11px] font-bold text-[#8993A0] uppercase tracking-wider">
                    Step 02
                  </span>
                </div>
                <h3 className="text-lg font-bold text-[#0D3557]">
                  Assess Your Skills
                </h3>
                <p className="text-xs text-[#505D6F] leading-relaxed">
                  Upload and analyze your resume against target company job descriptions to uncover ATS compatibility scores and missing skills.
                </p>
              </div>
              <div className="pt-4 border-t border-[#E5E9EF] mt-6">
                <span className="text-[11px] font-semibold text-[#123E63]">Identify Gaps Early</span>
              </div>
            </div>

            {/* Step 3 */}
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-[#E5E9EF] relative flex flex-col justify-between">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="w-12 h-12 rounded-xl bg-[#F5A623] text-white flex items-center justify-center font-extrabold text-lg shadow-sm">
                    3
                  </div>
                  <span className="text-[11px] font-bold text-[#8993A0] uppercase tracking-wider">
                    Step 03
                  </span>
                </div>
                <h3 className="text-lg font-bold text-[#0D3557]">
                  Practice and Improve
                </h3>
                <p className="text-xs text-[#505D6F] leading-relaxed">
                  Solve coding questions in an interactive sandbox and attend speech-enabled AI mock interview sessions with realistic prompts.
                </p>
              </div>
              <div className="pt-4 border-t border-[#E5E9EF] mt-6">
                <span className="text-[11px] font-semibold text-[#F5A623]">Hands-On Mastery</span>
              </div>
            </div>

            {/* Step 4 */}
            <div className="bg-white rounded-2xl p-6 shadow-sm border border-[#E5E9EF] relative flex flex-col justify-between">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="w-12 h-12 rounded-xl bg-emerald-600 text-white flex items-center justify-center font-extrabold text-lg shadow-sm">
                    4
                  </div>
                  <span className="text-[11px] font-bold text-[#8993A0] uppercase tracking-wider">
                    Step 04
                  </span>
                </div>
                <h3 className="text-lg font-bold text-[#0D3557]">
                  Track Your Growth
                </h3>
                <p className="text-xs text-[#505D6F] leading-relaxed">
                  Review personalized feedback and monitor your interview readiness and assessment records in your private performance dashboard.
                </p>
              </div>
              <div className="pt-4 border-t border-[#E5E9EF] mt-6">
                <span className="text-[11px] font-semibold text-emerald-600">Continuous Readiness</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 5. Benefits Section */}
      <section id="benefits" className="py-20 lg:py-28 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
          <div className="lg:col-span-5 space-y-6">
            <div className="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-[#123E63]/10 text-[#123E63] text-xs font-bold uppercase tracking-wider">
              <Award className="w-3.5 h-3.5 text-[#F5A623]" />
              Proven Value
            </div>
            <h2 className="text-3xl sm:text-4xl font-black text-[#0D3557] tracking-tight leading-tight">
              Why Students Choose InterviewReady AI
            </h2>
            <p className="text-sm sm:text-base text-[#505D6F] leading-relaxed">
              Traditional interview prep is fragmented across spreadsheets, random coding problem sets, and generic advice. InterviewReady AI unifies the entire preparation loop into an intelligent, student-centric platform.
            </p>
            <div className="pt-2">
              <Link
                href="/register"
                className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-[#0D3557] hover:bg-[#123E63] text-white text-xs sm:text-sm font-bold shadow-md transition"
              >
                <span>Join InterviewReady AI</span>
                <ArrowRight className="w-4 h-4 text-[#F5A623]" />
              </Link>
            </div>
          </div>

          <div className="lg:col-span-7 grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="bg-white p-5 rounded-2xl border border-[#E5E9EF] shadow-xs space-y-2.5">
              <div className="w-10 h-10 rounded-xl bg-[#123E63]/10 text-[#123E63] flex items-center justify-center">
                <Target className="w-5 h-5 text-[#123E63]" />
              </div>
              <h3 className="text-base font-bold text-[#0D3557]">Personalized Interview Prep</h3>
              <p className="text-xs text-[#505D6F] leading-relaxed">
                Evaluations calibrated to your chosen job role, experience level, and preferred technology stack.
              </p>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-[#E5E9EF] shadow-xs space-y-2.5">
              <div className="w-10 h-10 rounded-xl bg-[#FFF6E8] text-[#F5A623] flex items-center justify-center">
                <FileSearch className="w-5 h-5 text-[#F5A623]" />
              </div>
              <h3 className="text-base font-bold text-[#0D3557]">Early Skill Gap Detection</h3>
              <p className="text-xs text-[#505D6F] leading-relaxed">
                Discover what hiring managers and screening algorithms look for before you submit actual applications.
              </p>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-[#E5E9EF] shadow-xs space-y-2.5">
              <div className="w-10 h-10 rounded-xl bg-[#123E63]/10 text-[#123E63] flex items-center justify-center">
                <Code2 className="w-5 h-5 text-[#123E63]" />
              </div>
              <h3 className="text-base font-bold text-[#0D3557]">Practical Hands-On Experience</h3>
              <p className="text-xs text-[#505D6F] leading-relaxed">
                Execute algorithmic solutions in an interactive editor and practice articulate verbal communication.
              </p>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-[#E5E9EF] shadow-xs space-y-2.5">
              <div className="w-10 h-10 rounded-xl bg-[#FFF6E8] text-[#F5A623] flex items-center justify-center">
                <Compass className="w-5 h-5 text-[#F5A623]" />
              </div>
              <h3 className="text-base font-bold text-[#0D3557]">Actionable Recommendations</h3>
              <p className="text-xs text-[#505D6F] leading-relaxed">
                Get crystal-clear action items rather than vague scores to optimize your study hours.
              </p>
            </div>

            <div className="bg-white p-5 rounded-2xl border border-[#E5E9EF] shadow-xs space-y-2.5 sm:col-span-2">
              <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center">
                <BarChart3 className="w-5 h-5 text-emerald-600" />
              </div>
              <h3 className="text-base font-bold text-[#0D3557]">Continuous Improvement & Growth Tracking</h3>
              <p className="text-xs text-[#505D6F] leading-relaxed">
                Maintain a verifiable track record of solved problems, mock interview transcripts, and ATS score milestones as your competence matures.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* 6. Call to Action Banner */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        <div className="bg-gradient-to-r from-[#0D3557] via-[#123E63] to-[#0D3557] rounded-3xl p-8 sm:p-12 text-center text-white relative overflow-hidden shadow-xl">
          <div className="max-w-2xl mx-auto space-y-5 relative">
            <h2 className="text-2xl sm:text-3xl lg:text-4xl font-extrabold tracking-tight">
              Ready to Ace Your Next Technical Interview?
            </h2>
            <p className="text-xs sm:text-sm text-[#BCD3E6] leading-relaxed">
              Join students preparing with AI-powered resume analytics, algorithmic code sandboxes, and speech-enabled mock interviews.
            </p>
            <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-3">
              <Link
                href="/register"
                className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-[#F5A623] hover:bg-[#E09212] text-white font-extrabold text-sm shadow-md transition flex items-center justify-center gap-2"
              >
                <span>Create Student Account</span>
                <ArrowRight className="w-4 h-4" />
              </Link>
              <Link
                href="/login"
                className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-white/10 hover:bg-white/20 text-white font-bold text-sm transition flex items-center justify-center"
              >
                <span>Existing User? Sign In</span>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* 7. Footer */}
      <footer className="mt-auto bg-[#0A2640] text-white border-t border-[#1A4B75]/40 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 pb-8 border-b border-[#1A4B75]/40">
            {/* Branding */}
            <div className="space-y-2 max-w-md">
              <div className="flex items-center gap-2.5">
                <div className="w-9 h-9 rounded-xl bg-[#123E63] flex items-center justify-center text-white shadow-sm">
                  <Brain className="w-5 h-5 text-[#F5A623]" />
                </div>
                <span className="text-lg font-black text-white tracking-tight">
                  InterviewReady <span className="text-[#F5A623]">AI</span>
                </span>
              </div>
              <p className="text-xs text-[#8AAEC8] leading-relaxed">
                AI-Powered Student Interview Preparation Platform. Helping college students diagnose resume gaps, master coding challenges, and succeed in technical interviews.
              </p>
            </div>

            {/* Navigation Links */}
            <div className="flex flex-wrap items-center gap-6 text-xs font-semibold text-[#BCD3E6]">
              <Link href="/" className="hover:text-white transition">
                Home
              </Link>
              <Link href="/login" className="hover:text-white transition">
                Login
              </Link>
              <Link href="/register" className="hover:text-white transition">
                Register
              </Link>
              <Link href="/forgot-password" className="hover:text-white transition">
                Forgot Password
              </Link>
              <Link href="/dashboard" className="hover:text-white transition">
                Performance Dashboard
              </Link>
            </div>
          </div>

          {/* Copyright & Disclaimer */}
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px] text-[#8AAEC8]/80">
            <p>
              &copy; {new Date().getFullYear()} InterviewReady AI. All rights reserved. Major Project.
            </p>
            <p className="text-right">
              Built for Student Career Readiness &bull; Secure Authentication &bull; AI Evaluation
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
