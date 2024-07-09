import axios from 'axios';
import { getCSRFToken } from '../utils/getCSRFToken';

const API_URL = 'https://localhost:7262/api';

interface VerifyResponse {
    status_code: number;
    message: string;
    data: {
        isSuccess: boolean;
    };
}

export interface ApiResponse {
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

export interface ApiResponseGetPost {
    status_code: number;
    message: string;
    data: PostDto[];
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

export interface PostDto {
    id: number;
    title: string;
    content: string;
    imageUrls: string[];
    imageUrl: string;
    videoUrl: string;
    isPublished: boolean;
    createdAt: Date;
    updatedAt: Date;
    userId: string;
}

export const registerEP = async (data: RegisterRequest) => {
    try {
        const csrfToken = getCSRFToken();
        const response = await axios.post<ApiResponse>(`${API_URL}/auth/register`, data, {
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
        const response = await axios.post<ApiResponse>(`${API_URL}/auth/login`, data, {
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
        const response = await axios.get<VerifyResponse>(`${API_URL}/auth/verify/token`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'X-CSRF-TOKEN': csrfToken || '',
            }
        });        
        return response.data.data.isSuccess;
    } catch (e) {
        console.error('error verifying token: ', e);
        return false;
    }
};


export const getAllPosts = async (): Promise<ApiResponseGetPost> => {
    try {
        const csrfToken = getCSRFToken();
        const response = await axios.get<ApiResponseGetPost>(`${API_URL}/post/get/all`, {
            headers: {
                'X-CSRF-TOKEN': csrfToken || '',
            }
        });
        return response.data;

    } catch (e) {
        console.error('Error fetching posts:', e);
        throw e;
    }    
};