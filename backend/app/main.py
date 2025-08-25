from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

import os
from dotenv import load_dotenv

from backend.app.database.database import Base, engine
from backend.app.routes import (
    auth_routes, 
    user_routes, 
    admin_routes, 
    password_reset, 
    oauth_routes
)

load_dotenv()

app = FastAPI()

origins = [os.getenv("FRONTEND_URL"),]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY")
)

Base.metadata.create_all(bind=engine)

app.include_router(auth_routes.router)
app.include_router(password_reset.router)
app.include_router(user_routes.router)
app.include_router(admin_routes.router)
app.include_router(oauth_routes.router)
