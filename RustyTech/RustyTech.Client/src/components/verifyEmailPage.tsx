import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import useApiService from '../services/useApiService'; // Import the resendEmail method from accountService
import useRedirectIfAuthenticated from '../types/useRedirectIfAuthenticated';
import useQuery from '../types/useQueryParams';
import { ApiResponse, VerifyEmailRequest } from '../types/apiResponse';

const decodeBase64Token = (token: string) => {
    try {
        const decodedToken = atob(token); // Decode the Base64 string
        return decodedToken;
    } catch (error) {
        console.error("Failed to decode token", error);
        return undefined;
    }
};

const VerifyEmailPage: React.FC = () => {
    useRedirectIfAuthenticated();
    const [isEmailConfirmed, setIsEmailConfirmed] = useState<boolean>(false);
    const [isEmailSent, setIsEmailSent] = useState<boolean>(false);
    const [message, setMessage] = useState<string>('');
    const query = useQuery();
    const id = query.get('id');
    const token = query.get('token');
    const { verifyEmail, resendEmail } = useApiService();

    useEffect(() => {
        const verifyEmailAsync = async () => {
            try {
                if (id && token) {
                    const decodedToken = decodeBase64Token(token);
                    const values: VerifyEmailRequest = { id, token: decodedToken };
                    const response = await verifyEmail(values);
                    if (response?.data.data.isSuccess) {
                        setIsEmailConfirmed(response?.data.data.isSuccess);
                    } 
                }
            } catch (e) {
                setMessage(`error with frontend: ${e}`);
            }
        };
        verifyEmailAsync();
    }, [id, token, verifyEmail]);

    const handleResendEmail = async () => {
        try {
            if (id) {
                const response: ApiResponse = await resendEmail(id);
                if (response.isSuccess) {
                    setIsEmailSent(response.isSuccess);
                    setMessage(response.message);
                } else {
                    setMessage(response.message);
                }
            }
            else {
                setMessage('User id not found');
            }
            
        } catch (e) {
            setMessage(`error with frontend: ${e}`);
        }
    };

    return (
        <main>
            {isEmailConfirmed ? (
                <div>
                    <h2 className="api-success-message">{message}</h2>
                    <Link className="action-link" to="/login">Go to Login</Link>
                </div>
            ) : (
                <div>
                    <h2 className="api-error-message">{message}</h2>
                        <button className="api-action-button" onClick={handleResendEmail}>Resend Email</button>
                    {isEmailSent && <h3 className="api-success-message">Email sent successfully!</h3>}
                </div>
            )}
        </main>
    );
};

export default VerifyEmailPage;
