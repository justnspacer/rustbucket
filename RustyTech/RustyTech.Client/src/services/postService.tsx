import axios from 'axios';
import { getCSRFToken } from '../utils/getCSRFToken';
import { ApiResponse, PostDto } from '../types/apiResponse';
import { BASE_URL } from '../types/urls';

export async function createPost(post: PostDto): Promise<ApiResponse | null> {
    try {
        const response = await axios.post<ApiResponse>(`${BASE_URL}/posts`, post);
        return response.data;
    } catch (error) {
        console.log('Error creating post:', error);
        return null;
    }
}

export const getAllPosts = async (): Promise<ApiResponse[] | null> => {
    try {
        const csrfToken = getCSRFToken();
        const response = await axios.get<ApiResponse[]>(`${BASE_URL}/post/all`, {
            headers: {
                'X-CSRF-TOKEN': csrfToken || '',
            }
        });
        return response.data;
    } catch (e) {
        console.error('Error fetching posts:', e);
        return null;
    }
}

export const getPostById = async (postId: number): Promise<ApiResponse | null> => {
    try {
        const csrfToken = getCSRFToken();
        const response = await axios.get<ApiResponse>(`${BASE_URL}/post/${postId}`, {
            headers: {
                'X-CSRF-TOKEN': csrfToken || '',
            }
        });
        return response.data;
    } catch (e) {
        console.error('Error fetching post:', e);
        return null;
    }
}

export async function editPost<T extends PostDto>(newData: T): Promise<ApiResponse | null> {
    try {
        const response = await axios.put<ApiResponse>(`${BASE_URL}/posts/${newData.id}`, newData);
        return response.data;
    } catch (error) {
        console.error('Error editing post:', error);
        return null;
    }
}

export async function togglePostPublishedStatus(postId: number): Promise<ApiResponse | null> {
    try {
        const response = await axios.put<ApiResponse>(`${BASE_URL}/posts/publish/${postId}`);
        return response.data;
    } catch (error) {
        console.error('Error toggling post published status:', error);
        return null;
    }
}