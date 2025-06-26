from fastapi import APIRouter, Request, Depends, HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from auth import retrieve_user

router = APIRouter()

@router.get("/user")
async def get_user(user_response=Depends(retrieve_user)):
    if not user_response or not hasattr(user_response, 'user') or not user_response.user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, 
            detail="No authenticated user found"
        )
    
    user = user_response.user
    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "created_at": user.created_at,
        }, 
        "message": f"Profile data for user {user.id}"
    }