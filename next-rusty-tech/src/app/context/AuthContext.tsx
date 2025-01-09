"use client";
import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { setCookie, destroyCookie } from "nookies";
import { User } from "@supabase/supabase-js";
import { useRouter } from "next/navigation";
import { supabase } from "@/app/utils/supabaseClient";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  success: string;
  error: string;
  login: (username: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  resetPassword: (email: string) => Promise<void>;
  updateProfile: (updates: { displayName: string, email: string, photoURL: string, birthYear: number }) => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: {children: ReactNode}) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");
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
      if (isPasswordValid(password)) {
        await supabase.auth.signUp({ email, password });
        setSuccess("Registration successful");
        router.push("/login");
      }
    } catch (error) {
      console.error("Register error:", error);
      setError("Register error");
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
        setError(error.message);
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
    setSuccess("Logged in");
    setTimeout(() => {
      router.push("/"); 
    }, 1000);
  } catch (error) {
      console.error("Login error:", error);
      setError("Login error");
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
      setSuccess("User logged out");
      router.push("/");
  } catch (error) {
      console.error("Logout error:", error);
      setError("Logout error");
  } finally {
      setLoading(false);
  };
};

 // Reset password function
 const resetPassword = async (email: string) => {
  setLoading(true);
  try {
    await supabase.auth.resetPasswordForEmail(email);
    setSuccess("Password reset email sent");
  } catch (error) {
    console.error("Reset password error:", error);
    setError("Password reset failed");
  } finally {
    setLoading(false);
  }
};

// Update user profile function
const updateProfile = async (updates: { displayName: string, email: string, photoURL: string, birthYear: number }) => {
  if (user) {
    setLoading(true);
    try {
      const { data, error } = await supabase.auth.updateUser({
        data: {
          displayName: updates.displayName,
          email: updates.email,
          photoURL: updates.photoURL,
          birthYear: updates.birthYear,
        }
      });
      if (error) {
        setError(error.message);
        throw error;
      }
      setUser({ ...user, ...data });
      setSuccess("Profile updated");
    } catch (error) {
      console.error("Update profile error:", error);
      setError("Profile update failed");
    } finally {
      setLoading(false);
    }
  }
};

const isPasswordValid = (password: string) => {
  if (password === "") {
    setError("Password required");
    return false;
  }
  if(password.length < 6) {
    setError("Password must be at least 6 characters");
    return false;
  }
  if(password.length > 4096) {
    setError("Password must be less characters");
    return false;
  }
  if (!/[A-Z]/.test(password)) {
    setError("Password must contain at least one uppercase letter");
    return false;
  }
  if (!/[a-z]/.test(password)) {
    setError("Password must contain at least one lowercase letter");
    return false;
  }
  if (!/[0-9]/.test(password)) {
    setError("Password must contain at least one number");
    return false;
  }
  if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
    setError("Password must contain at least one special character");
    return false;
  }
  return true;
};

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, resetPassword, updateProfile, success, error }}>
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