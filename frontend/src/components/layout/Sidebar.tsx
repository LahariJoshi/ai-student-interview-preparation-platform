"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import {
  Home,
  FileText,
  Code2,
  Mic,
  Compass,
  BarChart2,
  User,
  Settings,
  LogOut,
  X,
  Target,
} from "lucide-react";

interface SidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
}

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  const navItems = [
    { label: "Home", href: "/", icon: Home },
    { label: "Resume Analysis", href: "/resume", icon: FileText },
    { label: "Coding Practice", href: "/coding", icon: Code2 },
    { label: "AI Mock Interview", href: "/interview", icon: Mic },
    { label: "Learning Recommendations", href: "/recommendations", icon: Compass },
    { label: "Performance Dashboard", href: "/dashboard", icon: BarChart2 },
    { label: "Profile", href: "/profile", icon: User },
    { label: "Settings", href: "/settings", icon: Settings },
  ];

  const displayName = user?.full_name ? user.full_name.toUpperCase() : "STUDENT USER";
  const displayEmail = user?.email || "student@college.edu";

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden backdrop-blur-sm transition-opacity"
          onClick={onClose}
        />
      )}

      {/* Vertical Navigation Sidebar */}
      <aside
        className={`fixed lg:sticky top-0 left-0 z-50 h-screen w-72 bg-[#0D3557] text-white flex flex-col justify-between py-6 px-4 transition-transform duration-300 ease-in-out shrink-0 select-none ${
          isOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"
        }`}
      >
        <div className="flex flex-col space-y-6">
          {/* Top Brand & Profile Avatar (Matching Reference Image) */}
          <div className="flex flex-col items-center text-center relative pt-2 pb-4 border-b border-[#1A4B75]/50">
            {/* Close button for mobile */}
            {onClose && (
              <button
                onClick={onClose}
                className="lg:hidden absolute right-1 top-1 p-1 text-slate-300 hover:text-white"
                aria-label="Close Sidebar"
              >
                <X className="w-5 h-5" />
              </button>
            )}

            {/* Circular Profile Avatar with White User Icon (From Reference Image) */}
            <div className="w-20 h-20 rounded-full bg-[#123E63] border-4 border-[#1E5685] flex items-center justify-center shadow-lg mb-3">
              <div className="w-14 h-14 rounded-full bg-white flex items-center justify-center text-[#0D3557]">
                <User className="w-8 h-8 stroke-[2.2]" />
              </div>
            </div>

            {/* User Name in Bold Uppercase & Email (Matching Reference Image) */}
            <h2 className="text-lg font-bold tracking-wider text-white font-mono">
              {displayName}
            </h2>
            <p className="text-xs text-[#8AAEC8] mt-0.5 truncate max-w-[220px]">
              {displayEmail}
            </p>

            {/* Application Subtitle Badge */}
            <div className="mt-2.5 px-3 py-1 rounded-full bg-[#123E63]/80 border border-[#1A4B75] text-[11px] text-[#BCD3E6]">
              <span className="text-[#F5A623] font-semibold">InterviewReady</span> AI
            </div>
          </div>

          {/* Navigation Links (Matching Reference Items) */}
          <nav className="space-y-1.5 overflow-y-auto max-h-[calc(100vh-320px)] pr-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive =
                item.href === "/"
                  ? pathname === "/"
                  : pathname === item.href || pathname.startsWith(item.href + "/");

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={() => onClose && onClose()}
                  className={`flex items-center gap-3.5 px-4 py-2.5 rounded-xl text-sm font-medium transition-all ${
                    isActive
                      ? "bg-[#123E63] text-white shadow-md border-l-4 border-[#F5A623] font-semibold"
                      : "text-[#BCD3E6] hover:bg-[#123E63]/50 hover:text-white"
                  }`}
                >
                  <Icon
                    className={`w-4 h-4 shrink-0 ${
                      isActive ? "text-[#F5A623]" : "text-[#8AAEC8]"
                    }`}
                  />
                  <span className="capitalize">{item.label}</span>
                </Link>
              );
            })}
          </nav>
        </div>

        {/* Footer Logout & Status */}
        <div className="pt-4 border-t border-[#1A4B75]/50 flex flex-col gap-2">
          {user ? (
            <button
              onClick={() => logout()}
              className="flex items-center gap-3 px-4 py-2 rounded-xl text-sm text-[#8AAEC8] hover:text-red-300 hover:bg-red-950/20 transition w-full"
            >
              <LogOut className="w-4 h-4 text-red-400 shrink-0" />
              <span>Sign Out</span>
            </button>
          ) : (
            <Link
              href="/login"
              className="flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl text-sm bg-[#F5A623] text-white font-semibold hover:bg-[#E09212] transition shadow-md"
            >
              Sign In
            </Link>
          )}

          <div className="text-[10px] text-center text-[#8AAEC8]/60 mt-1">
            v1.0 &bull; Major Project &copy; 2026
          </div>
        </div>
      </aside>
    </>
  );
}
