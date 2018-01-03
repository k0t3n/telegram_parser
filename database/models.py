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


def export_sources():
    """
    Функция для экспорта списка каналов из базы данных
    :return: список каналов
    """
    db_channels = Source.select()

    return db_channels
