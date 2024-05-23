import React from 'react';
import { useAuth } from '../contexts/authContext';

const Home: React.FC = () => {
    const { message } = useAuth();

    return (
        <><main>
            {message && <p>{message}</p>}
            <h1>Home Component</h1>

        </main>
        </>
    );
};

export default Home;