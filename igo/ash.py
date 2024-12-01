from src.baduk import OGSGame


def main():

    game_url = "https://online-go.com/game/<id>"

    game = OGSGame(game_url)
    # game = OGSGame('<id>')

    path = 'path/to/save/gif.gif'
    print(game.create_gif(path=path))


if __name__ == '__main__':
    main()
