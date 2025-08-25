from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.models import User
from backend.app.schemas.schemas import UserCreate, UserLogin, Token
from backend.app.auth.auth_password import hash_password, verify_password
from backend.app.auth.jwt_token_handler import create_access_token, create_refresh_token, verify_token
from backend.app.utils.email import send_email
from backend.app.auth.auth_token_handler import generate_email_verification_token, verify_email_verification_token

import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

@router.post("/auth/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        display_name=user.username,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()

    token = generate_email_verification_token(new_user.email)

    frontend_url = os.getenv('FRONTEND_URL')
    link = f"{frontend_url}/verify-email?token={token}"
    
    send_email(
        to=user.email,
        subject="Verify your email",
        body=f"Click the link to verify your email: {link}"
    )

    return {"message": "User registered successfully. Please check your email to verify your account."}

@router.get("/auth/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    email = verify_email_verification_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_verified = True
    db.commit()
    return {"message": "Email verified successfully. You can now log in."}

@router.post("/auth/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")

    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}
    )
    refresh_token = create_refresh_token(data={"sub": user.email})

    response = JSONResponse(content={"message": "Login successful"})
    response.set_cookie(
        key="access_token",
        value=access_token,
        # httponly=True,
        # secure=True,
        # samesite="lax",
        # max_age=60 * 60 * 24,
    )
    response.set_cookie(
        key="refresh_token", 
        value=refresh_token, 
        # httponly=True, 
        # max_age=7*24*60*60, 
        # samesite="none", 
        # secure=False
    )

    return response

@router.get("/logout")
def logout():
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response

@router.get("/logged_in")
def check_if_logged_in(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return {"logged_in": False}
    
    return {"logged_in": True}

@router.get("/auth/refresh")
def refresh_token(request: Request):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    try:
        payload = verify_token(token)
        email = payload.sub

        new_access_token = create_access_token(data={"sub": email})
        response = JSONResponse(content={"access_token": new_access_token})
        response.set_cookie("access_token", new_access_token, httponly=True, max_age=15*60, samesite="none", secure=False)
        return response
    
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
