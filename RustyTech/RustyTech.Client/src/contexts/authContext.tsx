/* eslint-disable react-refresh/only-export-components */
/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { registerUser, loginUser, verifyToken } from '../services/authService';
import { getJwtClaims } from '../utils/getJwtClaims';
import Spinner from '../components/spinner';
import { RegisterRequest, LoginRequest } from '../types/apiResponse';

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
        isLoading: true,
        statusCode: 0,
        isSuccess: false,
        message: '',
        user: null,
    });

    useEffect(() => {
        const token = localStorage.getItem('jwtToken');
        if (!token) {
            setAuthState((prevState) => ({
                ...prevState,
                isLoading: false, // Set isLoading to false if token is not present
                message: 'no token found',
            }));
            return;
        }

        setAuthState((prevState) => ({
            ...prevState,
            isLoading: true, // Set isLoading to true before token verification
            message: 'loading...',
        }));

        verifyToken(token).then((response) => {
            if (response) {
                const claims = getJwtClaims(token);
                if (claims) {
                    const userClaimed = { id: claims.nameIdentifier, email: claims.email };
                    setAuthState({
                        isAuthenticated: true,
                        isTokenValid: true,
                        token,
                        isLoading: false,
                        statusCode: 200,
                        isSuccess: true,
                        message: 'Welcome back',
                        user: userClaimed,
                    });
                }
            } else {
                setAuthState((prevState) => ({
                    ...prevState,
                    isAuthenticated: false,
                    isTokenValid: false,
                    token: null,
                    isLoading: false,
                    statusCode: 401,
                    isSuccess: false,
                    message: 'no token found',
                    user: null,
                }));
                localStorage.removeItem('jwtToken');
            }
        })
            .catch(() => {
                setAuthState((prevState) => ({
                    ...prevState,
                    isAuthenticated: false,
                    isTokenValid: false,
                    token: null,
                    isLoading: false,
                    statusCode: 500,
                    isSuccess: false,
                    message: 'Token verification failed',
                    user: null,
                }));
            });
    }, []);


    const register = async (data: RegisterRequest) => {
        try {
            const response = await registerUser(data); 

            if (response != null) {               
                setAuthState((prevState) => ({
                    ...prevState,
                    user: null,
                    isAuthenticated: false,
                    isTokenValid: false,
                    token: '',
                    isLoading: false,
                }));
            }
            else {
                console.error('error with registration');
            }

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
            const response = await loginUser(data);
            const token = response.data;
            if (token) {
                localStorage.setItem('jwtToken', "token");
            }
            else {
                console.error('missing token for login');
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

    if (authState.isLoading) {
        return <Spinner />;
    }

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