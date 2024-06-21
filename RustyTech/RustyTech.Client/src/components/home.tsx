import React from 'react';
import { useAuth } from '../contexts/authContext';

const Home: React.FC = () => {
    const { message } = useAuth();

    return (
        <><main>
            <h1>Home Component</h1>
            {message && <p>{message}</p>}
            <section>
            </section>
        </main>
        </>
    );
};

export default Home;