import React from 'react';
import { useAuth } from '../contexts/authContext';

const Home: React.FC = () => {
    const { message } = useAuth();

    return (
        <>{message && <p>{message}</p>}
        <h1>Home Component</h1></>
    );
};

export default Home;