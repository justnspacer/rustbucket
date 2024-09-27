import React, { useRef } from 'react';
import { Link } from 'react-router-dom';

const HomePage: React.FC = () => {
    const divRef = useRef<HTMLDivElement>(null);

    const handleClick = () => {
        if (divRef.current) {
            divRef.current.style.maxHeight = '300px';
        }
    };

    return (
        <><main>
            <h1>Welcome to Rust Bucket</h1>
            <p>Let's work together to bring your vision to life on the web!</p>
            <div className="accordion">
                <div className="accordion-item">
                    <button onClick={handleClick} className="accordion-header">About</button>
                    <div ref={divRef} className='accordion-content'>
                        <p>We specialize in crafting custom websites and digital
                            solutions that elevate your online presence.
                            With a strong foundation in the latest web technologies,
                            We deliver responsive, user-friendly designs tailored
                            to meet the unique needs of your business.
                            Whether you're looking to build a new website from scratch,
                            optimize an existing one, or create an engaging e-commerce platform,
                            I am dedicated to providing high-quality,
                            innovative services that help you achieve your goals.
                            Let's work together to bring your vision to life on the web.</p>
                        <ul>
                            <li><Link to="/contact">Contact</Link></li>
                            <li><Link to="/request">Request Service</Link></li>
                        </ul>
                    </div>
                </div>
                <div className="accordion-item">
                    <button onClick={handleClick} className="accordion-header">Projects</button>
                    <div ref={divRef} className='accordion-content'>
                        <ul>Projects
                            <li><Link to="/posts">User Posts</Link></li>
                        </ul>
                    </div>
                </div>
                <div className="accordion-item">
                    <button onClick={handleClick} className="accordion-header">Request Service</button>
                    <div ref={divRef} className='accordion-content'>
                        <p>Request Form</p>
                    </div>
                </div>
            </div>
        </main>
        </>
    );
};

export default HomePage;