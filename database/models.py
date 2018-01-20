# -*- coding: utf-8 -*-

import datetime
from peewee import *
from settings import *

db = MySQLDatabase(
    DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    charset=DB_CHARSET,
)


class Source(Model):
    username = CharField(unique=True)
    need_history = BooleanField(default=False)
    last_updated = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = db


class Message(Model):
    source = ForeignKeyField(Source, related_name='channel')
    message_id = IntegerField()
    message = TextField()
    date = DateTimeField()
    media = TextField()
    from_id = IntegerField()

    class Meta:
        database = db


class User(Model):
    user_id = IntegerField()
    username = CharField(null=True)
    first_name = CharField()
    last_name = CharField(null=True)

    class Meta:
        database = db


def export_sources(need_history=False):
    """
    Функция для экспорта списка каналов из базы данных
    :return: список каналов
    """
    if need_history:
        db_channels = Source.filter(need_history=True)
    else:
        db_channels = (Source
            .select()
            .order_by(-Source.last_updated)
            .filter(need_history=False)
            )
        for channel in db_channels:
            channel.last_updated = DateTimeField(datetime.datetime.now())
            channel.save()

    return db_channels
