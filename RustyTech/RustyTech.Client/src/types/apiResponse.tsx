export interface ResponseBase {
    isSuccess: boolean;
    message: string;
}

export interface RegisterRequest {
    email: string;
    password: string;
}

export interface LoginRequest {
    email: string;
    password: string;
    rememberMe: boolean;
}

export interface LoginResponse extends ResponseBase {
    isAuthenticated: boolean;
    user: GetUserRequest; 
}

export interface GetUserRequest {
    id: string;
    email: string;
    userName: string;
    verifiedAt: Date;
}

export interface VerifyEmailRequest {
    id: string;
    token: string;
}

export interface ResestPasswordRequest {
    email: string;
    resetCode : string;
    newPassword: string;
}

export interface UpdateUserRequest {
    userId: string;
    email: string;
    userName: string;
    birthYear: number;
}