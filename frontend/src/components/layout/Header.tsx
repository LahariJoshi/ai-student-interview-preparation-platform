"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useAuth } from "@/context/AuthContext";
import { Menu, Bell, User, CheckCircle2 } from "lucide-react";

interface HeaderProps {
  onMenuToggle: () => void;
  title?: string;
  subtitle?: string;
}

export default function Header({ onMenuToggle, title, subtitle }: HeaderProps) {
  const { user } = useAuth();
  const [greeting, setGreeting] = useState("Good morning");

  useEffect(() => {
    const hour = new Date().getHours();
    if (hour < 12) setGreeting("Good morning");
    else if (hour < 17) setGreeting("Good afternoon");
    else setGreeting("Good evening");
  }, []);

  const firstName = user?.full_name ? user.full_name.split(" ")[0] : "Student";
  const displayTitle = title || `${greeting}, ${firstName}!`;
  const displaySubtitle = subtitle || "Let's work towards your interview goals today.";

  return (
    <header className="w-full flex items-center justify-between py-4 px-4 sm:px-6 md:px-8 border-b border-[#E5E9EF] bg-transparent">
      {/* Title & Greeting */}
      <div className="flex items-center gap-3">
        <button
          onClick={onMenuToggle}
          className="lg:hidden p-2 rounded-xl text-[#123E63] hover:bg-white border border-[#E5E9EF] shadow-sm transition"
          aria-label="Open Sidebar"
        >
          <Menu className="w-5 h-5" />
        </button>

        <div>
          <h1 className="text-xl sm:text-2xl font-bold text-[#202B38] tracking-tight">
            {displayTitle}
          </h1>
          <p className="text-xs sm:text-sm text-[#8993A0] mt-0.5 font-normal">
            {displaySubtitle}
          </p>
        </div>
      </div>

      {/* Right Actions: Notifications & Avatar */}
      <div className="flex items-center gap-3">
        {/* Notification Bell */}
        <button
          className="relative p-2.5 rounded-full bg-white text-[#123E63] hover:text-[#F5A623] hover:shadow-md border border-[#E5E9EF] transition shadow-sm"
          aria-label="Notifications"
        >
          <Bell className="w-4 h-4" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-[#F5A623] ring-2 ring-white animate-pulse" />
        </button>

        {/* User Profile Chip */}
        {user ? (
          <Link
            href="/profile"
            className="flex items-center gap-2.5 p-1.5 pr-3 rounded-full bg-white hover:bg-slate-50 border border-[#E5E9EF] shadow-sm transition"
          >
            <div className="w-8 h-8 rounded-full bg-[#123E63] flex items-center justify-center text-white text-xs font-bold uppercase">
              {firstName.charAt(0)}
            </div>
            <span className="text-xs font-semibold text-[#202B38] hidden sm:inline-block max-w-[120px] truncate">
              {user.full_name}
            </span>
          </Link>
        ) : (
          <Link
            href="/login"
            className="text-xs font-semibold px-4 py-2 rounded-full bg-[#123E63] text-white hover:bg-[#0D3557] transition shadow-sm"
          >
            Sign In
          </Link>
        )}
      </div>
    </header>
  );
}
