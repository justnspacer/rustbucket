/* eslint-disable react-refresh/only-export-components */
/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import axios from 'axios';
import { verifyToken } from '../services/rustyTechService';

interface AuthState {
    isAuthenticated: boolean;
    isTokenValid: boolean;
    token: string | null;
    isLoading: boolean;
    statusCode: number;
    isSuccess: boolean;
    message: string;
    user: User | null;
}

interface ApiResponse {
    statusCode: number;
    Data: {
        statusCode: number;
        isSuccess: boolean;
        user: User;
        isAuthenticated: boolean;
        token: string;
        message: string;
    };
}

interface LoginRequest {
    email: string;
    password: string;
}

interface RegisterRequest {
    email: string;
    password: string;
    confirmPassword: string;
    birthYear: number;
}

interface User {
    id: string;
    email: string;
}

interface AuthContextType extends AuthState {
    login: (data: LoginRequest) => Promise<void>;
    register: (data: RegisterRequest) => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [authState, setAuthState] = useState<AuthState>({
        isAuthenticated: false,
        isTokenValid: false,
        token: null,
        isLoading: false,
        statusCode: 0,
        isSuccess: false,
        message: '',
        user: null,
    });

    useEffect(() => {
        const token = localStorage.getItem('jwtToken');
        if (token) {
            verifyToken(token).then((response) => {
                setAuthState((prevState) => ({
                    ...prevState,
                    isAuthenticated: response,
                    isTokenValid: response,
                    token,
                    isLoading: false,
                    statusCode: 200,
                    isSuccess: response,
                    user: null,
                }));
            });
        }
    }, []);

    const apiUrl = 'https://localhost:7262/api/auth';

    const register = async (data: RegisterRequest) => {
        try {
            const response = await axios.post<ApiResponse>(`${apiUrl}/register`, data);
            setAuthState((prevState) => ({
                ...prevState,
                isSuccess: response.data.Data.isSuccess,
                statusCode: response.data.Data.statusCode,
                message: response.data.Data.message,
                user: null,
                isAuthenticated: false,
                isTokenValid: false,
                token: '',
                isLoading: false,
            }));
        } catch (error: any) {
            setAuthState((prevState) => ({
                ...prevState,
                message: error.message || 'Registration failed',
                isLoading: false,
            }));
        }
    };

    const login = async (data: LoginRequest) => {
        setAuthState((prevState) => ({ ...prevState, isLoading: true }));
        try {
            const response = await axios.post<ApiResponse>(`${apiUrl}/login`, data);
            if (response.data.Data.isSuccess) {
                const token = response.data.Data.token;
                localStorage.setItem('jwtToken', token);
                verifyToken(token).then((res) => {
                    setAuthState({
                        isAuthenticated: res,
                        isTokenValid: res,
                        token,
                        isLoading: false,
                        statusCode: response.data.Data.statusCode,
                        isSuccess: response.data.Data.isSuccess,
                        message: response.data.Data.message,
                        user: response.data.Data.user,
                    });
                });
            }
        } catch (error: any) {
            setAuthState((prevState) => ({
                ...prevState,
                message: error.message || 'Login failed',
                isLoading: false,
            }));
        }
    };

    const logout = (): void => {
        localStorage.removeItem('jwtToken');
        setAuthState({
            isAuthenticated: false,
            isTokenValid: false,
            token: null,
            isLoading: false,
            statusCode: 200,
            isSuccess: true,
            message: 'User logged out',
            user: null,
        });
    };

    return (
        <AuthContext.Provider value={{ ...authState, login, register, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = (): AuthContextType => {
    const context = useContext(AuthContext);
    if (!context) throw new Error('useAuth must be used within an AuthProvider');
    return context;
};

export default AuthProvider;