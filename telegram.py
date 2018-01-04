# -*- coding: utf-8 -*-

import sys
from getpass import getpass

import time

from settings import *

from database.models import Message, export_sources

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.errors.rpc_error_list import UsernameNotOccupiedError, FloodWaitError
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import InputPeerChannel, InputChannel


class ApiHandler:
    """
    Класс для работы с Telegram Api
    """

    def __init__(self, app_id, app_hash):
        self.app_id = app_id
        self.app_hash = app_hash

        self.client = TelegramClient('user-session', app_id, app_hash)
        self.client.connect()

        if not self.client.is_user_authorized():
            try:
                self.client.send_code_request(PHONE)
                print('Sending a code...')
                self.client.sign_in(PHONE, code=input('Enter code: '))
            except FloodWaitError as FloodError:
                print('Flood wait: {}.'.format(FloodError))
                sys.exit()
            except SessionPasswordNeededError:
                self.client.sign_in(password=getpass('Enter password: '))

    def get_chat_messages(self, channel_name, all=False):
        """
        Функция для получения всех сообщений из чата.
        :param channel_name: имя чата (например durov)
        :param all: количество сообщений. Если False - получает последние 5к сообщений
        :return: объекты сообщений
        """
        chat_object = self.get_chat_info(channel_name)
        input_channel = InputChannel(chat_object['chat_id'], chat_object['access_hash'])
        channel = self.client.invoke(GetFullChannelRequest(input_channel)).__dict__
        chat_peer = InputPeerChannel(channel['full_chat'].id, chat_object['access_hash'])

        all_messages = []
        offset = 0
        new_messages = self.client.invoke(GetHistoryRequest(chat_peer, 0, None, offset, 0, 0, 0)).messages

        if all:
            while len(new_messages) is not 0 and offset < 5000:
                offset += 100

                for new_message in new_messages:
                    all_messages.append(new_message.__dict__)

                new_messages = self.client.invoke(GetHistoryRequest(chat_peer, 0, None, offset, 0, 0, 0)).messages
                time.sleep(1)

        else:
            while len(new_messages) is not 0:
                offset += 100

                for new_message in new_messages:
                    all_messages.append(new_message.__dict__)

                new_messages = self.client.invoke(GetHistoryRequest(chat_peer, 0, None, offset, 0, 0, 0)).messages

        return all_messages

    def get_chat_info(self, username):
        """
        Функция для получения информации о чате
        :param username: имя пользователя
        :return: словарь c chat_id и access_hash
        """
        try:
            chat = self.client(ResolveUsernameRequest(username))
        except UsernameNotOccupiedError:
            print('Chat/channel not found!')
            sys.exit()
        result = {
            'chat_id': chat.peer.channel_id,
            'access_hash': chat.chats[0].access_hash
        }
        return result
