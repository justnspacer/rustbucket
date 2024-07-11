import React, { useState, useEffect, useRef } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/authContext';
import rustyImage from '../assets/rusty.png';

const NavBar: React.FC = () => {
    const { isAuthenticated, isTokenValid, logout, user } = useAuth();
    const [showDropdown, setShowDropdown] = useState(false);
    const dropdownRef = useRef<HTMLDivElement>(null);

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
        <nav>
            <Link className="logo" to="/">
                <div>
                    <img className='mainlogo' src={rustyImage} alt="Rusty Logo" />
                </div>
                <span>Rust Bucket</span>
            </Link>
            <div className="links">
                {isAuthenticated && isTokenValid ? (
                    <>
                        <span className="username-container">
                            <span className="username" onClick={handleDropdownClick}>{user?.email}</span>
                            {showDropdown && (
                                <div className="dropdown" ref={dropdownRef}>
                                    <Link to="/profile">Profile</Link>
                                    <Link to="/" onClick={logout}>Logout</Link>
                                </div>
                            )}
                        </span>
                    </>
                ) : (
                    <>
                        <Link className="login-link" to="/login">
                            <i className="fa-solid fa-user icon"></i>
                            Login
                        </Link>
                    </>
                )}
            </div>
        </nav>
    );
};

export default NavBar;
