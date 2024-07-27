import axios from 'axios';
import { getCSRFToken } from '../utils/getCSRFToken';
import { ResponseBase, PostDto } from '../types/apiResponse';
import { BASE_URL } from '../types/urls';

export async function createPost(post: PostDto): Promise<ResponseBase> {
    try {
        const response = await axios.post<ResponseBase>(`${BASE_URL}/posts`, post);
        return response.data;
    } catch (error) {
        return { isSuccess: false, message: "unknown error" };
    }
}

export const getAllPosts = async (): Promise<PostDto[]> => {
    try {
        const csrfToken = getCSRFToken();
        const response = await axios.get<PostDto[]>(`${BASE_URL}/post/all`, {
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

export const getPostById = async (postId: number): Promise<PostDto> => {
    try {
        const csrfToken = getCSRFToken();
        const response = await axios.get<PostDto>(`${BASE_URL}/post/${postId}`, {
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
        const response = await axios.put<ResponseBase>(`${BASE_URL}/posts/${newData.id}`, newData);
        return response.data;
    } catch (error) {
        return { isSuccess: false, message: "unknown error" };
    }
}

export async function togglePostPublishedStatus(postId: number): Promise<ResponseBase> {
    try {
        const response = await axios.put<ResponseBase>(`${BASE_URL}/posts/publish/${postId}`);
        return response.data;
    } catch (error) {
        return { isSuccess: false, message: "unknown error" };
    }
}