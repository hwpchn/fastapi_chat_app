from pydantic import BaseModel, EmailStr


class FriendRequestInput(BaseModel):
    sender_email: str
    receiver_email: str


class AcceptRejectRequestInput(BaseModel):
    request_id: int


class GetUserFriendsInput(BaseModel):
    user_email: str


class DeleteFriendInput(BaseModel):
    user_email: str
    friend_email: str
