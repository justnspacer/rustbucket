"use client";
import { useEffect, useRef, useState } from 'react';
import { useAuth } from "@/app/context/AuthContext";
import LogoutButton from "@/components/LogoutButton";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCircleRight } from '@fortawesome/free-solid-svg-icons';
import Link from 'next/link';

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
      <div className='nav-left'>
      <h1 className='logo-link'><a href="/home"> <span className='bg-gradient'></span>
        Rust Bucket</a></h1>
        <ul className='nav-links'>
        <li><Link href="/business/about">About</Link></li>
          <li><Link href="/business/contact">Contact</Link></li>
          <li><Link href="/business/services">Services</Link></li>
          <li><Link href="/business/terms">Terms</Link></li>
          </ul>
      </div>
       
        {loading ? (
          <span>Loading...</span>
        ) : user ? (
          <>
          <div className='username' onClick={handleDropdownClick}>Welcome, { user.user_metadata.displayName || user.email }!
          <ul className='dropdown' ref={dropdownRef}>
          {showDropdown && (<>
          <li className='dropdown-item'><a href="/auth/myprofile">Profile</a></li>
          <li className='dropdown-item'><LogoutButton /></li>
          </>
          )}
          </ul>
          </div>
        </>):(
          <>
          <div className='auth-links'>
            <a className="login-link" href="/auth/login">
            Login<FontAwesomeIcon icon={faCircleRight}/></a>
          </div>
          </>
        )}       
    </nav>
  ); 
};

export default NavBar;