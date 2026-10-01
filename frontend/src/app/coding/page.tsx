"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import QuestionList from "@/components/coding/QuestionList";
import CodingProgress from "@/components/coding/CodingProgress";
import { Code2, BarChart2, Sparkles, BookOpen } from "lucide-react";

export default function CodingPage() {
  const { user, isLoading } = useAuth();
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<"problems" | "progress">("problems");

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center space-y-3">
          <div className="w-8 h-8 border-2 border-sky-400 border-t-transparent rounded-full animate-spin mx-auto" />
          <p className="text-sm text-slate-400">Loading coding environment...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    router.push("/login");
    return null;
  }

  return (
    <div className="space-y-8 py-2">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-sky-950/80 border border-sky-800 text-sky-300 text-xs font-semibold mb-2">
            <Code2 className="w-3.5 h-3.5 text-sky-400" />
            Member-2 Coding Assessment Sandbox
          </div>
          <h1 className="text-3xl font-extrabold text-white tracking-tight">
            Technical Coding Practice
          </h1>
          <p className="text-slate-400 text-sm mt-1 max-w-2xl">
            Sharpen algorithmic problem-solving skills with multi-language execution, verified test cases, and real-time proficiency analytics.
          </p>
        </div>

        {/* Tab Toggle */}
        <div className="flex items-center p-1 bg-slate-900 border border-slate-800 rounded-xl">
          <button
            onClick={() => setActiveTab("problems")}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold transition ${
              activeTab === "problems"
                ? "bg-sky-600 text-white shadow-sm"
                : "text-slate-400 hover:text-white"
            }`}
          >
            <BookOpen className="w-4 h-4" />
            <span>Problem Bank</span>
          </button>
          <button
            onClick={() => setActiveTab("progress")}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-semibold transition ${
              activeTab === "progress"
                ? "bg-sky-600 text-white shadow-sm"
                : "text-slate-400 hover:text-white"
            }`}
          >
            <BarChart2 className="w-4 h-4" />
            <span>My Progress & Analytics</span>
          </button>
        </div>
      </div>

      {/* Main Tab Content */}
      {activeTab === "problems" ? (
        <QuestionList />
      ) : (
        <CodingProgress />
      )}
    </div>
  );
}
