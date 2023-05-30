from fastapi import APIRouter, Depends, HTTPException
from models.friend import FriendRequest, Friendship
from models.accounts import User
from schemas.friend import FriendRequestInput, AcceptRejectRequestInput, GetUserFriendsInput, DeleteFriendInput
from utils.token_login import verify_token
from config import FRIEND_REQUEST_EXPIRY_DAYS
from datetime import datetime, timedelta

friend_router = APIRouter()


@friend_router.post("/send_request")
async def send_friend_request(friend_request: FriendRequestInput, token: str = Depends(verify_token)):
    sender = User.get(User.email == friend_request.sender_email)
    receiver = User.get(User.email == friend_request.receiver_email)

    if not sender or not receiver:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if a request sent within the last FRIEND_REQUEST_EXPIRY_DAYS days already exists
    expiry_date = datetime.now() - timedelta(days=FRIEND_REQUEST_EXPIRY_DAYS)
    existing_request = FriendRequest.select().where(
        (FriendRequest.sender == sender) & (FriendRequest.receiver == receiver) & (
                FriendRequest.created_at > expiry_date))
    if existing_request.exists():
        raise HTTPException(status_code=400, detail="A recent request already exists")

    request = FriendRequest.create(sender=sender, receiver=receiver, status="pending")
    return {
        "request_id": request.id,
        "status": "success",
        "sender_email": sender.email,
        "receiver_email": receiver.email,
        "created_at": request.created_at,
        "updated_at": request.updated_at
    }


@friend_router.post("/accept_request")
async def accept_friend_request(accept_request: AcceptRejectRequestInput, token: str = Depends(verify_token)):
    request = FriendRequest.get_or_none(FriendRequest.id == accept_request.request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    if request.status != "pending":
        raise HTTPException(status_code=400, detail="Invalid request status")

    friendship = Friendship.create(user1=request.sender, user2=request.receiver)
    request.status = "accepted"
    request.save()
    return {"status": "success", "user1_email": friendship.user1.email, "user2_email": friendship.user2.email}


@friend_router.post("/reject_request")
async def reject_friend_request(reject_request: AcceptRejectRequestInput, token: str = Depends(verify_token)):
    request = FriendRequest.get(FriendRequest.id == reject_request.request_id)

    if not request:
        raise HTTPException(status_code=404, detail="Request not found")

    if request.status != "pending":
        raise HTTPException(status_code=400, detail="Invalid request status")

    request.status = "rejected"
    request.save()
    return {"status": "success", "request_id": request.id, "sender_email": request.sender.email,
            "receiver_email": request.receiver.email}


@friend_router.get("/list/{user_email}")
async def get_friends_list(get_friends: GetUserFriendsInput, token: str = Depends(verify_token)):
    user = User.get(User.email == get_friends.user_email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    friends = []
    for friendship in user.friendships1:
        friends.append({"email": friendship.user2.email, "username": friendship.user2.username})
    for friendship in user.friendships2:
        friends.append({"email": friendship.user1.email, "username": friendship.user1.username})

    return {"friends": friends}


@friend_router.delete("/delete/{user_email}/{friend_email}")
async def delete_friend(delete_friend_input: DeleteFriendInput, token: str = Depends(verify_token)):
    user = User.get(User.email == delete_friend_input.user_email)
    friend = User.get(User.email == delete_friend_input.friend_email)

    if not user or not friend:
        raise HTTPException(status_code=404, detail="User not found")

    friendship = Friendship.get(((Friendship.user1 == user) & (Friendship.user2 == friend)) | (
            (Friendship.user1 == friend) & (Friendship.user2 == user)))

    if not friendship:
        raise HTTPException(status_code=404, detail="Friendship not found")

    friendship.delete_instance()
    return {"status": "success",
            "deleted_friendship": {"user1_email": friendship.user1.email, "user2_email": friendship.user2.email}}
