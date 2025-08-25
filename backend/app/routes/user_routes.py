from fastapi import APIRouter, Depends

from backend.app.auth.jwt_token_handler import get_current_user
from backend.app.models.models import User
from backend.app.schemas.schemas import UserProfile

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/profile", response_model=UserProfile)
def get_user_profile(current_user: User = Depends(get_current_user)):
    return current_user
