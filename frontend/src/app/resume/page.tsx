"use client";

import React, { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import ResumeUploadDropzone from "@/components/resume/ResumeUploadDropzone";
import { FileCheck } from "lucide-react";

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
      <div className="py-20 text-center text-slate-400">
        <div className="animate-spin w-8 h-8 border-2 border-sky-400 border-t-transparent rounded-full mx-auto mb-4" />
        Authenticating session...
      </div>
    );
  }

  return (
    <div className="py-8 space-y-8">
      <div className="text-center space-y-2 max-w-xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-950/80 border border-sky-800 text-sky-300 text-xs font-semibold">
          <FileCheck className="w-4 h-4 text-sky-400" />
          Resume Management
        </div>
        <h1 className="text-3xl font-extrabold text-white">Student Resume Upload</h1>
        <p className="text-slate-400 text-sm">
          Upload your resume in PDF or DOCX format to store securely for upcoming ATS analysis and interview preparation.
        </p>
      </div>

      <ResumeUploadDropzone />
    </div>
  );
}
