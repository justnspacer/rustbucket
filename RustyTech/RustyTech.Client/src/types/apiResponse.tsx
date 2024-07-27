export interface RegisterRequest {
    email: string;
    password: string;
    confirmPassword: string;
    birthYear: number;
}

export interface LoginRequest {
    email: string;
    password: string;
}

export interface User {
    id: string;
    email: string;
}

export interface ResponseBase {
    isSuccess: boolean;
    message: string;
}

export interface RoleDto {
    id: string;
    roleName: string;
}

export interface UserUpdateDto {
    userId: string;
    email?: string;
    userName?: string;
    birthYear: number;
}

export interface UserDto {
    id: string;
    email: string;
    userName: string;
    verifiedAt: Date;
}

export interface PostDto {
    id: number;
    title: string;
    content: string;
    plainTextContent: string;
    keywords: string[];
    postType: string;
    userId: string;
    user: UserDto;
}

export interface BlogDto extends PostDto {
    imageUrls: File[];
}

export interface VideoDto extends PostDto {
    videoUrl: File;
}

export interface ImageDto extends PostDto {
    imageUrl: File;
}

export interface ApiData<T> {
    data: T;
}

export type Data = RoleDto | VideoDto | ImageDto | BlogDto | UserUpdateDto | UserDto | PostDto | PostDto[] | ResponseBase | null;

export interface ApiResponse extends ApiData<Data> { }