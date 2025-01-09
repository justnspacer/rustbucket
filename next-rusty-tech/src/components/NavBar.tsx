"use client";
import { useEffect, useRef, useState } from 'react';
import { useAuth } from "@/app/context/AuthContext";
import Image from 'next/image';
import LogoutButton from "@/components/LogoutButton";

export const NavBar = () => {
  const { user, loading } = useAuth();
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef<HTMLUListElement>(null);

  const handleDropdownClick = () => {
    setShowDropdown(!showDropdown);
};

const handleClickOutside = (event: MouseEvent) => {
    if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowDropdown(false);
    }
};

useEffect(() => {
  document.addEventListener('mousedown', handleClickOutside);
  return () => {
      document.removeEventListener('mousedown', handleClickOutside);
  };
}, []);

  return (
    <nav className='main-nav'>
        <h1 className='logo-link'><a href="/">Rust Bucket</a></h1>
        {loading ? (
          <span>Loading...</span>
        ) : user ? (
          <>
          <div className='username' onClick={handleDropdownClick}>Welcome, { user.user_metadata.displayName || user.email }!
          <ul className='dropdown' ref={dropdownRef}>
          {showDropdown && (<>
          <li className='dropdown-item'><a href="/myprofile">Profile</a></li>
          <li className='dropdown-item'><LogoutButton /></li>
          </>
          )}
          </ul>
          </div>
        </>):(
          <>
          <div className='auth-links'>
            <a className="flex items-center gap-2 hover:underline hover:underline-offset-4" href="/login">
            <Image aria-hidden src="/window.svg" alt="Window icon" width={16} height={16}/>Login</a>
            <a className="flex items-center gap-2 hover:underline hover:underline-offset-4" href="/register">
            <Image aria-hidden src="/file.svg" alt="Window icon" width={16} height={16}/>Register</a>
          </div>
          </>
        )}       
    </nav>
  ); 
};

export default NavBar;