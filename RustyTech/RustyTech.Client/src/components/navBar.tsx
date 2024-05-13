import React from 'react';
import { Link } from 'react-router-dom';

interface NavBarProps {
  isAuthenticated: boolean;
  isTokenValid: boolean;
}

const NavBar: React.FC<NavBarProps> = ({ isAuthenticated, isTokenValid }) => {
  return (
    <nav>
      <div className="logo">
        <Link to="/">Rust Bucket LLC</Link>
      </div>
      <div className="links">
        {isAuthenticated && isTokenValid ? (
          <>
            <Link to="/logout">Logout</Link>
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
