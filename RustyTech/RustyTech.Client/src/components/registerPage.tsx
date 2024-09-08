import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/authContext';
import useRedirectIfAuthenticated from '../types/useRedirectIfAuthenticated';
import Form from './form';
import { RegisterRequest } from '../types/apiResponse';

const RegisterPage: React.FC = () => {
    const { registerUser } = useAuth();
    const navigate = useNavigate();
    useRedirectIfAuthenticated();

    const initialValues: RegisterRequest = { userName: '', email: '', password: '', confirmPassword: '', birthYear: 0 };

    const handleSubmit = async (request: RegisterRequest) => {
        const response = await registerUser(request);
        if (response?.data.data.isSuccess) {
            navigate('/login');
        }
    };

    return (
        <>
            <Form
                initialValues={initialValues}
                onSubmit={handleSubmit}>
                {({ values, handleChange }) => (
                    <div id="registerForm">
                        <label htmlFor="userName">Username</label>
                        <input id="userName" autoComplete="username" type="text" name="userName" placeholder="Choose a username" value={values.userName} onChange={handleChange} required />
                        <label htmlFor="email">Email</label>
                        <input id="email" autoComplete="email" type="email" name="email" placeholder="Enter email" value={values.email} onChange={handleChange} required />

                        <label htmlFor="password">Password</label>
                        <input id="password" autoComplete="current-password" name="password" type="password" placeholder="Password" value={values.password} onChange={handleChange} required />

                        <label htmlFor="confirmPassword">Confirm Password</label>
                        <input id="confirmPassword" autoComplete="off" name="confirmPassword" type="password" placeholder="Confirm Password" value={values.confirmPassword} onChange={handleChange} required />

                        <label htmlFor="birthYear">Birth Year (Optional)</label>
                        <input id="birthYear" type="number" placeholder="Birth Year" name="birthYear" value={values.birthYear} onChange={handleChange} />

                        <button id="register-button" type="submit">Register</button>
                        <p className="login-line">Have an account?<Link to="/login">Login</Link></p>
                    </div>
                )}
            </Form></>
    );
};

export default RegisterPage;