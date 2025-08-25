# import secrets

# def generate_token(length: int = 32) -> str:
#     """Generate a secure random token."""
#     return secrets.token_urlsafe(length)

from datetime import datetime, timedelta, timezone
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

ALGORITHM = os.getenv("ALGORITHM", "HS256")
RESET_SECRET_KEY = os.getenv("RESET_SECRET_KEY")
RESET_TOKEN_EXPIRE_MINUTES = int(os.getenv("RESET_TOKEN_EXPIRE_MINUTES", 15))
EMAIL_SECRET_KEY = os.getenv("EMAIL_SECRET_KEY")
EMAIL_TOKEN_EXPIRE_MINUTES = int(os.getenv("EMAIL_TOKEN_EXPIRE_MINUTES", 60))

def generate_password_reset_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": email}
    return jwt.encode(to_encode, RESET_SECRET_KEY, algorithm=ALGORITHM)

def verify_password_reset_token(token: str) -> str:
    try:
        payload = jwt.decode(token, RESET_SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None
    
def generate_email_verification_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=EMAIL_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": email}
    return jwt.encode(to_encode, EMAIL_SECRET_KEY, algorithm=ALGORITHM)

def verify_email_verification_token(token: str) -> str:
    try:
        payload = jwt.decode(token, EMAIL_SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None