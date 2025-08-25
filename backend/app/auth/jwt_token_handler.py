from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.app.schemas.schemas import TokenData
from backend.app.database.database import get_db
from backend.app.models.models import User

import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    payload = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    payload.update({"exp": int(expire.timestamp())})
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    payload = data.copy()
    payload.update({"exp": expire})
    return jwt.encode(payload, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str, secret_key: str = SECRET_KEY):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return TokenData(sub=email)
    except JWTError as e:
        raise credentials_exception
    
# def get_current_user(token: str = Depends(oauth2_scheme)):
def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")
    print(token)
    if not token:
        print("token missing")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    payload = verify_token(token)
    user = db.query(User).filter(User.email == payload.sub).first()
    if user is None:
        print("user not found")
        raise credentials_exception
    return user
