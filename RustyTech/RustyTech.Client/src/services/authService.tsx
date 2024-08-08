import axios from 'axios';
import { getCSRFToken } from '../utils/getCSRFToken';
import { RegisterRequest, LoginRequest, ApiResponse } from '../types/apiResponse';
import { BASE_URL } from '../types/urls';

export async function registerUser(data: RegisterRequest): Promise<ApiResponse> {
    try {
        const csrfToken = getCSRFToken();
        const response = await axios.post<ApiResponse>(`${BASE_URL}/auth/register`, data, {
            headers: {
                'X-CSRF-TOKEN': csrfToken || '',
            }
        });
        return response.data;
    } catch (e) {
        console.error('error with user registration: ', e);
        return { data: { isSuccess: false, message: 'Error registering user', statusCode: 500 } };
    }
}

export async function loginUser(data: LoginRequest): Promise<ApiResponse> {
    try {
        const csrfToken = getCSRFToken();
        const response = await axios.post<ApiResponse>(`${BASE_URL}/auth/login`, data, {
            headers: {
                'X-CSRF-TOKEN': csrfToken || '',
            }
        });
        return response.data;
    } catch (e) {
        console.error('error with user login: ', e);
        return { data: { isSuccess: false, message: 'Error registering user', statusCode: 500 } };
    }
}

export const verifyToken = async (token: string) => {
    try {
        const csrfToken = getCSRFToken();
        const response = await axios.get<ApiResponse>(`${BASE_URL}/auth/verify/token`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'X-CSRF-TOKEN': csrfToken || '',
            }
        });        
        return response.data;
    } catch (e) {
        console.error('error verifying token: ', e);
        return false;
    }
};