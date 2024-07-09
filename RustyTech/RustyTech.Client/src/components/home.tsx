import React from 'react';
import { useAuth } from '../contexts/authContext';
import PostsList from './postsList';

const Home: React.FC = () => {
    const { message } = useAuth();

    return (
        <><main>
            {message && <p>{message}</p>}
            <h1>Welcome</h1>
            <h2>Posts</h2>
            <PostsList />
        </main>
        </>
    );
};

export default Home;