from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    confirm_password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfile(UserBase):
    id: int
    display_name: str
    is_verified: bool
    role: str = "user"  # Default role is 'user'

    class Config:
        from_attributes = True

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
    confirm_password: str

#JWT Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: str | None = None