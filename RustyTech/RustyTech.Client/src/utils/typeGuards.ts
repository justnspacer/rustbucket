import { Data, RoleDto, UserUpdateDto, UserDto, PostDto, ResponseBase } from '../types/apiResponse'; // Adjust the import path as needed


export function isRoleDto(data: Data): data is RoleDto {
    return (data as RoleDto).type === "RoleRequest";
}

export function isUserUpdateDto(data: Data): data is UserUpdateDto {
    return (data as UserUpdateDto).type === "UserUpdateRequest";
}

export function isUserDto(data: Data): data is UserDto {
    return (data as UserDto).type === "GetUserRequest";
}

export function isPostDto(data: Data): data is PostDto {
    return (data as PostDto).type === "GetPostRequest";
}

export function isPostDtoArray(data: Data): data is PostDto[] {
    return Array.isArray(data) && data.every(item => (item as PostDto).type === "GetPostRequest");
}

export function isResponseBase(data: Data): data is ResponseBase {
    return (data as ResponseBase).type === "ResponseBase";
}