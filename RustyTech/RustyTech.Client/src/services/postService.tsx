import axios from 'axios';
import { getCSRFToken } from '../utils/getCSRFToken';
import { ApiResponse, PostDto } from '../types/apiResponse';
import { BASE_URL } from '../types/urls';

export const createPost = async (post: PostDto) => {
    try {
        const response = await axios.post<ApiResponse>(`${BASE_URL}/posts`, post);
        return response.data;
    } catch (error) {
        console.log('Error creating post:', error);
        return null;
    }
}

export const getAllPosts = async () => {
    try {
        const csrfToken = getCSRFToken();
        const response = await axios.get<ApiResponse>(`${BASE_URL}/post/all`, {
            headers: {
                'X-CSRF-TOKEN': csrfToken || '',
            }
        });
        return response.data.data;
    } catch (e) {
        console.error('Error fetching posts:', e);
    }
}

export const getPostById = async (postId: number) => {
    try {
        const csrfToken = getCSRFToken();
        const response = await axios.get<ApiResponse>(`${BASE_URL}/post/${postId}`, {
            headers: {
                'X-CSRF-TOKEN': csrfToken || '',
            }
        });
        return response.data.data;
    } catch (e) {
        console.error('Error fetching post:', e);
    }
}

export const editPost = async <T extends PostDto>(newData: T) => {
    try {
        const response = await axios.put<ApiResponse>(`${BASE_URL}/posts/${newData.id}`, newData);
        return response.data;
    } catch (e) {
        console.error('Error editing post:', e);
    }
}

export const togglePostPublishedStatus = async (postId: number) => {
    try {
        const response = await axios.put<ApiResponse>(`${BASE_URL}/posts/publish/${postId}`);
        return response.data;
    } catch (e) {
        console.error('Error toggling post published status:', e);
    }
}