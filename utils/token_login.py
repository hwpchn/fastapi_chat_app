import jwt
from datetime import datetime, timedelta
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from models.user_auths import UserAuth
from bcrypt import checkpw

ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(identifier: str, credential: str) -> bool:
    user_auth = UserAuth.get(UserAuth.identifier == identifier)
    return checkpw(credential.encode(), user_auth.credential.encode())


def verify_token(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload

# ten_days = timedelta(days=10)
# token = create_access_token(data, expires_delta=ten_days)
