from fastapi import APIRouter, Request, Depends
from auth import verify_token

router = APIRouter()

@router.get("/user/data")
async def get_user_data(request: Request, user=Depends(verify_token)):
    user_id = request.state.user_id
    return {"user_id": user_id, "message": f"Data for user {user_id}"}
