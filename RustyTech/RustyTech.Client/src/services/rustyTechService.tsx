import axios from 'axios';

const API_URL = 'https://localhost:7262/api';

interface VerifyResponse {
    status_code: number;
    message: string;
    data: {
        isSuccess: boolean;
    };
}

interface ApiResponse {
    status_code: number;
    message: string;
    data: {
        statusCode: number;
        isSuccess: boolean;
        user: User;
        isAuthenticated: boolean;
        token: string;
        message: string;
    };
}

interface RegisterRequest {
    email: string;
    password: string;
    confirmPassword: string;
    birthYear: number;
}

interface LoginRequest {
    email: string;
    password: string;
}

interface User {
    id: string;
    email: string;
}


export const registerEP = async (data: RegisterRequest) => {
    try {
        const response = await axios.post<ApiResponse>(`${API_URL}/auth/register`, data);
        return response;
    } catch (e) {
        console.error('error with user registration: ', e);
    }
};

export const loginEP = async (data: LoginRequest) => {
    try {
        const response = await axios.post<ApiResponse>(`${API_URL}/auth/login`, data);
        return response;
    } catch (e) {
        console.error('error with user login: ', e);
    }
};

export const verifyTokenEP = async (token: string) => {
    try {
        const response = await axios.get<VerifyResponse>(`${API_URL}/auth/verify/token`, {
            headers: {
                'Authorization': `Bearer ${token}`,
            }
        });        
        return response.data.data.isSuccess;
    } catch (e) {
        console.error('error verifying token: ', e);
        return false;
    }
};