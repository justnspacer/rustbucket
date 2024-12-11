"use client";
import { useAuth } from "@/app/context/AuthContext";
import { useRouter } from "next/router";

const LogoutButton = () => {
  const { logout, loading } = useAuth();
  const router = useRouter();

  const handleLogout = async () => {
    await logout();
    router.push("/");
  };

  return (
    <button onClick={handleLogout} disabled={loading}>
      {loading ? "Logging out..." : "Logout"}
    </button>
  );
}