import datetime
from peewee import *

db = SqliteDatabase('test.db')


class Channel(Model):
    username = CharField(unique=True)

    class Meta:
        database = db


class ChannelMessage(Model):
    channel = ForeignKeyField(Channel, related_name='channel')
    message_id = IntegerField()
    message = TextField()
    date = DateTimeField()
    media = TextField(null=True)

    class Meta:
        database = db


def export_channels():
    """
    Функция для экспорта списка каналов из базы данных
    :return: список каналов
    """
    db_channels = Channel.select()

    return db_channels


def export_chats():
    """
    Функция для экспорта списка чатов из базы наддных
    :return:
    """
    return True
