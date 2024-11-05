import os
import logging
from src.bot import Bot

os.makedirs('logs/', exist_ok=True)
handler = logging.FileHandler('logs/session.log', encoding='utf-8', mode='w')


def main():
    bot = Bot(os.environ['IGO_DISCORD'])
    bot.run(log_handler=handler, root_logger=True)


if __name__ == '__main__':
    main()
