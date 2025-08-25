from fastapi import Depends, HTTPException, status

from backend.app.auth.jwt_token_handler import get_current_user
from backend.app.models.models import User

def require_role(required_role: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"User does not have the required role: {required_role}"
            )
        return current_user
    return role_checker