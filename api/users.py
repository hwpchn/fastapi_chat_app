from fastapi import APIRouter
from models.users import User

users_router = APIRouter()

@users_router.post("/users/")
async def create_user(user: User):
    user.save()
    return {"message": "User created successfully."}
