"use client";

import "./globals.css";
import React from "react";
import Link from "next/link";
import { AuthProvider, useAuth } from "@/context/AuthContext";
import { User, LogOut, UserCheck, Sparkles } from "lucide-react";

function Navigation() {
  const { user, logout } = useAuth();

  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2 text-xl font-bold text-sky-400">
          <Sparkles className="w-6 h-6 text-sky-400" />
          <span>PrepAI</span>
        </Link>
        <nav className="flex items-center gap-4">
          {user ? (
            <>
              <div className="flex items-center gap-2 text-slate-300 text-sm bg-slate-800 px-3 py-1.5 rounded-lg border border-slate-700">
                <UserCheck className="w-4 h-4 text-emerald-400" />
                <span className="font-medium text-white">{user.full_name}</span>
              </div>
              <Link
                href="/profile"
                className="flex items-center gap-1 text-sm bg-sky-600 hover:bg-sky-500 text-white px-3 py-1.5 rounded-lg font-medium transition"
              >
                <User className="w-4 h-4" />
                Profile
              </Link>
              <button
                onClick={logout}
                className="flex items-center gap-1 text-sm bg-slate-800 hover:bg-slate-700 text-slate-300 px-3 py-1.5 rounded-lg border border-slate-700 font-medium transition"
              >
                <LogOut className="w-4 h-4 text-red-400" />
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                href="/login"
                className="text-sm text-slate-300 hover:text-white px-3 py-1.5 rounded-lg font-medium transition"
              >
                Login
              </Link>
              <Link
                href="/register"
                className="text-sm bg-sky-600 hover:bg-sky-500 text-white px-4 py-2 rounded-lg font-medium transition"
              >
                Get Started
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <title>AI-Powered Student Interview Preparation Platform</title>
        <meta name="description" content="AI platform to prepare college students for placement and technical interviews." />
      </head>
      <body className="bg-slate-950 text-slate-100 min-h-screen flex flex-col">
        <AuthProvider>
          <Navigation />
          <main className="flex-1 max-w-6xl w-full mx-auto p-4 md:p-6">{children}</main>
          <footer className="border-t border-slate-800 py-6 text-center text-xs text-slate-500">
            &copy; 2026 AI-Powered Student Interview Preparation Platform — College Major Project
          </footer>
        </AuthProvider>
      </body>
    </html>
  );
}
