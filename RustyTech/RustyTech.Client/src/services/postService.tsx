import axios from 'axios';
import { ResponseBase, GetPostRequest } from '../types/apiResponse';
import { BASE_URL } from '../types/urls';


export const createPost = async (post: GetPostRequest) => {
    try {
        const response = await axios.post<ResponseBase>(`${BASE_URL}/posts`, post);
        return response.data;
    } catch (error) {
        console.log('Error creating post:', error);
        return null;
    }
}

export const getAllPosts = async () => {
    try {
        const response = await axios.get<ResponseBase>(`${BASE_URL}/post/all`, {
            
        });
        return response.data;
    } catch (e) {
        console.error('Error fetching posts:', e);
    }
}

export const getPostById = async (postId: number) => {
    try {
        const response = await axios.get<ResponseBase>(`${BASE_URL}/post/${postId}`, {
            
        });
        return response.data;
    } catch (e) {
        console.error('Error fetching post:', e);
    }
}

export const editPost = async <T extends GetPostRequest>(newData: T) => {
    try {
        const response = await axios.put<ResponseBase>(`${BASE_URL}/posts/${newData.id}`, newData);
        return response.data;
    } catch (e) {
        console.error('Error editing post:', e);
    }
}

export const togglePostPublishedStatus = async (postId: number) => {
    try {
        const response = await axios.put<ResponseBase>(`${BASE_URL}/posts/publish/${postId}`);
        return response.data;
    } catch (e) {
        console.error('Error toggling post published status:', e);
    }
}