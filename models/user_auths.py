from peewee import *
from users import User
import datetime
from utils.db_instance import db


class UserAuth(Model):
    id = AutoField()
    user = ForeignKeyField(User, backref='auths')
    identity_type = CharField(max_length=255)
    identifier = CharField(max_length=255)
    credential = CharField(max_length=255)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
