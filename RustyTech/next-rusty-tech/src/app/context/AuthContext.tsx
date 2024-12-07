import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import {auth} from "@/firebase/firebaseConfig";
import { onAuthStateChanged, User } from "firebase/auth";
import {setCookie, destroyCookie, parseCookies } from "nookies";

interface AuthContextType {
  user: User | null;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: {children: ReactNode}) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      if(user){
        setUser(user);
        user.getIdToken().then((token) => {
          setCookie(null, "token", token, {
            maxAge: 60 * 60 * 24 * 7,
            path: "/",
            secure: true,
            httpOnly: true,
            sameSite: "lax"
          });
        });

      }else{
        setUser(null);
        destroyCookie(null, "token");
      }
      setLoading(false);
    });
    return () => unsubscribe();
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading }}>
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