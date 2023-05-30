from utils.db_instance import db
from passlib.context import CryptContext
from peewee import Model, CharField, DateField
import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Model):
    username = CharField(default="user")
    email = CharField(unique=True)
    password = CharField()
    birthdate = DateField(default=datetime.datetime.strptime('2000-01-01', '%Y-%m-%d'))
    gender = CharField(default="Gender")

    class Meta:
        database = db

    @classmethod
    def create_user(cls, email, password):
        hashed_password = pwd_context.hash(password)
        return cls.create(email=email, password=hashed_password)
