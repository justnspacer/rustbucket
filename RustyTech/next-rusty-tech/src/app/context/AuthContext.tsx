"use client";
import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { auth } from "@/firebase/firebaseConfig";
import { onAuthStateChanged, User, signOut, getIdToken, UserCredential } from "@firebase/auth";
import { setCookie, destroyCookie, parseCookies } from "nookies";
import { useRouter } from "next/navigation";
import { loginUser } from "@/services/authService";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  isLoggedIn: () => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: {children: ReactNode}) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const cookies = parseCookies();
    const token = cookies.token;
    if (token) {
      console.log('auth', auth);
      onAuthStateChanged(auth, async (user) => {
        if (user) {
          const idToken = await user.getIdToken();
          if (idToken === token) {
            setUser(user);
            console.log("User is logged in", user);
          } else {
            setUser(null);
          }
        } else {
          setUser(null);
        }
        setLoading(false);
      });
    } else {
      setLoading(false);
    }
  }, []);

  // Login function
  const login = async (username: string, password: string) => {
    setLoading(true);
    try {
      const userCredential = await loginUser(username, password);
      const user = userCredential.user;
      const token = await user.getIdToken();
      
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

// Check if user is logged in
const isLoggedIn = () => {
  const cookies = parseCookies();
  return !!cookies.token;
};

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, isLoggedIn }}>
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