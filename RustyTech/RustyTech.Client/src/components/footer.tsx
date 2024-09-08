import React from 'react';
import { Link } from 'react-router-dom';


const Footer: React.FC = () => {

    return (
        <footer>
            <div>
                <Link className="logo" to="/">Rust Bucket LLC</Link>
            </div>
        </footer>
    );
};

export default Footer;