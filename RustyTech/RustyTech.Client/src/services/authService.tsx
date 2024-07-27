import axios from 'axios';
import { getCSRFToken } from '../utils/getCSRFToken';
import { RegisterRequest, LoginRequest, ResponseBase } from '../types/apiResponse';
import { BASE_URL } from '../types/urls';

export const registerEP = async (data: RegisterRequest) => {
    try {
        const csrfToken = getCSRFToken();
        const response = await axios.post<ResponseBase>(`${BASE_URL}/auth/register`, data, {
            headers: {
                'X-CSRF-TOKEN': csrfToken || '',
            }
        });
        return response;
    } catch (e) {
        console.error('error with user registration: ', e);
    }
};

export const loginEP = async (data: LoginRequest) => {
    try {
        const csrfToken = getCSRFToken();
        const response = await axios.post<ResponseBase>(`${BASE_URL}/auth/login`, data, {
            headers: {
                'X-CSRF-TOKEN': csrfToken || '',
            }
        });
        return response;
    } catch (e) {
        console.error('error with user login: ', e);
    }
};

export const verifyTokenEP = async (token: string) => {
    try {
        const csrfToken = getCSRFToken();
        const response = await axios.get<ResponseBase>(`${BASE_URL}/auth/verify/token`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'X-CSRF-TOKEN': csrfToken || '',
            }
        });        
        return response.data.isSuccess;
    } catch (e) {
        console.error('error verifying token: ', e);
        return false;
    }
};