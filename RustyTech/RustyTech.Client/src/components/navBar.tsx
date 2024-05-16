import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/authContext';

const NavBar: React.FC = () => {
    const { isAuthenticated, isTokenValid, logout } = useAuth();

    return (
        <nav>
            <div className="logo">
                <Link to="/">Rust Bucket</Link>
            </div>
            <div className="links">
                {isAuthenticated && isTokenValid ? (
                    <>
                        <button onClick={logout}>Logout</button>
                    </>
                ) : (
                    <>
                        <Link to="/register">Register</Link>
                        <Link to="/login">Login</Link>
                    </>
                )}
            </div>
        </nav>
    );
};

export default NavBar;
