import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.models import User
from backend.app.auth.google_auth import oauth
from backend.app.auth.jwt_token_handler import create_access_token, create_refresh_token
from backend.app.utils.username_gen import get_unique_internal_username

load_dotenv()

router = APIRouter()

@router.get("/login/google")
async def login_with_google(request: Request):
    print("Logging in with Google")
    api_url = os.getenv("API_URL")
    redirect_uri = f"{api_url}/auth/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri=redirect_uri)

@router.get("/auth/callback")
async def google_auth_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        print("OAuth token:", token)
    except Exception as e:
        print("OAuth failed:", repr(e))

    user_info = token.get('userinfo')
    print("User info:", user_info)

    name = user_info.get("name")
    email = user_info.get("email")
    username = await get_unique_internal_username(db)

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            username=username,
            email=email,
            display_name=name,
            hashed_password="aouth2-google",  # Placeholder, as password is not used for OAuth users
            is_verified=True  # Automatically verified for OAuth users
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    jwt_token = create_access_token(data={"sub": user.email, "role": user.role})
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    response = RedirectResponse(url=os.getenv("FRONTEND_URL") + "/dashboard")
    response.set_cookie(
        key="access_token",
        value=jwt_token,
        # httponly=True,
        # max_age=60 * 60 * 24,  # 1 day
        # expires=60 * 60 * 24,
        # secure=False,  # True over HTTPS
        # samesite="none"  # or "none" if you're using cross-origin domains with credentials
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
