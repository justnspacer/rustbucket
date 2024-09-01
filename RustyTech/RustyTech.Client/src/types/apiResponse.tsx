export interface ResponseBase {
    data: {
        isSuccess: boolean;
        message: string;
    };
}

export interface AuthResponse {
    data: {
        isAuthenticated: boolean;
        isSuccess: boolean;
        user: GetUserRequest;
        message?: string;
    };
}

export interface LoginResponse {
    data: {
        isAuthenticated: boolean;
        isSuccess: boolean;
        user: GetUserRequest;
        message?: string;
    };
}

export interface RegisterRequest {
    email: string;
    password: string;
    confirmPassword: string;
    birthYear: number;
}

export interface LoginRequest {
    email: string;
    password: string;
    rememberMe: boolean;
}

export interface GetUserRequest {
    id: string;
    email: string;
    userName: string;
    verifiedAt: Date;
}

export interface VerifyEmailRequest {
    id?: string;
    token?: string;
}

export interface ResestPasswordRequest {
    email: string;
    resetCode: string;
    newPassword: string;
}

export interface UpdateUserRequest {
    userId: string;
    email: string;
    userName: string;
    birthYear: number;
}

export interface GetPostRequest {
    id: number;
    title?: string;
    content?: string;
    isPublished: boolean;
    keywords?: string[];
    createdAt: Date;
    updatedAt: Date;
    user: GetUserRequest;
    userId?: string;
    postType?: string;
    videoFile?: string;
    imageFile?: string;
    imageFiles?: string[];
}


export interface VerifyEmailValues {
    id: string;
    token: string;
}

export interface ApiResponse {
    message: string;
    isSuccess: boolean;
}