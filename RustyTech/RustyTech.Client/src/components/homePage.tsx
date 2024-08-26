import React from 'react';
import { Link } from 'react-router-dom';

const HomePage: React.FC = () => {

    return (
        <><main>
            Welcome to Rust Bucket
            <p>Let's work together to bring your vision to life on the web!</p>
            <ul>
                <li><Link to="/about">About</Link></li>
                <li><Link to="/projects">Projects</Link></li>
                <li><Link to="/posts">Posts</Link></li>
            </ul>
        </main>
        </>
    );
};

export default HomePage;