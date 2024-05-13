/* eslint-disable react-refresh/only-export-components */
/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { createContext, useContext, useState, ReactNode } from 'react';
import { AuthState, LoginRequest, RegisterRequest, ApiResponse } from '../types/index';
import axios from 'axios';

interface AuthContextType extends AuthState {
    login: (data: LoginRequest) => Promise<void>;
    register: (data: RegisterRequest) => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {

    const apiUrl = 'https://localhost:7262/api/auth';

    const [state, setState] = useState<AuthState>({
        statusCode: 0,
        isSuccess: false,
        message: '',
        user: null,
        isAuthenticated: false,
        isTokenValid: false,
        token: '',
        isLoading: false,
    });

    const handleRegisterResponse = async (response: ApiResponse) => {
        setState({
            isSuccess: response.Data.isSuccess,
            statusCode: response.Data.statusCode,
            message: response.Data.message,
            user: null,
            isAuthenticated: false,
            isTokenValid: false,
            token: '',
            isLoading: false,
        });
    };

    const handleLoginResponse = async (response: ApiResponse) => {
        setState({
            statusCode: response.Data.statusCode,
            isSuccess: response.Data.isSuccess,
            message: response.Data.message,
            user: response.Data.user,
            isAuthenticated: response.Data.isAuthenticated,
            isTokenValid: true,
            token: response.Data.token,
            isLoading: false,
        });

        const expirationDate = new Date();
        expirationDate.setDate(expirationDate.getDate() + 1);
        document.cookie = "rusty-expiry=" + expirationDate.toISOString() + "; path=/";
        document.cookie = "rusty-token=" + response.Data.token + "; path=/";
    };

    const register = async (data: RegisterRequest) => {
        try {
            const response = await axios.post<ApiResponse>(`${apiUrl}/register`, data);
            await handleRegisterResponse(response.data);
        } catch (error: any) {
            setState({ ...state, message: error.message || 'Registration failed' });
        }
    };

    const login = async (data: LoginRequest) => {
        try {
            const response = await axios.post<ApiResponse>(`${apiUrl}/login`, data);
            await handleLoginResponse(response.data);
        } catch (error: any) {
            setState({ ...state, message: error.message || 'Login failed' });
        }
    };

    const logout = () => {
        setState({
            ...state,
            user: null,
            isAuthenticated: false,
            isLoading: false,
            message: 'User logged out',
        });

        document.cookie = "rusty-expiry=" + null + "; path=/";
        document.cookie = "rusty-token=" + null + "; path=/";
    };

    return <AuthContext.Provider value={{ ...state, login, register, logout }}>
        {children}
    </AuthContext.Provider>;
};

export const useAuth = (): AuthContextType => {
    const context = useContext(AuthContext);
    if (!context) throw new Error('useAuth must be used within an AuthProvider');
    return context;
};

export default AuthProvider;