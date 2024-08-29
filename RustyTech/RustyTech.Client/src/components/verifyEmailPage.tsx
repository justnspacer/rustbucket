import React from 'react';
import Form from './form';
import { verifyEmail } from '../services/accountService';
import { BASE_URL } from '../types/urls';

interface VerifyEmailFormValues {
    id: string;
    token: string;
}

const VerifyEmailPage: React.FC = () => {
    const initialValues: VerifyEmailFormValues = {
        id: '',
        token: '',
    };

    const handleSubmit = async (values: VerifyEmailFormValues) => {
        try {
            await verifyEmail(values);
            // Handle success
            console.log('Email verified successfully');
        } catch (error) {
            // Handle error
            console.error('Error verifying email:', error);
        }
    };

    return (
        <main>
            <h1>Verify Email</h1>
            <Form<VerifyEmailFormValues>
                initialValues={initialValues}
                onSubmit={handleSubmit}
            >
                {({ values, errors, handleChange, handleSubmit }) => (
                    <>
                        <div>
                            <label htmlFor="id">ID:</label>
                            <input
                                type="text"
                                id="id"
                                name="id"
                                value={values.id}
                                onChange={handleChange}
                            />
                            {errors.id && <span>{errors.id}</span>}
                        </div>
                        <div>
                            <label htmlFor="token">Token:</label>
                            <input
                                type="text"
                                id="token"
                                name="token"
                                value={values.token}
                                onChange={handleChange}
                            />
                            {errors.token && <span>{errors.token}</span>}
                        </div>
                        <button type="submit" onClick={handleSubmit}>
                            Verify Email
                        </button>
                        <a className="resend-email-link" href={`${BASE_URL}/account/resend/email`}>Resend Verification Email</a>
                    </>
                )}
            </Form>
        </main>
    );
};

export default VerifyEmailPage;
