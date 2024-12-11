"use client";
import { signIn, signUp } from "@/firebase/authService";
import Image from 'next/image';
import { useRouter } from "next/navigation";
import { useAuth } from "@/app/context/AuthContext";
import { useEffect } from "react";
import LogoutButton from "@/components/LogoutButton";
import {parseCookies } from "nookies";

export const NavBar = () => {
  const {user} = useAuth();
  const router = useRouter();

  if (user) {
    return <p>Welcome, {user.displayName}</p>;
  }
  return (
    <>
      <a
        className="flex items-center gap-2 hover:underline hover:underline-offset-4"
        href="/login"
      >
        <Image
          aria-hidden
          src="/window.svg"
          alt="Window icon"
          width={16}
          height={16}
        />
        Login
      </a>
      <a
        className="flex items-center gap-2 hover:underline hover:underline-offset-4"
        href="/register"
      >
        <Image
          aria-hidden
          src="/file.svg"
          alt="Window icon"
          width={16}
          height={16}
        />
        Register
      </a>
    </>
  );
 
};

export default NavBar;