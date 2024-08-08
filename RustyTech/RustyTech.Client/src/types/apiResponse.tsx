export interface RegisterRequest {
    type: "RegisterRequest";
    email: string;
    password: string;
    confirmPassword: string;
    birthYear: number;
}

export interface LoginRequest {
    type: "LoginRequest";
    email: string;
    password: string;
}

export interface ResponseBase
{
    type: "ResponseBase";
    statusCode: number;
    isSuccess: boolean;
    message: string;
}

export interface RoleDto {
    type: "RoleRequest";
    id: string;
    roleName: string;
}

export interface UserUpdateDto {
    type: "UserUpdateRequest";
    userId: string;
    email?: string;
    userName?: string;
    birthYear: number;
}

export interface UserDto {
    type: "GetUserRequest";
    id: string;
    email: string;
    userName: string;
    verifiedAt: Date;
}

export interface PostDto {
    type: "GetPostRequest";
    id: number;
    title: string;
    content: string;
    plainTextContent: string;
    keywords: string[];
    postType: string;
    userId: string;
    user: UserDto;
    createdAt: Date;
    updatedAt: Date;
    isPublished: boolean;
    imageFile?: string;
    videoFile?: string;
    imageFiles?: string[];
}

export interface ApiData<T> {
    data: T;
}

export type Data = RoleDto | UserUpdateDto | UserDto | PostDto | PostDto[] | ResponseBase | null;

export interface ApiResponse extends ApiData<Data> { }