"use client";

import React, { useState } from "react";
import Sidebar from "./Sidebar";
import Header from "./Header";

interface DashboardShellProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
}

export default function DashboardShell({
  children,
  title,
  subtitle,
}: DashboardShellProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-[#EAEFF5] p-2 sm:p-4 md:p-6 lg:p-8 flex items-center justify-center font-sans antialiased text-[#202B38]">
      {/* Centered spacious rounded outer container matching the reference image */}
      <div className="w-full max-w-[1600px] min-h-[92vh] bg-[#F1F3F6] rounded-[24px] sm:rounded-[28px] lg:rounded-[32px] shadow-shell overflow-hidden flex flex-col lg:flex-row border border-[#E5E9EF]/80 relative">
        {/* Left Vertical Navy Sidebar */}
        <Sidebar
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
        />

        {/* Main Content Area */}
        <div className="flex-1 flex flex-col min-w-0 bg-[#F1F3F6] overflow-x-hidden">
          {/* Header */}
          <Header
            onMenuToggle={() => setSidebarOpen(true)}
            title={title}
            subtitle={subtitle}
          />

          {/* Dynamic Page Content */}
          <main className="flex-1 p-4 sm:p-6 md:p-8">
            {children}
          </main>
        </div>
      </div>
    </div>
  );
}
