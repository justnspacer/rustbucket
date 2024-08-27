import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/authContext';
import useRedirectIfAuthenticated from '../types/useRedirectIfAuthenticated';

const RegisterPage: React.FC = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [birthYear, setBirthYear] = useState('');
    const { registerUser } = useAuth();
    const navigate = useNavigate();
    useRedirectIfAuthenticated();

    useEffect(() => {
        if (isSuccess) {
            navigate('/login', { state: { message } });
        }
    }, [isSuccess, navigate, message]);

    const handleRegister = async (event: React.FormEvent) => {
        event.preventDefault();
        await registerUser({ email, password, birthYear: parseInt(birthYear) || 0 });
    };

    return (
        <form onSubmit={handleRegister} id="registerForm">
            <h1 className="header-one">Register here</h1>

            <label htmlFor="email">Email</label>
            <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />

            <label htmlFor="password">Password</label>
            <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />

            <label htmlFor="confirmPassword">Confirm Password</label>
            <input type="password" placeholder="Confirm Password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} required />

            <label htmlFor="birthYear">Birth Year</label>
            <input type="number" placeholder="Birth Year" value={birthYear} onChange={e => setBirthYear(e.target.value)} />

            <button type="submit">Register</button>
        </form>
    );
};

export default RegisterPage;