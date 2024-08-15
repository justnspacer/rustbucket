import { RegisterRequest, LoginRequest, ApiResponse } from '../types/apiResponse';
import { BASE_URL } from '../types/urls';
import redaxios from 'redaxios';

export async function registerUser(params: RegisterRequest): Promise<ApiResponse> {

    const response = await redaxios.post(`${BASE_URL}/auth/register`, params);
    return response.data.data;
}

export async function loginUser(params: LoginRequest): Promise<ApiResponse> {
    const response = await redaxios.post(`${BASE_URL}/auth/login`, { session: params });
    return response.data.data;
}

export async function logout() {
    const response = await redaxios.delete(`${BASE_URL}/auth/logout`);
    return response.data.data;
}

export async function verifyToken(token: string): Promise<ApiResponse> {
    const response = await redaxios.post(`${BASE_URL}/auth/verify/token`, token);
    return response.data;
}