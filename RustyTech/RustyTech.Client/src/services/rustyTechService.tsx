import axios from 'axios';
const API_URL = 'https://localhost:5001/api';

export const register = async (data: unknown) => axios.post(`${API_URL}/auth/register`, data);
export const login = async (data: unknown) => axios.post(`${API_URL}/auth/login`, data);
