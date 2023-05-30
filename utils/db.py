from utils.db_instance import db
from models.accounts import User
from models.friend import FriendRequest, Friendship


def initialize_db():
    db.connect()
    db.create_tables([User, FriendRequest, Friendship])


def close_db():
    if not db.is_closed():
        db.close()
