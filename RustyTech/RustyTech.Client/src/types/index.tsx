export interface User {
    id: string;
    email: string;
}

export interface AuthState {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    message: string;
}

export interface LoginRequest {
    email: string;
    password: string;
}

export interface RegisterRequest {
    email: string;
    password: string;
    birthYear: number;
}

export interface ApiResponse {
    isSuccess: boolean;
    message: string;
}