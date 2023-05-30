from peewee import *
import datetime
from utils.db_instance import db


class User(Model):
    id = AutoField()
    nickname = CharField(max_length=255, null=True)
    avatar = CharField(max_length=255, null=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    updated_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db
