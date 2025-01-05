"use client";
import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { setCookie, destroyCookie } from "nookies";
import { User } from "@supabase/supabase-js";
import { useRouter } from "next/navigation";
import { supabase } from "@/app/utils/supabaseClient";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  resetPassword: (email: string) => Promise<void>;
  updateProfile: (profile: { displayName?: string; photoURL?: string }) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: {children: ReactNode}) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const { data: authListener } = supabase.auth.onAuthStateChange((event, session) => {
      if (session) {
        const token = session.access_token;
  
        setCookie(null, "token", token, {
          maxAge: 7 * 24 * 60 * 60, // 7 days
          path: "/",                // Accessible on all routes
          secure: true,             // Only send over HTTPS
          httpOnly: false,          // Set to true if setting from an API route
          sameSite: "lax",          // Protects against CSRF attacks
        });
  
        setUser(session.user);
      } else {
        setUser(null);
        setCookie(null, "token", "", {
          maxAge: -1, // Expire the cookie
          path: "/",
        });
      }
      setLoading(false);
    });
  
    return () => {
      authListener?.subscription.unsubscribe();
    };
  }, []);

  // Register function
  const register = async (email: string, password: string) => {
    setLoading(true);
    try {
      await supabase.auth.signUp({ email, password });
      router.push("/login");
    } catch (error) {
      console.error("Register error:", error);
    } finally {
      setLoading(false);
    }
  };

  // Login function
  const login = async (username: string, password: string) => {
    setLoading(true);
    try {
      const { data, error } = await supabase.auth.signInWithPassword({ email: username, password });

      if (error) {
        throw error;
      }

      const token = data.session?.access_token;

      setCookie(null, "token", token, {
        maxAge: 7 * 24 * 60 * 60, // 7 days
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
      await supabase.auth.signOut();
      setUser(null);
      destroyCookie(null, "token");
      router.push("/");
  } catch (error) {
      console.error("Logout error:", error);
  } finally {
      setLoading(false);
  };
};

 // Reset password function
 const resetPassword = async (email: string) => {
  setLoading(true);
  try {
    await supabase.auth.resetPasswordForEmail(email);
  } catch (error) {
    console.error("Reset password error:", error);
  } finally {
    setLoading(false);
  }
};

// Update user profile function
const updateProfile = async () => {
  if (user) {
    setLoading(true);
    try {
      await supabase.auth.updateUser(user);
      setUser({ ...user });
    } catch (error) {
      console.error("Update profile error:", error);
    } finally {
      setLoading(false);
    }
  }
};

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, resetPassword, updateProfile }}>
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