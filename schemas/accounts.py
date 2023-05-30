from pydantic import BaseModel, EmailStr
import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str = "user"
    birthdate: datetime.date = datetime.date(2000, 1, 1)
    gender: str = "Gender"

class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True