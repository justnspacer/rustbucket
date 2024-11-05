import React, { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

const SpotifyCallbackPage: React.FC = () => {
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const code = queryParams.get('code');

    useEffect(() => {
        // Do something with the code parameter
        console.log(code);
    }, [code]);

    return (
        <main>
            Calling back from Spotify
        </main>
    );
};

export default SpotifyCallbackPage;