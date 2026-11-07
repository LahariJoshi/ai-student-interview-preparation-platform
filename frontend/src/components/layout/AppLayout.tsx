"use client";

import React, { useState } from "react";
import { usePathname } from "next/navigation";
import Sidebar from "./Sidebar";
import Header from "./Header";

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Authentication and recovery pages use focused clean layout
  const isAuthPage =
    pathname === "/login" ||
    pathname === "/register" ||
    pathname === "/forgot-password" ||
    pathname === "/reset-password";

  if (isAuthPage) {
    return (
      <div className="min-h-screen bg-[#F1F3F6] flex flex-col justify-center items-center p-4 sm:p-6">
        <div className="w-full max-w-md">
          {children}
        </div>
      </div>
    );
  }

  // Public Landing Page (Home Page) renders full-width modern marketing experience
  if (pathname === "/") {
    return (
      <div className="min-h-screen bg-[#F8FAFC] text-[#202B38] font-sans antialiased flex flex-col">
        {children}
      </div>
    );
  }

  // Authenticated workspace and platform modules (Dashboard, ATS, Coding, Interview, etc.)
  return (
    <div className="min-h-screen bg-[#E5EBF2] p-2 sm:p-4 md:p-6 lg:p-8 flex items-center justify-center font-sans antialiased text-[#202B38]">
      {/* Centered spacious rounded outer container with subtle shadows */}
      <div className="w-full max-w-[1600px] min-h-[92vh] bg-[#F1F3F6] rounded-[24px] sm:rounded-[28px] lg:rounded-[32px] shadow-shell overflow-hidden flex flex-col lg:flex-row border border-[#E5E9EF] relative">
        {/* Navy Left Sidebar */}
        <Sidebar
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
        />

        {/* Main Light Dashboard Area */}
        <div className="flex-1 flex flex-col min-w-0 bg-[#F1F3F6] overflow-x-hidden">
          <Header onMenuToggle={() => setSidebarOpen(true)} />

          <main className="flex-1 p-4 sm:p-6 md:p-8">
            {children}
          </main>
        </div>
      </div>
    </div>
  );
}
