import sys
from getpass import getpass
from settings import *

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.errors.rpc_error_list import UsernameNotOccupiedError, FloodWaitError
from telethon.tl.functions.contacts import ResolveUsernameRequest


def get_chat_info(username, client):
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


def main():
    client = TelegramClient('user-session', API_ID, API_HASH)
    print('Connecting...')
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
    print(get_chat_info(CHANNEL, client))
    print('Done!')


if __name__ == '__main__':
    main()
