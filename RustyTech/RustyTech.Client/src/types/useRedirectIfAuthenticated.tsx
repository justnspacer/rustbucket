import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/authContext';

const useRedirectIfAuthenticated = () => {
    const { userAuthenticated } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        if (userAuthenticated) {
            navigate('/');
        }
    }, [userAuthenticated, navigate]);
};

export default useRedirectIfAuthenticated;
