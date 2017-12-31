import datetime
from peewee import *

db = SqliteDatabase('test.db')


class Channel(Model):
    username = CharField(unique=True)

    class Meta:
        database = db


class Message(Model):
    channel = ForeignKeyField(Channel, related_name='channel')
    message = TextField()
    date = DateTimeField()
    media = TextField()

    class Meta:
        database = db

