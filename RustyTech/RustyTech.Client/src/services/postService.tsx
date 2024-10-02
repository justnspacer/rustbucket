import axios from 'axios';
import { ResponseBase, GetPostRequest } from '../types/apiResponse';
import { BASE_API_URL } from '../types/urls';


export const createPost = async (post: GetPostRequest) => {
    try {
        const response = await axios.post<ResponseBase>(`${BASE_API_URL}/api/posts`, post);
        return response.data;
    } catch (error) {
        console.log('Error creating post:', error);
        return null;
    }
}

export async function getAllPosts() {
    try {
        const response = await axios.get(`${BASE_API_URL}/api/post/all`);
        return response.data.data;
    } catch (e) {
        console.error('Error fetching posts:', e);
    }
}

export async function getPostById(postId: number) {
    try {
        const response = await axios.get(`${BASE_API_URL}/api/post/${postId}`);
        return response.data.data;
    } catch (e) {
        console.error('Error fetching post:', e);
    }
}

export async function getPostByUserId(userId?: string) {
    try {
        const response = await axios.get(`${BASE_API_URL}/api/post/user?userId=${userId}`);
        return response.data.data;
    } catch (e) {
        console.error('Error fetching user post:', e);
    }
}

export const editPost = async <T extends GetPostRequest>(newData: T) => {
    try {
        const response = await axios.put<ResponseBase>(`${BASE_API_URL}/api/posts/${newData.id}`, newData);
        return response.data;
    } catch (e) {
        console.error('Error editing post:', e);
    }
}

export const togglePostPublishedStatus = async (postId: number) => {
    try {
        const response = await axios.put<ResponseBase>(`${BASE_API_URL}/api/posts/publish/${postId}`);
        return response.data;
    } catch (e) {
        console.error('Error toggling post published status:', e);
    }
}