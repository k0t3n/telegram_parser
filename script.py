import sys
from getpass import getpass

import time

from settings import *

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.errors.rpc_error_list import UsernameNotOccupiedError, FloodWaitError
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.messages import GetHistoryRequest, GetFullChatRequest
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.types import InputPeerChannel, InputChannel


def get_chat_messages(channel_name, client, offset=0):
    """
    Функция для получения сообщений из чата. Максимально 100 сообщений за раз
    :param offset: смещение
    :param channel_name: имя канала (например durov)
    :param client: объект клиента
    :return: объект сообщений
    """
    chat_object = get_chat_info(channel_name, client)
    input_channel = InputChannel(chat_object['chat_id'], chat_object['access_hash'])
    channel = client.invoke(GetFullChannelRequest(input_channel)).__dict__
    chat_peer = InputPeerChannel(channel['full_chat'].id, chat_object['access_hash'])
    messages = client.invoke(GetHistoryRequest(chat_peer, 0, None, offset, LIMIT, 0, 0))

    return messages.messages


def get_chat_info(username, client):
    """
    Функция для получения информации о чате
    :param username: имя пользователя
    :param client: объект клиента
    :return:
    """
    try:
        chat = client(ResolveUsernameRequest(username))
    except UsernameNotOccupiedError:
        print('Chat/channel not found!')
        sys.exit()
    result = {
        'chat_id': chat.peer.channel_id,
        'access_hash': chat.chats[0].access_hash
    }
    return result


def auth(app_id, app_hash):
    """
    Функция для авторизации пользователя
    :param app_id: ID приложения
    :param app_hash: Hash приложения
    :return: объект клиента
    """
    client = TelegramClient('user-session', app_id, app_hash)
    client.connect()

    if not client.is_user_authorized():
        try:
            client.send_code_request(PHONE)
            print('Sending a code...')
            client.sign_in(PHONE, code=input('Enter code: '))
            print('Successfully!')
        except FloodWaitError as FloodError:
            print('Flood wait: {}.'.format(FloodError))
            sys.exit()
        except SessionPasswordNeededError:
            client.sign_in(password=getpass('Enter password: '))
            print('Successfully!')

    return client


def main():
    client = auth(API_ID, API_HASH)

    offset = 0
    messages = get_chat_messages(CHANNEL_NAME, client, offset)
    posts_count = len(messages)

    while len(messages) != 0:
        offset += 100
        messages = get_chat_messages(CHANNEL_NAME, client, offset)
        posts_count += len(messages)
        time.sleep(1)

    print(posts_count)

    # print(len(messages))
    # for message in messages:
    #     print(message.message)

    print('Done!')


if __name__ == '__main__':
    main()
