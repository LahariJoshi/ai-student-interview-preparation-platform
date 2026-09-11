"use client";

import React, { createContext, useContext, useState, useEffect } from "react";
import { apiFetch } from "@/lib/api";

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  created_at: string;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, full_name: string) => Promise<void>;
  logout: () => Promise<void>;
  checkAuth: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const checkAuth = async () => {
    try {
      const data = await apiFetch<User>("/auth/me");
      setUser(data);
    } catch {
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    checkAuth();
  }, []);

  const login = async (email: string, password: string) => {
    const data = await apiFetch<User>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
    setUser(data);
  };

  const register = async (email: string, password: string, full_name: string) => {
    const data = await apiFetch<User>("/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password, full_name }),
    });
    setUser(data);
  };

  const logout = async () => {
    try {
      await apiFetch("/auth/logout", { method: "POST" });
    } finally {
      setUser(null);
    }
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, register, logout, checkAuth }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
