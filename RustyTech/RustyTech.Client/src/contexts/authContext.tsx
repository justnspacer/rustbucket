/* eslint-disable react-refresh/only-export-components */
/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { createContext, useContext, useState, ReactNode } from 'react';
import { AuthState, LoginRequest, RegisterRequest, ApiResponse, User } from '../types/index';
import axios from 'axios';

interface AuthContextType extends AuthState {
    login: (data: LoginRequest) => Promise<void>;
    register: (data: RegisterRequest) => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [state, setState] = useState<AuthState>({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        message: '',
    });

    const apiUrl = 'https://localhost:7262/api/auth';

    const login = async (data: LoginRequest) => {
        try {
            const response = await axios.post<ApiResponse & { user: User }>(`${apiUrl}/login`, data);
            if (response.data.isSuccess) {
                setState({
                    user: response.data.user,
                    isAuthenticated: true,
                    isLoading: false,
                    message: response.data.message,
                });
            } else {
                setState(s => ({ ...s, message: response.data.message }));
            }
        } catch (error: any) {
            setState(s => ({ ...s, message: error.message || 'Login failed' }));
        }
    };

    const register = async (data: RegisterRequest) => {
        try {
            const response = await axios.post<ApiResponse>(`${apiUrl}/register`, data);
            setState(s => ({ ...s, message: response.data.message }));
        } catch (error: any) {
            setState(s => ({ ...s, message: error.message || 'Registration failed' }));
        }
    };

    const logout = () => {
        setState({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            message: 'User logged out',
        });
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