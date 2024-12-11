"use client";
import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import {auth} from "@/firebase/firebaseConfig";
import { onAuthStateChanged, User, getAuth, getIdToken } from "firebase/auth";
import {setCookie, destroyCookie, parseCookies } from "nookies";
import { useRouter } from "next/navigation";
import { get } from "http";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: {children: ReactNode}) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    setLoading(false);
  }, []);

  // Login function
  const login = async (username: string, password: string) => {
    setLoading(true);
    try {
      const response = await fetch("/api/auth/login", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
          },
          body: JSON.stringify({ username, password }),
      });

      if (!response.ok) {
          throw new Error("Login failed");
      }
      const data = await response.json();
      setCookie(null, "token", data.user.stsTokenManager.accessToken, {
        maxAge: data.user.stsTokenManager.expirationTime, // 7 days
        path: "/",                // Accessible on all routes
        secure: true,             // Only send over HTTPS
        httpOnly: false,          // Set to true if setting from an API route
        sameSite: "lax",          // Protects against CSRF attacks
    });

    setUser(user);
      router.push("/");
  } catch (error) {
      console.error("Login error:", error);
  } finally {
      setLoading(false);
  }};

  // Logout function
  const logout = async () => {
    setLoading(true);
    try {
      await fetch("/api/auth/logout", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
          },
      });
      setUser(null);
      destroyCookie(null, "token");
      router.push("/");
  } catch (error) {
      console.error("Logout error:", error);
  } finally {
      setLoading(false);
  };
};

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};


export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};