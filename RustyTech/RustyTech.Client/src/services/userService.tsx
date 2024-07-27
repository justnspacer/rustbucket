import axios from 'axios';

export interface UserDto {
  id: string;
  name: string;
  email: string;
}

export interface ResponseBase {
  isSuccess: boolean;
  message: string;
}

export async function getAllUsers(active: boolean = true): Promise<UserDto[]> {
  try {
    const response = await axios.get<UserDto[]>('/api/users', {
      params: { active },
    });
    return response.data;
  } catch (error) {
    console.error('Error occurred while fetching users:', error);
    return [];
  }
}

export async function getUserById(id: string): Promise<UserDto | null> {
  try {
    const response = await axios.get<UserDto>(`/api/users/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error occurred while fetching user with id ${id}:`, error);
    return null;
  }
}

export async function deleteUser(id: string): Promise<ResponseBase> {
  try {
    const response = await axios.delete<ResponseBase>(`/api/users/${id}`);
    return response.data;
  } catch (error) {
    console.error(`Error occurred while deleting user with id ${id}:`, error);
    return { isSuccess: false, message: 'An error occurred' };
  }
}
