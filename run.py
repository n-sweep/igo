import json
from src.bot import Bot
from src.baduk import OGSGame
from src.util import sgf_data


def test():

    game = OGSGame('68441458')
    print(game.snapshot())

    sgf_meta = sgf_data()
    print(json.dumps(game.data))

    for code, val in game.meta.items():
        print(code, sgf_meta[code]['description'], val)


def main():
    # test()
    # return

    bot = Bot('/home/n/.config/discord/bots/gobot/token')
    bot.run()


if __name__ == '__main__':
    main()
