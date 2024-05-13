/* eslint-disable @typescript-eslint/no-explicit-any */
export interface User {
    id: string;
    email: string;
}

export interface AuthState {
    statusCode: number;
    isSuccess: boolean;
    message: string;
    user: User | null;
    isAuthenticated: boolean;
    isTokenValid: boolean;
    token: string;
    isLoading: boolean;
}

export interface LoginRequest {
    email: string;
    password: string;
}

export interface RegisterRequest {
    email: string;
    password: string;
    confirmPassword: string;
    birthYear: number;
}

export interface ApiResponse {
    statusCode: number;
    message: string;
    Data: {
        statusCode: number;
        isSuccess: boolean;
        user: User;
        isAuthenticated: boolean;
        token: string;
        message: string;
    };
}