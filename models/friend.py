import datetime
from peewee import *
from models.accounts import User
from utils.db import db


class FriendRequest(db.Model):
    sender = ForeignKeyField(User, backref="sent_requests")
    receiver = ForeignKeyField(User, backref="received_requests")
    status = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)


class Friendship(db.Model):
    user1 = ForeignKeyField(User, backref="friendships1")
    user2 = ForeignKeyField(User, backref="friendships2")
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)
