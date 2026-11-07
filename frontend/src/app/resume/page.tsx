"use client";

import React, { useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import ResumeUploadDropzone from "@/components/resume/ResumeUploadDropzone";
import { FileText, Target, ArrowRight } from "lucide-react";

export default function ResumePage() {
  const router = useRouter();
  const { user, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading && !user) {
      router.push("/login");
    }
  }, [user, isLoading, router]);

  if (isLoading) {
    return (
      <div className="py-20 text-center text-[#8993A0]">
        <div className="animate-spin w-8 h-8 border-2 border-[#123E63] border-t-transparent rounded-full mx-auto mb-4" />
        <p className="text-xs font-semibold">Authenticating student session...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-4xl">
      {/* Top Header Card */}
      <div className="bg-white rounded-2xl p-6 sm:p-7 shadow-card border border-[#E5E9EF] flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#123E63]/10 border border-[#123E63]/20 text-[#123E63] text-xs font-semibold mb-2">
            <FileText className="w-3.5 h-3.5 text-[#F5A623]" />
            Resume Optimization Engine
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-[#202B38] tracking-tight">
            Student Resume Analysis
          </h2>
          <p className="text-xs sm:text-sm text-[#8993A0] mt-1">
            Upload your resume in PDF or DOCX format to analyze structure, action verbs, impact metrics, and ATS compatibility.
          </p>
        </div>

        <Link
          href="/ats"
          className="px-4 py-2.5 rounded-xl bg-[#123E63] hover:bg-[#0D3557] text-white text-xs font-bold shadow-sm transition flex items-center gap-1.5 shrink-0 self-start sm:self-auto"
        >
          <Target className="w-4 h-4 text-[#F5A623]" />
          <span>ATS Job Matcher</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>

      {/* Main Upload Dropzone and Stored Resumes */}
      <ResumeUploadDropzone />
    </div>
  );
}
