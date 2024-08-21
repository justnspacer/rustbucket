import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/authContext';

const LoginForm: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { loginUser } = useAuth();

    const handleLogin = async (event: React.FormEvent) => {
        event.preventDefault();
        try {
            const getd = loginUser({ email, password });

            console.log('Logged in, redirect?');
        } catch (e) {
            console.error(e);
        }
    };

    return (
        <form onSubmit={handleLogin} id="loginForm">
            <h1 className="header-one">Login</h1>

            <label htmlFor="email">Email</label>
            <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />

            <label htmlFor="password">Password</label>
            <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />

            <button type="submit">Login</button>
            <p className="register-line">Need an account?<Link to="/register">Register</Link></p>            
        </form>
    );
};

export default LoginForm;
