import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/authContext'; // Assuming you have an AuthContext

const useRedirectIfAuthenticated = () => {
    const { userAuthenticated } = useAuth(); // Assuming your AuthContext provides this
    const navigate = useNavigate();

    useEffect(() => {
        if (userAuthenticated) {
            navigate('/');
        }
    }, [userAuthenticated, navigate]);
};

export default useRedirectIfAuthenticated;
