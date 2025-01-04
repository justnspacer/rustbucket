import axios from 'axios';
import { BASE_API_URL } from '../types/urls';
import { AccessTokenResponse } from '../types/apiResponse';


export const spotifyCallBack = async (code: string, state: string) => {
    try {
        const response = await axios.post<AccessTokenResponse>(`${BASE_API_URL}/api/spotify/callback`, {code, state});
        return response.data;
    } catch (error) {
        console.log('Error during spotify callback:', error);
        return null;
    }
}