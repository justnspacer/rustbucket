/* eslint-disable @typescript-eslint/no-explicit-any */
import axios from 'axios';
import { BASE_API_URL } from '../types/urls';
import {
    RegisterRequest, LoginRequest, VerifyEmailRequest, ResestPasswordRequest,
    UpdateUserRequest, LoginResponse, AuthResponse, ApiResponse
} from '../types/apiResponse';
import { useMessage } from '../contexts/messageContext';

const useApiService = () => {
    const { setMessage } = useMessage();

    const extractMessage = (response: any): string => {
        if (response?.data?.data?.message) {
            return response.data.data.message;
        } else if (response?.title) {
            return response.title;
        } else {
            return '';
        }
    };

    const handleApiResponse = (response: any) => {
        const message = extractMessage(response);
        setMessage(message);
    };

    const register = async (request: RegisterRequest): Promise<ApiResponse | undefined> => {
        return new Promise((resolve, reject) => {
            axios.post(`${BASE_API_URL}/api/account/register`, {
                userName: request.userName,
                email: request.email,
                password: request.password,
                confirmPassword: request.confirmPassword,
                birthYear: request.birthYear
            })
                .then(response => {
                    handleApiResponse(response);
                    resolve(response);
                })
                .catch(err => {
                    console.error('Error registering user:', err);
                    reject(err);
                });
        });
    }

    const login = async (request: LoginRequest): Promise<LoginResponse | undefined> => {
        return new Promise((resolve, reject) => {
            axios.post(`${BASE_API_URL}/api/account/login`, {
                email: request.email,
                password: request.password,
                rememberMe: request.rememberMe
            }, {
                withCredentials: true
            })
                .then(response => {
                    handleApiResponse(response);
                    resolve(response);
                })
                .catch(err => {
                    console.error('Error logging in:', err);
                    reject(err);
                });
        });
    }

    const isAuthenticated = async (): Promise<AuthResponse | undefined> => {
        return new Promise((resolve, reject) => {
            axios.get(`${BASE_API_URL}/api/account/isAuthenticated`, {
                withCredentials: true
            })
                .then(response => {
                    handleApiResponse(response);
                    resolve(response);
                })
                .catch(err => {
                    console.error('Error authenicating:', err);
                    reject(err);
                });
        });
    }

    const logout = async (): Promise<ApiResponse | undefined> => {
        return new Promise((resolve, reject) => {
            axios.post(`${BASE_API_URL}/api/account/logout`, {
            }, {
                withCredentials: true
            }).then(response => {
                handleApiResponse(response);
                resolve(response);
            }).catch(err => {
                console.error('Error logging out user:', err);
                reject(err)
            })
        });
    }

    const verifyEmail = async (request: VerifyEmailRequest): Promise<ApiResponse | undefined> => {
        return new Promise((resolve, reject) => {
            axios.post(`${BASE_API_URL}/api/account/verify/email`, {
                id: request.id,
                token: request.token
            }, {
                withCredentials: true
            }).then(response => {
                handleApiResponse(response);
                resolve(response);
            }).catch(err => {
                console.error('Error verifying email:', err);
                reject(err)
            })
        });
    }

    const resendEmail = async (email: string): Promise<ApiResponse | undefined> => {
        return new Promise((resolve, reject) => {
            axios.post(`${BASE_API_URL}/api/account/resend/email`, {
                email: email,
            }, {
                withCredentials: true
            }).then(response => {
                handleApiResponse(response);
                resolve(response);
            }).catch(err => {
                console.error('Error resending email:', err);
                reject(err)
            })
        });
    }

    const forgotPassword = async (email: string): Promise<ApiResponse | undefined> => {
        return new Promise((resolve, reject) => {
            axios.post(`${BASE_API_URL}/api/account/forgot/password`, {
                email: email,
            }).then(response => {
                handleApiResponse(response);
                resolve(response);
            }).catch(err => {
                console.error('Error forget password request:', err);
                reject(err)
            })
        });
    }

    const resetPassword = async (request: ResestPasswordRequest): Promise<ApiResponse | undefined> => {
        return new Promise((resolve, reject) => {
            axios.post(`${BASE_API_URL}/api/account/reset/password`, {
                email: request.email,
                resetCode: request.resetCode,
                newPassword: request.newPassword
            }).then(response => {
                handleApiResponse(response);
                resolve(response);
            }).catch(err => {
                console.error('Bad token for forgot password request:', err);
                reject(err)
            })
        });
    }

    const updateUser = async (request: UpdateUserRequest): Promise<ApiResponse | undefined> => {
        return new Promise((resolve, reject) => {
            axios.put(`${BASE_API_URL}/api/account/update`, {
                userName: request.userName,
                email: request.email,
                birthYear: request.birthYear,
            }, {
                withCredentials: true
            }).then(response => {
                handleApiResponse(response);
                resolve(response);
            }).catch(err => {
                console.error('Error updating user:', err);
                reject(err)
            })
        });
    }

    const toggleTwoFactorAuth = async (userId: string): Promise<ApiResponse | undefined> => {
        return new Promise((resolve, reject) => {
            axios.post(`${BASE_API_URL}/api/account/manage/2fa`, {
                userId: userId,
            }, {
                withCredentials: true
            }).then(response => {
                handleApiResponse(response);
                resolve(response);
            }).catch(err => {
                console.error('Error resending email:', err);
                reject(err)
            })
        });
    }

    const getInfo = async (userId: string): Promise<ApiResponse | undefined> => {
        return new Promise((resolve, reject) => {
            axios.get(`${BASE_API_URL}/api/account/manage/info?userId=${userId}`, {
                withCredentials: true
            }).then(response => {
                handleApiResponse(response);
                resolve(response);
            }).catch(err => {
                console.error('Error resending email:', err);
                reject(err)
            })
        });
    }

    return {
        register, login, isAuthenticated,
        logout, verifyEmail, resendEmail,
        forgotPassword, resetPassword, updateUser,
        toggleTwoFactorAuth, getInfo
    };
}

export default useApiService;