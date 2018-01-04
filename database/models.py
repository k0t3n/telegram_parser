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

    class Meta:
        database = db


class Message(Model):
    source = ForeignKeyField(Source, related_name='channel')
    message_id = IntegerField()
    message = TextField()
    date = DateTimeField()
    media = TextField()

    class Meta:
        database = db


def export_sources(need_history=False):
    """
    Функция для экспорта списка каналов из базы данных
    :return: список каналов
    """
    if need_history:
        db_channels = Source.select().where(need_history=True)
    else:
        db_channels = Source.select()

    return db_channels
