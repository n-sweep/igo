import os
import logging
from src.bot import Bot

# handler = logging.FileHandler('logs/session.log', encoding='utf-8', mode='w')


def main():
    # d = os.path.dirname(os.path.realpath(__file__))
    # bot = Bot(os.path.join(d, '/home/n/.config/discord/bots/gobot/token'))
    # bot.run(log_handler=handler, root_logger=True)

    bot = Bot(os.environ['IGO_DISCORD'])
    bot.run()

if __name__ == '__main__':
    main()
