from fastapi import APIRouter, HTTPException
from models.accounts import User
from schemas.accounts import UserCreate, User as UserSchema
from utils.security import authenticate_user
from utils.token_login import create_access_token
from utils.db import db
from datetime import timedelta

accounts_router = APIRouter()


@accounts_router.post("/register", response_model=UserSchema)
async def register(user: UserCreate):
    """
    用户注册接口
    """
    with db.atomic():
        new_user = User.create_user(email=user.email, password=user.password)
    return new_user


@accounts_router.post("/login", response_model=str)
async def login(user: UserCreate):
    """
    用户登录接口
    """
    authenticated_user = authenticate_user(user.email, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    ten_days = timedelta(days=10)
    access_token = create_access_token(data={"sub": authenticated_user.email}, expires_delta=ten_days)
    return access_token
