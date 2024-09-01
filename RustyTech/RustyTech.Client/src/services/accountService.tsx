import axios from 'axios';
import { BASE_API_URL } from '../types/urls';
import {
    RegisterRequest, LoginRequest,
    VerifyEmailRequest, ResestPasswordRequest,
    UpdateUserRequest
} from '../types/apiResponse';

export async function register(request: RegisterRequest) {
    try {
        const response = await axios.post(`${BASE_API_URL}/api/account/register`, {
            email: request.email,
            password: request.password
        });
        return response.data.data;
    } catch (e) {
        console.error('Error registering user:', e);
    }
}

export async function login(request: LoginRequest) {
    try {
        const response = await axios.post(`${BASE_API_URL}/api/account/login`, {
            email: request.email,
            password: request.password,
            rememberMe: request.rememberMe
        });
        return response.data.data;
    } catch (e) {
        console.error('Error logging in:', e);
    }
}

export async function isAuthenticated() {
    try {
        const response = await axios.get(`${BASE_API_URL}/api/account/isAuthenticated`, {
            withCredentials: true
        });
        return response.data.data;
    } catch (e) {
        console.error('Error authenicating user:', e);
    }
}

export async function verifyEmail(request: VerifyEmailRequest) {
    try {
        const response = await axios.post(`${BASE_API_URL}/api/account/verify/email`, {
            id: request.id,
            token: request.token
        }, {
            withCredentials: true
        });
        return response.data.data;
    } catch (e) {
        console.error('Error verifying email:', e);
    }
}

export async function resendEmail(email: string) {
    try {
        const response = await axios.post(`${BASE_API_URL}/api/account/resend/email`, {
            email: email,
        }, {
            withCredentials: true
        });
        return response.data.data;
    } catch (e) {
        console.error('Error resending email:', e);
    }
}


export async function forgotPassword(email: string) {
    try {
        const response = await axios.post(`${BASE_API_URL}/api/account/forgot/password`, {
            email: email,
        });
        return response.data.data;
    } catch (e) {
        console.error('Bad token for forgot password request:', e);
    }
}

export async function resetPassword(request: ResestPasswordRequest) {
    try {
        const response = await axios.post(`${BASE_API_URL}/api/account/reset/password`, {
            email: request.email,
            resetCode: request.resetCode,
            newPassword: request.newPassword
        });
        return response.data.data;
    } catch (e) {
        console.error('Bad token for forgot password request:', e);
    }
}

export async function updateUser(request: UpdateUserRequest) {
    try {
        const response = await axios.put(`${BASE_API_URL}/api/account/forgot/update`, {
            userName: request.userName,
            email: request.email,
            birthYear: request.birthYear,
        }, {
            withCredentials: true
        });
        return response.data.data;
    } catch (e) {
        console.error('Bad token for forgot password request:', e);
    }
}


export async function toggleTwoFactorAuth(userId: string) {
    try {
        const response = await axios.post(`${BASE_API_URL}/api/account/manage/2fa`, {
            userId: userId,
        }, {
            withCredentials: true
        });
        return response.data.data;
    } catch (e) {
        console.error('Bad token for forgot password request:', e);
    }
}


export async function getInfo(userId: string) {
    try {
        const response = await axios.get(`${BASE_API_URL}/api/account/manage/info?userId=${userId}`, {
            withCredentials: true
        });
        return response.data.data;
    } catch (e) {
        console.error('Bad token for forgot password request:', e);
    }
}


export async function logout() {
    try {
        const response = await axios.post(`${BASE_API_URL}/api/account/logout`, {
        }, {
            withCredentials: true
        });
        return response.data.data;
    } catch (e) {
        console.error('Error logging out user:', e);
    }
}