/* eslint-disable react-refresh/only-export-components */
/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import { register, login, logout, isAuthenticated } from '../services/accountService';
//import Spinner from '../components/spinner';
import { RegisterRequest, LoginRequest, ResponseBase, LoginResponse } from '../types/apiResponse';

interface AuthContextType {
    user: any;
    userAuthenticated: boolean;
    loading: boolean;
    error: any;
    loginUser: (data: LoginRequest) => Promise<LoginResponse>;
    registerUser: (data: RegisterRequest) => Promise<ResponseBase>;
    logoutUser: () => Promise<ResponseBase>;
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
                if (response.data.isAuthenticated) {
                    setUserAuthenticated(true);
                    setUser(response.data.user);
                }
            } catch (e) {

                console.error('Error checking auth status:', e);
                setError(e);
            } finally {
                setUserAuthenticated(false);
                setUser(null);
                setLoading(false);
            }
        };
        isUserAuthenticated();
    }, []);

    const registerUser = async (data: RegisterRequest): Promise<ResponseBase> => {
        const response = await register(data);
        if (response.data.isSuccess) {
            console.log('have user check email and redirect to email verification form?');
            return response;
        } else {
            throw new Error(response.data.message);
        }

    };

    const loginUser = async (data: LoginRequest): Promise<LoginResponse> => {
        const response = await login(data);
        if (response.data.isSuccess && response.data.isAuthenticated) {
            setUser(response.data.user);
            setUserAuthenticated(response.data.isAuthenticated);
            return response;
        } else {
            return response;
        }
    };

    const logoutUser = async (): Promise<ResponseBase> => {
        const response = await logout();
        if (response.data.isSuccess) {
            setUser(null);
            setUserAuthenticated(false);
            console.log('user logged out');
            return response;
        }
        else {
            console.log(response.data.message);
            throw new Error(response.data.message);
        }
    };

    return (
        <AuthContext.Provider value={{ user, registerUser, userAuthenticated, loginUser, logoutUser, loading, error }}>
            {children}
        </AuthContext.Provider>
    );
};