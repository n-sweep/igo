import os
import imageio.v2 as iio
import requests
import numpy as np
from itertools import product
from src.util import draw_go_board, read_sgf

from typing import Generator

ALPHA = 'abcdefghijklmnopqrstuvwxyz'
B = "⚫"
W = "⚪"
PT = "╶╴"
SP = "🬇🬃"

# COLORS
BLACK = '\033[30m'      # ]
GRAY = '\033[90m'       # ]
YELLOW = '\033[33m'     # ]
BG_YELLOW = '\033[43m'  # ]
RESET = '\033[0m'       # ]


class Board:
    def __init__(self, meta: dict) -> None:
        self.move = 0
        self.meta = meta
        self.size = int(meta['SZ'])

        self.state = np.zeros((self.size, self.size), dtype=int)
        self._stones = self.state.copy()

    def get_stones(self, player: int|None = None) -> np.ndarray:
        if player is not None:
            return self._stones[self.state == player]
        return self._stones[self.state > 0]

    @property
    def stones(self) -> np.ndarray:
        return self.get_stones()

    def update_stones(self) -> None:
        stones = np.zeros(self.state.shape, dtype=object)
        for i, j in list(zip(*np.where(self.state > 0))):
            stones[i, j] = Stone(self, int(self.state[i, j]), np.array((i, j)))
        self._stones = stones

    def process_groups(self, player: int) -> None:

        def recursive_find_group(stone, group=None) -> set:
            group = set() if group is None else group
            if stone in group:
                return set()
            group.add(stone)
            for con in stone.connections:
                recursive_find_group(con, group)
            return group

        groups = []
        stones = set(self.get_stones(player))
        while stones:
            group = recursive_find_group(stones.pop())
            groups.append(group)
            stones = stones - group

            liberties = len(set.union(*[s.liberties for s in group]))
            if liberties == 0:
                remove = np.array([s.location for s in group])
                self.state[remove[:, 0], remove[:, 1]] = 0
                self._stones[remove[:, 0], remove[:, 1]] = 0

    def _play(self, player: int, loc: tuple) -> None:
        x, y = loc
        self.state[y][x] = player
        self.update_stones()
        for p in (3 - player, player):
            self.process_groups(p)
        self.move += 1

    def play(self, player: int|str, loc: str) -> None:
        if isinstance(player, str) and player in 'BW':
            player = 'BW'.index(player) + 1
        x = ALPHA.replace('i', '').index(loc[0].lower())
        y = 13 - int(loc[1:])

        self._play(int(player), (x, y))

    def __repr__(self) -> str:
        return str(self.state)

    def plaintext_board(self) -> str:
        star_points = np.zeros((self.size,self.size), dtype=int)
        corners = [j for i in range(3) if (j:=((s:=2+(self.size>9))+(2*s*i))) < self.size]
        pts = [(f:=self.size//2, f)] + list(product(corners, repeat=2))
        star_points[*zip(*pts)] = -1

        board = self.state.copy()
        mask = ~self.state.astype(bool)
        board[mask] = star_points[mask]

        joined = ' '.join(list(ALPHA.replace('i', '')[:self.size])).upper()
        rows = [col_label:=f"{YELLOW}{(d:='-' * s)}{BLACK}{joined} {YELLOW}{d}"]

        for r, input_row in enumerate(board, 1):
            row = ''.join([(PT,B,W,SP)[i] for i in input_row])
            num = str(self.size - r + 1)
            lnum = num.rjust(int(len(str(self.size))))
            rnum = num.ljust(int(len(str(self.size))))
            rows.append(f'{BLACK}{lnum} {GRAY}{row} {BLACK}{rnum}')

        rows.append(col_label)
        rows = [f'{BG_YELLOW}{row}{RESET}' for row in rows]

        return '\n'.join(rows)

    def __str__(self):
        return self.plaintext_board()




class Stone:
    def __init__(self, board: Board, color: int, location: np.ndarray) -> None:
        self.board = board
        self.color = color  # 1 is black, 2 is white
        self.location = location

    @property
    def neighbors(self) -> tuple:
        neighbor_locs = np.array(((0, 1), (1, 0), (0, -1), (-1, 0))) + self.location
        oob = (neighbor_locs >= 0) & (neighbor_locs < self.board.size)
        neighbor_locs = neighbor_locs[oob.all(axis=1)]
        neighbor_vals = self.board.state[neighbor_locs[:, 0], neighbor_locs[:, 1]]

        return neighbor_locs, neighbor_vals

    @property
    def connections(self) -> list:
        locs, vals = self.neighbors
        conns = locs[vals == self.color]
        return list(self.board._stones[conns[:, 0], conns[:, 1]])

    @property
    def liberties(self) -> set:
        locs, vals = self.neighbors
        return set(map(tuple, locs[vals < 1]))

    def __str__(self):
        return f'{(B, W)[self.color-1]} {self.location}'

    def __repr__(self):
        return f'Stone(Board, {self.color}, {self.location})'


class OGSGame:
    BASE_URL = "https://online-go.com/api/v1/games/"

    def __init__(self, game_url: str) -> None:
        self.id = game_url.strip("https://online-go.com/game/")
        self.url = self.BASE_URL + self.id
        self.meta, self.moves = read_sgf(self.sgf)
        self.board = Board(self.meta)

        self.p1_username = self.meta['PB']
        self.p2_username = self.meta['PW']

    @property
    def data(self) -> dict:
        return requests.get(self.url).json()

    @property
    def sgf(self) -> str:
        text = requests.get(self.url + '/sgf').text
        if text == 'Permission denied':
            raise ValueError('Cannot access private game')

        return text

    @property
    def turns(self) -> Generator:
        yield self.board
        for player, move in self.moves:
            player = 'BW'.index(player) + 1

            if move:
                x, y = (ALPHA.index(c) for c in move)
                self.board._play(player, (x, y))

            yield self.board

    def snapshot(self, path: str = '/tmp/ogs', overwrite: bool = True) -> str:
        board = list(self.turns)[0]
        img_loc = draw_go_board(board, self.id, path, overwrite)

        return img_loc

    def create_gif(self, dur: float = 0.25, path: str = '/tmp/ogs', overwrite: bool = False) -> str:
        for board in self.turns:
            draw_go_board(board, self.id, path, overwrite)
        frame_path = f'{path}/{self.id}'
        out_path = f'{path}/{self.id}.gif'
        files = sorted([f"{frame_path}/{f}" for f in os.listdir(frame_path)])
        files = [files[0]] * 3 + files + [files[-1]] * 9
        frames = [iio.imread(f) for f in files]
        iio.mimsave(out_path, frames, fps=1/dur, loop=0)  # pyright: ignore

        return out_path
