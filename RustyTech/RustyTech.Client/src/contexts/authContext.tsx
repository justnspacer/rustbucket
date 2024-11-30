/* eslint-disable react-refresh/only-export-components */
/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import useApiService from '../services/useApiService';
//import Spinner from '../components/spinner';
import { RegisterRequest, LoginRequest, ApiResponse, LoginResponse, GetUserRequest } from '../types/apiResponse';

interface AuthContextType {
    user: GetUserRequest;
    userAuthenticated: boolean;
    loading: boolean;
    error: string;
    loginUser: (data: LoginRequest) => Promise<LoginResponse | undefined>;
    registerUser: (data: RegisterRequest) => Promise<ApiResponse | undefined>;
    logoutUser: () => Promise<ApiResponse | undefined>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be within an AuthProvider');
    }
    return context;
}

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<any>(null);
    const [userAuthenticated, setUserAuthenticated] = useState<boolean>(false);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<any>(null);
    const { register, login, logout, isAuthenticated } = useApiService();
    
    useEffect(() => {
        const isUserAuthenticated = async () => {
            const storedUser = sessionStorage.getItem('user');
            if (!storedUser) {
                try {
                    const response = await isAuthenticated();
                    if (response?.data.data.isSuccess) {
                        setUserAuthenticated(response.data.data.isAuthenticated);
                        setUser(response.data.data.user);
                        sessionStorage.setItem('user', JSON.parse(response.data.data.user.toString()));
                        setLoading(false);
                    }
                } catch (e) {
                    console.error('Error checking auth status:', e);
                    sessionStorage.setItem('isAuthenicated', 'false');
                    setError(e)
                }
            } else {
                setUser(JSON.parse(storedUser));
                setUserAuthenticated(true);

            }
        };
        isUserAuthenticated();
    });

    const registerUser = async (data: RegisterRequest): Promise<ApiResponse | undefined> => {
        try {
            const response = await register(data);
            if (response?.data.data.isSuccess) {
                setLoading(false);
            }
            return response;
        } catch (e) {
            console.error('Error registering user:', e);
            setError(e)
        }

    };

    const loginUser = async (data: LoginRequest): Promise<LoginResponse | undefined> => {
        try {
            const response = await login(data);
            if (response?.data.data.isSuccess) {
                setUser(response?.data.data.user);
                setUserAuthenticated(response?.data.data.isAuthenticated);
                setLoading(false);
            }
            return response;

        } catch (e) {
            console.error('Error logging in:', e);
            setError(e)
        }
    };

    const logoutUser = async (): Promise<ApiResponse | undefined> => {
        try {
            const response = await logout();
            if (response?.data.data.isSuccess) {
                setUser(null);
                setUserAuthenticated(false);
                setLoading(false);
                return response;
            }
        } catch (e) {
            console.error('Error logging out:', e);
            setError(e)
        }

    };

    return (
        <AuthContext.Provider value={{ user, registerUser, userAuthenticated, loginUser, logoutUser, loading, error }}>
            {children}
        </AuthContext.Provider>
    );
};