from fastapi import FastAPI
from api.users import users_router
from api.user_auths import user_auths_router
from api.friend import friend_router
from utils.db import initialize_db, close_db

app = FastAPI()

app.include_router(users_router, prefix="/users")
app.include_router(user_auths_router, prefix="/user_auths")
app.include_router(friend_router, prefix="/friends", tags=["friend"])


@app.on_event("startup")
async def startup_event():
    initialize_db()


@app.on_event("shutdown")
async def shutdown_event():
    close_db()
