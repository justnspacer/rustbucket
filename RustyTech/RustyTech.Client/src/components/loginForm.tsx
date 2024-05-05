import React, { useState } from 'react';
import { useAuth } from '../contexts/authContext';

const LoginForm: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const { login, message } = useAuth();

    const handleSubmit = async (event: React.FormEvent) => {
        event.preventDefault();
        await login({ email, password });
    };

    return (
        <form onSubmit={handleSubmit} id="loginForm">
            <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
            <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
            <button type="submit">Login</button>
            {message && <p>{message}</p>}
        </form>
    );
};

export default LoginForm;