"use client";
import { useAuth } from "@/app/context/AuthContext";

const LogoutButton = () => {
  const { logout, loading } = useAuth();

  const handleLogout = async () => {
    await logout();
  };

  return (
    <button className="button-logout" onClick={handleLogout} disabled={loading}>
      {loading ? "Logging out..." : "Logout"}
    </button>
  );
};

export default LogoutButton;