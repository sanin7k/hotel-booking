from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.schemas.schemas import PasswordResetRequest, PasswordResetConfirm
from backend.app.auth.auth_password import hash_password
from backend.app.auth.auth_token_handler import generate_password_reset_token, verify_password_reset_token
from backend.app.utils.email import send_email
from backend.app.database.database import get_db
from backend.app.models.models import User

import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

@router.post("/forgot-password")
def forgot_password(request: PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    token = generate_password_reset_token(user.email)
    
    frontend_url = os.getenv('FRONTEND_URL')
    reset_link = f"{frontend_url}/reset-password?token={token}"

    send_email(
        to=user.email,
        subject="Reset your password",
        body=f"Click the link to reset your password: {reset_link}"
    )
    return {"message": "Password reset link sent to your email"}

@router.post("/reset-password")
def reset_password(request: PasswordResetConfirm, db: Session = Depends(get_db)):
    email = verify_password_reset_token(request.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    user.hashed_password = hash_password(request.new_password)
    db.commit()

    return {"message": "Password reset successfully"}
