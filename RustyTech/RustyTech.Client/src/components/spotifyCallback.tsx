import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import { spotifyCallBack } from '../services/spotifyService';
import { AccessTokenResponse } from '../types/apiResponse';


const SpotifyCallbackPage: React.FC = () => {
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const code = queryParams.get('code');
    const state = queryParams.get('state');
    const [tokenResponse, setTokenResponse] = useState<AccessTokenResponse | null>();

    useEffect(() => {
        const callBacker = async () => {
            try {
                if (code != null && state != null) {
                    const response = await spotifyCallBack(code, state);
                    setTokenResponse(response);
                }
            } catch (err) {
                console.error('Error calling back from Spotify:', err);
            }
        };
        callBacker();
    }, [code, state]);

    return (
        <main>
            Calling back from Spotify
            {tokenResponse && <div>
                <h2>Token Response</h2>
                <p>Access Token: {tokenResponse.accessToken}</p>
                <p>Refresh Token: {tokenResponse.refreshToken}</p>
                <p>Expires In: {tokenResponse.expiresIn}</p>
                <p>Token Type: {tokenResponse.tokenType}</p>
            </div>}
        </main>
    );
};

export default SpotifyCallbackPage;