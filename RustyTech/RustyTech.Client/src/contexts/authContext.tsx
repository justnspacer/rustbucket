/* eslint-disable react-refresh/only-export-components */
/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { createContext, useContext, useState, ReactNode } from 'react';
import { register, login, logout } from '../services/accountService';
//import Spinner from '../components/spinner';
import { RegisterRequest, LoginRequest, ResponseBase, LoginResponse } from '../types/apiResponse';

interface AuthContextType {
    user: any;
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
}


export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [user, setUser] = useState<any>(null);


    const registerUser = async (data: RegisterRequest): Promise<ResponseBase> => {
        const response = await register(data);
        if (response.isSuccess) {
            console.log('have user check email and redirect to email verification form?');
            return response;
        } else {
            throw new Error(response.message);
        }

    };

    const loginUser = async (data: LoginRequest): Promise<LoginResponse> => {
        const response = await login(data);
        if (response.isSuccess) {
            setUser(response.user);
            console.log('redirect to previous page after login?');
            return response;
        } else {
            throw new Error(response.message);
        }
    };

    const logoutUser = async (): Promise<ResponseBase> => {
        const response = await logout();
        if (response.isSuccess) {
            setUser(null);
            console.log('user logged out');
            return response;
        }
        else {
            console.log(response.message);
            throw new Error(response.message);
        }
    };

    return (
        <AuthContext.Provider value={{ user, registerUser, loginUser, logoutUser }}>
            {children}
        </AuthContext.Provider>
    );
};