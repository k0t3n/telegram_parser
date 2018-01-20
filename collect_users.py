from telegram import ApiHandler

from database.models import Message, User

from settings import *


def main():
    print('Starting script...')

    client = ApiHandler(API_ID, API_HASH)
    print('Auth - successfully!')

    messages = Message.select()
    print('Getting messages...\nGot {} messages'.format(len(messages)))

    user_ids = []

    for message in messages:
        if message.from_id and message.from_id not in user_ids:
            try:
                user_ids.append(message.from_id)
            except Exception:
                pass

    print('Got {} unique users'.format(len(user_ids)))

    users = client.get_users(user_ids)

    for user in users:
        User.get_or_create(
            user_id=user['id'],
            username=user['username'],
            first_name=user['first_name'],
            last_name=user['last_name']
        )

    print('Done!')


if __name__ == '__main__':
    main()
