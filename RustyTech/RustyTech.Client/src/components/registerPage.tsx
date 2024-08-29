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
    const [responseError, setResponseError] = React.useState<string>('');

    const initialValues: RegisterRequest = { email: '', password: '', confirmPassword: '', birthYear: 0 };

    const validate = (request: RegisterRequest) => {
        const errors: Partial<RegisterRequest> = {};
        if (!request.email) errors.email = 'Email is required';
        if (!request.password) errors.password = 'Password is required';
        if (!request.confirmPassword) {
            errors.confirmPassword = 'Confirm Password is required';
        } else if (request.password !== request.confirmPassword) {
            errors.confirmPassword = 'Passwords do not match';
        }
        return errors;
    };
    const handleSubmit = async (request: RegisterRequest) => {
        const response = await registerUser(request);
        if (response.isAuthenticated) {
            navigate('/verify/email');
        } else {
            setResponseError(response.message);
        }
    };

    return (
        <><div>
            {responseError && <span className="response-error">{responseError}</span>}
        </div>
            <Form
                initialValues={initialValues}
                validate={validate}
                onSubmit={handleSubmit}>
                {({ values, errors, handleChange }) => (
                    <div id="registerForm">
                        <label htmlFor="email">Email</label>
                        <input id="email" autoComplete="email" type="email" name="email" placeholder="Email" value={values.email} onChange={handleChange} required />

                        <label htmlFor="password">Password</label>
                        <input id="password" autoComplete="current-password" name="password" type="password" placeholder="Password" value={values.password} onChange={handleChange} required />
                        {errors.password && <div>{errors.password}</div>}


                        <label htmlFor="confirmPassword">Confirm Password</label>
                        <input id="confirm-password" autoComplete="current-password" name="confirm-password" type="password" placeholder="Confirm Password" value={values.confirmPassword} onChange={handleChange} required />
                        {errors.confirmPassword && <div>{errors.confirmPassword}</div>}


                        <label htmlFor="birthYear">Optional Birth Year</label>
                        <input type="number" placeholder="Year of Birth" value={values.birthYear} onChange={handleChange} />
                        <button id="register-button" type="submit">Register</button>
                        <p className="login-line">Have an account?<Link to="/login">Login</Link></p>
                    </div>
                )}
            </Form></>
    );
};

export default RegisterPage;