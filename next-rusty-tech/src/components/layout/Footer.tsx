"use client";
import { useEffect, useRef, useState } from 'react';

export const Footer = () => {
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef<HTMLUListElement>(null);

  const handleDropdownClick = () => {
    setShowDropdown(!showDropdown);
};

const handleMouseLeave = () => {
    setShowDropdown(false);
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
    <footer> 
      <div>
        <p>something else</p>
      </div>
      <div>
      <h1 className='logo-link'><a href="/home">Rust Bucket</a></h1>
      </div>
    </footer>
  ); 
};

export default Footer;