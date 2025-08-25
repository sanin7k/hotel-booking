from sqlalchemy import Column, Integer, String, Boolean

from backend.app.database.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    display_name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_verified = Column(Boolean, default=False)
    role = Column(String, default='user')  # 'user' or 'admin'
