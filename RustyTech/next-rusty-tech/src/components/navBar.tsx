"use client";
import Image from 'next/image';
import { useAuth } from "@/app/context/AuthContext";
import LogoutButton from "@/components/LogoutButton";

export const NavBar = () => {
  const { user, loading } = useAuth();

  return (
    <nav>
      <ul>
        <li><a href="/">Home</a></li>
        {loading ? (
          <li>Loading...</li>
        ) : user ? (
          <>
          <li>Welcome, { user.displayName || user.email }</li>
          <li><LogoutButton /></li>
        </>):(
          <>
          <li>
            <a className="flex items-center gap-2 hover:underline hover:underline-offset-4" href="/login">
            <Image aria-hidden src="/window.svg" alt="Window icon" width={16} height={16}/>Login</a>
          </li>
          <li>
            <a className="flex items-center gap-2 hover:underline hover:underline-offset-4" href="/register">
            <Image aria-hidden src="/file.svg" alt="Window icon" width={16} height={16}/>Register</a>
          </li>
          </>
        )}       
      </ul>
    </nav>
  ); 
};

export default NavBar;