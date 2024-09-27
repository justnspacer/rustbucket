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
            <Link className="logo nav-item" to="/">Rust Bucket</Link>

            {user ? (
                <>
                    <div className="drop-container nav-item">
                        <i className="fa-solid fa-ellipsis-vertical" onClick={handleDropdownClick}></i>
                        {showDropdown && (
                            <section className="dropdown-backdrop">
                                <div className="dropdown" ref={dropdownRef} onMouseLeave={handleMouseLeave}>
                                    <span className="username">Hey {user.userName}</span>
                                    <Link to={`/profile/${user.id}`}>Check Profile</Link>
                                    <button className='logout-button' onClick={handleLogout}>Logout</button>
                                </div>
                            </section>
                        )}
                    </div>
                </>
            ) : (
                <>
                    <Link className="login-link nav-item" to="/login">
                        {/*                        <i className="fa-solid fa-user icon"></i>*/}
                        Login
                    </Link>
                </>
            )}
        </nav>
    );
};

export default NavBar;
