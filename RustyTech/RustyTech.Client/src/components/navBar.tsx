import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/authContext';

const NavBar: React.FC = () => {
    const { user, logoutUser } = useAuth();
    const [showDropdown, setShowDropdown] = useState(false);
    const dropdownRef = useRef<HTMLDivElement>(null);
    const navigate = useNavigate();


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

    const handleLogout = async () => {
        await logoutUser();
        navigate('/login');
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
                <div>Rust Bucket</div>
            </Link>
            <div className="links">
                {user ? (
                    <>
                        <span className="username-container">
                            <span className="username" onClick={handleDropdownClick}>{user?.email}</span>
                            {showDropdown && (
                                <div className="dropdown" ref={dropdownRef} onMouseLeave={handleMouseLeave}>
                                    <Link to={`/profile/${user.id}`}>Profile</Link>
                                    <button className='logout-button' onClick={handleLogout}>Logout</button>
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
