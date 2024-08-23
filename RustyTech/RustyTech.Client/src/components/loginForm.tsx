import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/authContext';
import { LoginRequest } from '../types/apiResponse';

const LoginForm: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [rememberMe, setRememberMe] = useState(false);
    const [error, setError] = useState('');
    const { loginUser } = useAuth();
    const navigate = useNavigate();

    const handleLogin = async (event: React.FormEvent) => {
        event.preventDefault();
        const loginRequest: LoginRequest = {
            email: email,
            password: password,
            rememberMe: rememberMe
        };
        const response = await loginUser(loginRequest);
        if (response.data.isAuthenticated) {
            navigate('/');
        } else {
            console.log(response);
            if (response.data.message != null) {
                setError(response.data.message);
            }
        }        
    };

    return (
        <form onSubmit={handleLogin} id="loginForm">
            
            <label htmlFor="email">Email</label>
            <input id="email" autoComplete="email" type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />

            <label htmlFor="password">Password</label>
            <input id="password" autoComplete="current-password" type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
            <span className="flex">
                <label className="inline" htmlFor="checkbox">Remember Me</label>
                <input id="checkbox" className="checkbox" type="checkbox" checked={rememberMe} onChange={e => setRememberMe(e.target.checked)} />
            </span>
            <button type="submit">Login</button>
            <p className="register-line">Need an account?<Link to="/register">Register</Link></p>            

            {error && <p className="error">{error}</p>}
        </form>
    );
};

export default LoginForm;
