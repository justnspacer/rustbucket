/* eslint-disable react-refresh/only-export-components */
/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import { register, login, logout, isAuthenticated } from '../services/accountService';
//import Spinner from '../components/spinner';
import { RegisterRequest, LoginRequest } from '../types/apiResponse';

interface AuthContextType {
    user: any;
    userAuthenticated: boolean;
    loading: boolean;
    error: any;
    loginUser: (data: LoginRequest) => Promise<any>;
    registerUser: (data: RegisterRequest) => Promise<any>;
    logoutUser: () => Promise<any>;
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

    useEffect(() => {
        const isUserAuthenticated = async () => {
            try {
                const response = await isAuthenticated();
                setUserAuthenticated(response.isAuthenticated);
                setUser(response.user);
                setLoading(false);
            } catch (e) {
                console.error('Error checking auth status:', e);
                setError(e)
            }
        };
        isUserAuthenticated();
    }, []);

    const registerUser = async (data: RegisterRequest) => {
        const response = await register(data);
        return response;
    };

    const loginUser = async (data: LoginRequest) => {
        const response = await login(data);
        setUser(response.user);
        setUserAuthenticated(response.isAuthenticated);
        return response;
    };

    const logoutUser = async () => {
        const response = await logout();
        setUser(response.user);
        setUserAuthenticated(response.isAuthenticated);
        return response;        
    };

    return (
        <AuthContext.Provider value={{ user, registerUser, userAuthenticated, loginUser, logoutUser, loading, error }}>
            {children}
        </AuthContext.Provider>
    );
};