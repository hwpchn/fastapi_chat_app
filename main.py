from fastapi import FastAPI
from api.accounts import accounts_router
from api.friend import friend_router
from utils.db import initialize_db, close_db

app = FastAPI()

app.include_router(accounts_router, prefix="/accounts")
app.include_router(friend_router, prefix="/friends", tags=["friend"])


@app.on_event("startup")
async def startup_event():
    initialize_db()


@app.on_event("shutdown")
async def shutdown_event():
    close_db()
