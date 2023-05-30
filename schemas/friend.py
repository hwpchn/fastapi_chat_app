from pydantic import BaseModel, EmailStr
import datetime


class FriendRequestInput(BaseModel):
    sender_email: str
    receiver_email: str
    created_at: datetime = datetime.datetime.now()
    updated_at: datetime = datetime.datetime.now()


class AcceptRejectRequestInput(BaseModel):
    request_id: int


class GetUserFriendsInput(BaseModel):
    user_email: str


class DeleteFriendInput(BaseModel):
    user_email: str
    friend_email: str
