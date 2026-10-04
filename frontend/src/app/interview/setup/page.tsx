"use client";

import React, { useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import InterviewSetup from "@/components/interview/InterviewSetup";
import { ArrowLeft, Loader2 } from "lucide-react";

export default function InterviewSetupPage() {
  const { user, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !user) {
      router.push("/login");
    }
  }, [user, isLoading, router]);

  if (isLoading || !user) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <Loader2 className="w-8 h-8 animate-spin text-sky-400" />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto py-4">
      {/* Back button */}
      <div className="mb-4">
        <Link
          href="/interview"
          className="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-400 hover:text-slate-200 transition"
        >
          <ArrowLeft className="w-3.5 h-3.5" />
          Back to Interviews
        </Link>
      </div>

      <InterviewSetup />
    </div>
  );
}
