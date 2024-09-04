import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/authContext';
import { LoginRequest } from '../types/apiResponse';
import useRedirectIfAuthenticated from '../types/useRedirectIfAuthenticated';
import Form from './form';

const LoginPage: React.FC = () => {
    const { loginUser } = useAuth();
    const navigate = useNavigate();
    useRedirectIfAuthenticated();
    const [responseError, setResponseError] = React.useState<string | undefined>('');


    const initialValues: LoginRequest = { email: '', password: '', rememberMe: false };

    const handleSubmit = async (request: LoginRequest) => {
        const response = await loginUser(request);
        if (response?.data.data.isAuthenticated) {
            navigate('/');
        } else {
            setResponseError(response?.data.data.message);
        }
    };

    return (
        <><div>
            {responseError && <span className="response-error">{responseError}</span>}
        </div>
            <Form
                initialValues={initialValues}
                onSubmit={handleSubmit}>
                {({ values, handleChange }) => (
                    <div id="loginForm">
                        <label htmlFor="email">Email</label>
                        <input id="email" autoComplete="email" type="email" name="email" placeholder="Email" value={values.email} onChange={handleChange} required />

                        <label htmlFor="password">Password</label>
                        <input id="password" autoComplete="current-password" name="password" type="password" placeholder="Password" value={values.password} onChange={handleChange} required />

                        <span className="flex">
                            <label className="rememberMeLabel" htmlFor="rememberMe">Remember Me</label>
                            <input id="rememberMe" className="rememberMe" name="rememberMe" type="checkbox" checked={values.rememberMe} onChange={handleChange} />
                        </span>
                        <button id="login-button" type="submit">Login</button>
                        <p className="register-line">Need an account?<Link to="/register">Register</Link></p>
                        <p><Link className="forgot-password" to="/forgot-password">Forgot Password?</Link></p>
                    </div>
                )}
            </Form></>
    );
};

export default LoginPage;
