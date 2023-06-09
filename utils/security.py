from passlib.context import CryptContext
from models.accounts import User
from peewee import DoesNotExist

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def authenticate_user(email: str, password: str):
    try:
        user = User.get(User.email == email)
    except DoesNotExist:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user


import bcrypt


def hash_password(password: str) -> str:
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return password_hash.decode()
