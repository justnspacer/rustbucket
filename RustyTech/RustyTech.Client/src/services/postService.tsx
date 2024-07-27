import axios from 'axios';
import { getCSRFToken } from '../utils/getCSRFToken';

const API_URL = 'https://localhost:7262/api';

export interface PostDto {
    id: number;
    title: string;
    content: string;
    createdAt: Date;
    updatedAt: Date;
    userId: string;
    isPublished: boolean;
    postType: string;
    keywords: string[];
    imageUrl: string;
    videoUrl: string;
    imageUrls: string[];
}

export interface ResponseBase {
    isSuccess: boolean;
    message: string;
}

export interface ApiResponseGetPost {
    status_code: number;
    message: string;
    data: PostDto[];
}

export interface ApiResponseGetSinglePost {
    status_code: number;
    message: string;
    data: PostDto;
}

export async function createPost(post: PostDto): Promise<ResponseBase> {
    try {
        const response = await axios.post<ResponseBase>(`${API_URL}/posts`, post);
        return response.data;
    } catch (error) {
        return { isSuccess: false, message: "unknown error" };
    }
}

export const getAllPosts = async (): Promise<ApiResponseGetPost> => {
    try {
        const csrfToken = getCSRFToken();
        const response = await axios.get<ApiResponseGetPost>(`${API_URL}/post/all`, {
            headers: {
                'X-CSRF-TOKEN': csrfToken || '',
            }
        });
        return response.data;
    } catch (e) {
        console.error('Error fetching posts:', e);
        throw e;
    }
}

export const getPostById = async (postId: number): Promise<ApiResponseGetSinglePost> => {
    try {
        const csrfToken = getCSRFToken();
        const response = await axios.get<ApiResponseGetSinglePost>(`${API_URL}/post/${postId}`, {
            headers: {
                'X-CSRF-TOKEN': csrfToken || '',
            }
        });
        return response.data;
    } catch (e) {
        console.error('Error fetching post:', e);
        throw e;
    }
}

export async function editPost<T extends PostDto>(newData: T): Promise<ResponseBase> {
    try {
        const response = await axios.put<ResponseBase>(`${API_URL}/posts/${newData.id}`, newData);
        return response.data;
    } catch (error) {
        return { isSuccess: false, message: "unknown error" };
    }
}

export async function togglePostPublishedStatus(postId: number): Promise<ResponseBase> {
    try {
        const response = await axios.put<ResponseBase>(`${API_URL}/posts/${postId}/togglePublishedStatus`);
        return response.data;
    } catch (error) {
        return { isSuccess: false, message: "unknown error" };
    }
}