"""
This module generate an JWT for API Authentication
"""
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os

APP_ENV = os.getenv("APP_ENV", "dev")

if APP_ENV == "prod":
    SECRET_KEY = os.getenv("SECRET_KEY")
else:
    SECRET_KEY = "ExampleSecretKey"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "admin": {
        "username": "admin",
        "password": "admin123"
    }
}

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def authenticate_user(username: str, password: str):
    user = fake_users_db.get(username)
    if not user:
        return False
    if user["password"] != password:
        return False
    return True