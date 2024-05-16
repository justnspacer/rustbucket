import axios, { AxiosError } from 'axios';

const API_URL = 'https://localhost:7262/api';

interface ApiResponse {
    statusCode: number;
    Data: {
        isSuccess: boolean;
    };
}

export const register = async (data: unknown) => axios.post(`${API_URL}/auth/register`, data);
export const login = async (data: unknown) => axios.post(`${API_URL}/auth/login`, data);


export const verifyToken = async (token: string) => {
    try {
        const response = await axios.get<ApiResponse>(`${API_URL}/auth/verify/token?token=${token}`);
        if (!response.data.Data.isSuccess) {
            throw new Error('Token is invalid');
        }
        const result = await response.data.Data.isSuccess;
        return result;
    } catch (e) {
        console.error('error verifying token: ', e);
        if (axios.isAxiosError(e)) {
            const axiosError = e as AxiosError;
            console.error('axios error details: ', axiosError.response?.data);
        }
        return false;
    }
};