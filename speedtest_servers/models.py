from secrets import token_hex
from uuid import uuid4
from peewee import Model
from peewee import MySQLDatabase
from peewee import IntegerField
from peewee import CharField
from peewee import DateTimeField
from peewee import UUIDField
from peewee import SQL

database = MySQLDatabase(None)


class BaseModel(Model):
    class Meta:
        database = database


class Users(BaseModel):
    username = CharField()
    access_key = CharField(default=token_hex(32))


class Settings(BaseModel):
    is_initialized = IntegerField(default=False)
    is_updating = IntegerField(default=False)
    created_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    updated_at = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])


class Servers(BaseModel):
    id = UUIDField(primary_key=True, default=uuid4)
    server_id = IntegerField()
    city = CharField()
    country = CharField()
    provider = CharField()
