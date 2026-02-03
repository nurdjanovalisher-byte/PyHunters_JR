from datetime import datetime
from utils.logger import logger



def timestamp():
    current_date = datetime.now()
    return current_date.strftime('%d/%m/%Y %H:%M')


def print_message(message: str):
    print('\n┌' + '─' * (len(message) + 2) + '┐')
    print(f'│ {message} │')
    print('└' + '─' * (len(message) + 2) + '┘\n')


def on_start():
    msg = f'Bot started at {timestamp()}'
    logger.info(msg)


def on_shutdown():
    msg = f'Bot is down at {timestamp()}'
    print_message(msg)