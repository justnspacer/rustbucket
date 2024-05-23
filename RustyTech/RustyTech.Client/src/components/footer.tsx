import React from 'react';
import { Link } from 'react-router-dom';

const Footer: React.FC = () => {

    return (
        <footer>
            <div>
                <span>Made by </span>
                <span className="logo">
                    <Link to="/">Rust Bucket LLC</Link>
                </span>
            </div>
        </footer>
    );
};

export default Footer;