import React from 'react';
import { Link } from 'react-router-dom';


const Footer: React.FC = () => {

    return (
        <footer>
            <div className='footer-item'>
                <Link className="footer-logo" to="/">Rust Bucket LLC</Link>
            </div>
        </footer>
    );
};

export default Footer;