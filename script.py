import argparse

from telegram import ApiHandler

from database.models import Message, export_sources

from settings import *


def main():
    print('Starting script...')
    parser = argparse.ArgumentParser()
    parser.add_argument("-full_history", action="append",
                        help="increase output verbosity")
    args = parser.parse_args()

    FULL_HISTORY = True if args.full_history else False
    print('Getting all messages - {}'.format(FULL_HISTORY))

    client = ApiHandler(API_ID, API_HASH)
    print('Auth - successfully!')

    sources = export_sources()
    print('Getting sourses...\nGot {} sources'.format(len(sources)))

    for source in sources:
        print('Getting {} messages...'.format(source.username))

        if FULL_HISTORY:
            messages = client.get_chat_messages(source.username, all=True)
        else:
            messages = client.get_chat_messages(source.username)

        print('Got {} messages.\nSaving {} messages...'.format(len(messages), source.username))

        for message in messages:
            try:
                Message.get_or_create(
                    source_id=source._get_pk_value(),
                    message_id=message['id'],
                    message=message['message'],
                    date=message['date'],
                    media='Yes' if message['media'] else 'No'
                )
            except KeyError:
                pass

    print('Done!')


if __name__ == '__main__':
    main()
