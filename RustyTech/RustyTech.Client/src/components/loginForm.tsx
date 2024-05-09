import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/authContext';

const LoginForm: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { login, message } = useAuth();
    const auth = useAuth();
    const navigate = useNavigate();

    const handleLogin = async (event: React.FormEvent) => {
        event.preventDefault();
        await login({ email, password });

        if (auth.isAuthenticated) {
            navigate('/');
        } else {
            console.log('Login failed');
        }
    };

    return (
        <form onSubmit={handleLogin} id="loginForm">
            <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
            <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
            <button type="submit">Login</button>
            {message && <p>{message}</p>}
        </form>
    );
};

export default LoginForm;