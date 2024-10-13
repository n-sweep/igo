import os
import sys
import json

from src.baduk import OGSGame


def make_tapefile(game, size, sleep=0.25, messages=[]):
    path = f'/tmp/{game}.tape'
    output = f'./{game}.gif'

    fstr = 'Type "{}"\nSleep 750ms\nBackspace {}'
    insert_messages = '\n'.join([fstr.format(msg, len(msg)) for msg in messages])

    tape = f'''
    Output "{output}"

    Set Shell "bash"
    Set FontSize 32
    Set Width {size * 65}
    Set Height {size * 70 + 100}
    Set Theme Kanagawa
    Set Margin 20

    {insert_messages}
    Sleep 200ms

    Type "./play {game}"
    Sleep 500ms
    Enter
    Sleep {sleep}s
    '''

    with open(path, 'w') as f:
        f.write(tape)

    return path, output

def record_tape(game_id, speed):
    game = OGSGame(game_id)

    tape, gif = make_tapefile(
        game.id,
        game.board.size,
        int(speed * len(game.moves) * 2),
        ['welcome to OGS gif generator']
    )

    data = {
        'id': game.id,
        'size': game.board.size,
        'turns': [str(g) for g in game.turns],
        'tape_file': tape,
        'gif_file': gif,
        'speed': speed
    }

    with open(f'/tmp/{game.id}.json', 'w') as f:
        json.dump(data, f)

    os.system(f"vhs -q {tape}")

    return data


def main():
    game_id = sys.argv[1]
    data = record_tape(game_id, 0.1)

    print(json.dumps(data))


if __name__ == "__main__":
    main()
