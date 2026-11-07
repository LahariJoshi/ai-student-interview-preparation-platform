"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { UserPlus, Mail, Lock, User, AlertCircle, ArrowRight } from "lucide-react";

export default function RegisterPage() {
  const router = useRouter();
  const { register } = useAuth();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsSubmitting(true);

    try {
      await register(email, password, fullName);
      router.push("/profile");
    } catch (err: any) {
      setError(err.message || "Registration failed. Email may already be registered.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="w-full">
      <div className="bg-white rounded-2xl p-8 shadow-card border border-[#E5E9EF] space-y-6">
        <div className="text-center space-y-2">
          <div className="w-16 h-16 rounded-full bg-[#123E63] border-4 border-[#1E5685] flex items-center justify-center mx-auto shadow-md mb-2">
            <div className="w-10 h-10 rounded-full bg-white flex items-center justify-center text-[#123E63]">
              <UserPlus className="w-6 h-6 stroke-[2.2]" />
            </div>
          </div>
          <h2 className="text-2xl font-extrabold text-[#202B38] tracking-tight">Student Registration</h2>
          <p className="text-[#8993A0] text-xs">
            Create an account to master technical and HR interview rounds
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
              Full Name
            </label>
            <div className="relative">
              <User className="w-4 h-4 text-[#8993A0] absolute left-3.5 top-3" />
              <input
                type="text"
                required
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="Lahari Joshi"
                className="w-full bg-[#F8F9FA] border border-[#E5E9EF] focus:border-[#123E63] text-[#202B38] rounded-xl pl-10 pr-4 py-2.5 text-xs font-medium focus:outline-none transition"
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="block text-[11px] font-bold text-[#8993A0] uppercase tracking-wider">
              College / Student Email
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
            <label className="block text-[11px] font-bold text-[#8993A0] uppercase tracking-wider">
              Password
            </label>
            <div className="relative">
              <Lock className="w-4 h-4 text-[#8993A0] absolute left-3.5 top-3" />
              <input
                type="password"
                required
                minLength={6}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Minimum 6 characters"
                className="w-full bg-[#F8F9FA] border border-[#E5E9EF] focus:border-[#123E63] text-[#202B38] rounded-xl pl-10 pr-4 py-2.5 text-xs font-medium focus:outline-none transition"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={isSubmitting}
            className="w-full bg-[#F5A623] hover:bg-[#E09212] disabled:opacity-50 text-white font-bold py-3 rounded-xl transition text-xs shadow-md flex items-center justify-center gap-2 mt-2"
          >
            <span>{isSubmitting ? "Creating Account..." : "Register & Start Preparing"}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </form>

        <div className="pt-2 text-center text-xs text-[#8993A0] border-t border-[#E5E9EF]">
          Already have an account?{" "}
          <Link href="/login" className="text-[#123E63] hover:text-[#0D3557] font-bold">
            Sign in here
          </Link>
        </div>
      </div>
    </div>
  );
}
