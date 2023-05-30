from fastapi import APIRouter
from models.user_auths import UserAuth
from models.users import User
from utils.security import hash_password

user_auths_router = APIRouter()


@user_auths_router.post("/user_auths/")
async def create_user_auth(user_id: int, identity_type: str, identifier: str, credential: str):
    user = User.get(User.id == user_id)
    hashed_credential = hash_password(credential)
    user_auth = UserAuth.create(user=user, identity_type=identity_type, identifier=identifier,
                                credential=hashed_credential)
    return {"message": "User authorization created successfully."}
