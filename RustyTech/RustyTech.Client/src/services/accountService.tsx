import axios from 'axios';
import { BASE_URL } from '../types/urls';
import {
    ResponseBase, RegisterRequest, LoginRequest,
    LoginResponse, VerifyEmailRequest, ResestPasswordRequest,
    UpdateUserRequest
} from '../types/apiResponse';

async function sendPostRequest<TRequest, TResponse>(url: string, data: TRequest): Promise<TResponse> {
    const response = await axios.post<TResponse>(`${BASE_URL}${url}`, data, {
        headers: { 'Content-Type': 'application/json' },
        withCredentials: true
    });
    return response.data;
}

async function sendPostRequestNoCreds<TRequest, TResponse>(url: string, data: TRequest): Promise<TResponse> {
    const response = await axios.post<TResponse>(`${BASE_URL}${url}`, data, {
        headers: { 'Content-Type': 'application/json' },
    });
    return response.data;
}


async function sendGetRequest<TRequest, TResponse>(url: string, data: TRequest): Promise<TResponse> {
    const response = await axios.get<TResponse>(`${BASE_URL}${url}`, {
        params: data,
        withCredentials: true
    });
    return response.data;
}

/*
async function sendAuthRequest<AuthResponse>(url: string): Promise<AuthResponse> {
    const response = await axios.get<AuthResponse>(`${BASE_URL}${url}`, {
        withCredentials: true
    });
    return response.data;
}
*/

export async function register(data: RegisterRequest): Promise<ResponseBase> {
    return sendPostRequest<RegisterRequest, ResponseBase>('/api/account/register', data );
}

//export async function login(data: LoginRequest): Promise<LoginResponse> {
//    return sendPostRequestNoCreds<LoginRequest, LoginResponse>('/api/account/login', data);
//}

export async function verifyEmail(data: VerifyEmailRequest): Promise<ResponseBase> {
    return sendPostRequest<VerifyEmailRequest, ResponseBase>('/api/account/verify/email', data);
}

export async function resendEmail(email: string): Promise<ResponseBase>  {
    return sendPostRequest<string, ResponseBase>('/api/account/resend/email', email);
}

export async function forgotPassword(email: string): Promise<ResponseBase> {
    return sendPostRequest<string, ResponseBase>('/api/account/forgot/password', email);
}

export async function resetPassword(data: ResestPasswordRequest): Promise<ResponseBase> {
    return sendPostRequest<ResestPasswordRequest, ResponseBase>('/api/account/reset/password', data);
}

export async function updateUser(data: UpdateUserRequest): Promise<ResponseBase> {
    return sendPostRequest<UpdateUserRequest, ResponseBase>('/api/account/update', data);
}

export async function toggleTwoFactorAuth(userId: string): Promise<ResponseBase> {
    return sendPostRequest<string, ResponseBase>('/api/account/manage/2fa', userId);
}

export async function getInfo(userId: string): Promise<ResponseBase> {
    return sendGetRequest<string, ResponseBase>('/api/account/manage/info', userId);
}

export async function logout(): Promise<ResponseBase> {
    return sendPostRequest('/api/account/logout', {});
}

export async function login(loginRequest: LoginRequest) {
    try {
        const response = await axios.post(`${BASE_URL}/api/account/login`, {
            email: loginRequest.email,
            password: loginRequest.password,
            rememberMe: loginRequest.rememberMe
        }, {
            withCredentials: true
        });
        return response.data.data;
    } catch (e) {
        console.log('Error logging in:', e);
    }
}

export async function isAuthenticated() {
    try {
        const response = await axios.get(`${BASE_URL}/api/account/isAuthenticated`, {
            withCredentials: true
        });
        return response.data.data;
    } catch (e) {
        console.error('Error authenicating user:', e);
    }
}