"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import QuestionList from "@/components/coding/QuestionList";
import CodingProgress from "@/components/coding/CodingProgress";
import { Code2, BarChart2, BookOpen, Sparkles } from "lucide-react";

export default function CodingPage() {
  const { user, isLoading } = useAuth();
  const router = useRouter();
  const [activeTab, setActiveTab] = useState<"problems" | "progress">("problems");

  if (isLoading) {
    return (
      <div className="py-20 text-center text-[#8993A0]">
        <div className="animate-spin w-8 h-8 border-2 border-[#123E63] border-t-transparent rounded-full mx-auto mb-4" />
        <p className="text-xs font-semibold">Loading coding sandbox...</p>
      </div>
    );
  }

  if (!user) {
    router.push("/login");
    return null;
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="bg-white rounded-2xl p-6 sm:p-7 shadow-card border border-[#E5E9EF] flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#123E63]/10 border border-[#123E63]/20 text-[#123E63] text-xs font-semibold mb-2">
            <Code2 className="w-3.5 h-3.5 text-[#F5A623]" />
            Algorithmic Problem Sandbox
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-[#202B38] tracking-tight">
            Technical Coding Practice
          </h2>
          <p className="text-xs sm:text-sm text-[#8993A0] mt-1">
            Solve algorithmic problems in Python, Java, or C++ with automated test cases, execution memory profiling, and topic proficiency metrics.
          </p>
        </div>

        {/* Tab Switcher */}
        <div className="flex items-center p-1 bg-[#F1F3F6] border border-[#E5E9EF] rounded-xl self-start md:self-auto shrink-0">
          <button
            onClick={() => setActiveTab("problems")}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-bold transition ${
              activeTab === "problems"
                ? "bg-[#123E63] text-white shadow-xs"
                : "text-[#8993A0] hover:text-[#202B38]"
            }`}
          >
            <BookOpen className="w-3.5 h-3.5" />
            <span>Problem Bank</span>
          </button>
          <button
            onClick={() => setActiveTab("progress")}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg text-xs font-bold transition ${
              activeTab === "progress"
                ? "bg-[#123E63] text-white shadow-xs"
                : "text-[#8993A0] hover:text-[#202B38]"
            }`}
          >
            <BarChart2 className="w-3.5 h-3.5" />
            <span>My Progress & Analytics</span>
          </button>
        </div>
      </div>

      {/* Main Tab Content */}
      {activeTab === "problems" ? <QuestionList /> : <CodingProgress />}
    </div>
  );
}
