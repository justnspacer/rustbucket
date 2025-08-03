'use client';
import { useEffect, useRef, useState } from 'react';
import { useAuth } from '@/app/context/AuthContext';
import LogoutButton from '@/components/LogoutButton';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCircleRight, faEllipsis } from '@fortawesome/free-solid-svg-icons';
import Link from 'next/link';
import { faBars } from '@fortawesome/free-solid-svg-icons/faBars';

export const NavBar = () => {
  const { user, loading } = useAuth();
  const [showDropdown, setShowDropdown] = useState(false);
  const [showMobileMenu, setShowMobileMenu] = useState(false);
  const dropdownRef = useRef<HTMLUListElement>(null);

  const handleDropdownClick = () => {
    setShowDropdown(!showDropdown);
  };

  const handleMobileMenuToggle = () => {
    const hamburger = document.querySelector('.hamburger') as HTMLElement;
    setShowMobileMenu(!showMobileMenu);
    if (showMobileMenu && hamburger) {
      hamburger.style.color = 'var(--foreground)';
    } else {
      hamburger.style.color = 'var(--background)';
    }
    setShowDropdown(false); // Close dropdown when mobile menu is opened
  };

  const handleClickOutside = (event: MouseEvent) => {
    if (
      dropdownRef.current &&
      !dropdownRef.current.contains(event.target as Node)
    ) {
      setShowDropdown(false);
    }
  };

  const closeMobileMenu = () => {
    setShowMobileMenu(false);
  };

  useEffect(() => {
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <nav className="main-nav">
      <h1 className="logo-link">
        <a href="/home">
          {' '}
          <span className="bg-gradient"></span>
          Rust Bucket
        </a>
      </h1>

      <ul className="nav-links">
        <li>
          <Link href="/business/about">About</Link>
        </li>
        <li>
          <Link href="/business/contact">Contact</Link>
        </li>
        <li>
          <Link href="/business/projects">Projects</Link>
        </li>
        <li>
          <Link href="/business/services">Services</Link>
        </li>
        <li>
          <Link href="/business/terms">Terms</Link>
        </li>
        <li>
          <Link href="/admin">Admin</Link>
        </li>
      </ul>
      {loading ? (
        <span>Loading...</span>
      ) : user ? (
        <>
          <div className="username" onClick={handleDropdownClick}>
            <img
              className="profile-image"
              src={user?.user_metadata.photoURL}
              alt={user?.email || 'User profile picture'}
            />{' '}
            {user.user_metadata.displayName || user.email}
            <ul className="dropdown" ref={dropdownRef}>
              {showDropdown && (
                <>
                  <li className="dropdown-item">
                    <a href="/auth/myprofile">Profile</a>
                  </li>
                  <li className="dropdown-item">
                    <LogoutButton />
                  </li>
                </>
              )}
            </ul>
          </div>
        </>
      ) : (
        <>
          <div className="auth-links">
            <a className="login-link" href="/auth/login">
              Login
              <FontAwesomeIcon icon={faCircleRight} />
            </a>
          </div>
        </>
      )}
      <button
        className="hamburger"
        aria-label="Toggle navigation"
        aria-expanded={showMobileMenu}
        onClick={handleMobileMenuToggle}
      >
        <FontAwesomeIcon icon={faBars} />
      </button>

      {/* Mobile Menu Overlay */}
      <div
        className={`mobile-menu-overlay ${showMobileMenu ? 'active' : ''}`}
        onClick={closeMobileMenu}
      ></div>

      {/* Mobile Menu */}
      <div className={`mobile-menu ${showMobileMenu ? 'active' : ''}`}>
        <ul className="mobile-nav-links">
          <li>
            <Link href="/business/about" onClick={closeMobileMenu}>
              About
            </Link>
          </li>
          <li>
            <Link href="/business/contact" onClick={closeMobileMenu}>
              Contact
            </Link>
          </li>
          <li>
            <Link href="/business/projects" onClick={closeMobileMenu}>
              Projects
            </Link>
          </li>
          <li>
            <Link href="/business/services" onClick={closeMobileMenu}>
              Services
            </Link>
          </li>
          <li>
            <Link href="/business/terms" onClick={closeMobileMenu}>
              Terms
            </Link>
          </li>
          <li>
            <Link href="/admin" onClick={closeMobileMenu}>
              Admin
            </Link>
          </li>

          {user ? (
            <>
              <li>
                <Link href="/auth/myprofile" onClick={closeMobileMenu}>
                  Profile
                </Link>
              </li>
              <li>
                <LogoutButton />
              </li>
            </>
          ) : (
            <li>
              <Link href="/auth/login" onClick={closeMobileMenu}>
                Login
              </Link>
            </li>
          )}
        </ul>
      </div>
    </nav>
  );
};

export default NavBar;
