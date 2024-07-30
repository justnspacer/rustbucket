import axios from 'axios';
import { UserDto, ApiResponse } from '../types/apiResponse';
import { BASE_URL } from '../types/urls';


export async function getAllUsers(active: boolean = true): Promise<ApiResponse | null> {
    try {
        const response = await axios.get<ApiResponse>(`${BASE_URL}/api/users`, {
            params: { active },
        });
        return response.data;
    } catch (error) {
        console.error('Error occurred while fetching users:', error);
        return null;
    }
}

export async function getUserById(id: string): Promise<UserDto | null> {
    try {
        const response = await axios.get<UserDto>(`${BASE_URL}/api/users/${id}`);
        return response.data;
    } catch (error) {
        console.error(`Error occurred while fetching user with id ${id}:`, error);
        return null;
    }
}

export async function deleteUser(id: string): Promise<ApiResponse | null> {
    try {
        const response = await axios.delete<ApiResponse>(`${BASE_URL}/api/users/${id}`);
        return response.data;
    } catch (error) {
        console.error(`Error occurred while deleting user with id ${id}:`, error);
        return null;
    }
}
