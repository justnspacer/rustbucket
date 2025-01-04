import axios from 'axios';
import { BASE_API_URL } from '../types/urls';


export async function getAllUsers() {
    try {
        const response = await axios.get(`${BASE_API_URL}/api/user/get/all`);
        return response.data.data;
    } catch (error) {
        console.error('Error occurred while fetching users:', error);
    }
}

export async function getUserById(id?: string) {
    try {
        const response = await axios.get(`${BASE_API_URL}/api/user/get?id=${id}`);
        return response.data.data;
    } catch (error) {
        console.error(`Error occurred while fetching user with id ${id}:`, error);
    }
}

export async function deleteUser(id: string) {
    try {
        const response = await axios.delete(`${BASE_API_URL}/api/user/delete?id=${id}`);
        return response.data.data;
    } catch (error) {
        console.error(`Error occurred while deleting user with id ${id}:`, error);
    }
}
