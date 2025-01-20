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
        <h1 className='logo-link'><a href="/"> <span className='bg-gradient'></span>
        Rust Bucket</a></h1>
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
            <a className="login-link" href="/login">
            Login<i className="fa-regular fa-circle-right"></i></a>
          </div>
          </>
        )}       
    </nav>
  ); 
};

export default NavBar;