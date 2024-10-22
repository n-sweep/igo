# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: hydrogen
#       format_version: '1.3'
#       jupytext_version: 1.16.4
#   kernelspec:
#     display_name: Python3
#     language: python
#     name: Python3
# ---

# %%
import numpy as np
from itertools import accumulate, product, combinations

# %% [markdown]
# # Template Notebook

# %%
ALPHA = 'abcdefghijklmnopqrstuvwxyz'
B = "⚫"
W = "⚪"
PT = "╶╴"
SP = "╺╸"

BLACK = '\033[30m'      # ]
GRAY = '\033[90m'       # ]
YELLOW = '\033[33m'     # ]
BG_YELLOW = '\033[43m'  # ]
RESET = '\033[0m'       # ]


class Board:
    def __init__(self, size: int = 19):
        self.size = size
        self.state = np.zeros((size,size), dtype=int)

    def play(self, player: int, x: int, y: int) -> None:
        self.state[y, x] = player

    def plaintext_board(self) -> str:
        star_points = np.zeros((self.size,self.size), dtype=int)
        s = 3 if self.size > 9 else 2
        corners = [j for i in range(3) if (j:=(s+(2*s*i))) < self.size]
        pts = [(f:=self.size//2, f)] + list(product(corners, repeat=2))
        star_points[*zip(*pts)] = -1

        board = self.state.copy()
        mask = ~self.state.astype(bool)
        board[mask] = star_points[mask]

        joined = ' '.join(list(ALPHA.replace('i', '')[:size])).upper()
        rows = [col_label:=f"{YELLOW}{(d:='-' * s)}{BLACK}{joined} {YELLOW}{d}"]

        for r, input_row in enumerate(board, 1):
            row = ''.join([(PT,B,W,SP)[i] for i in input_row])
            num = str(size - r + 1)
            lnum = num.rjust(int(len(str(size))))
            rnum = num.ljust(int(len(str(size))))
            rows.append(f'{BLACK}{lnum} {GRAY}{row} {BLACK}{rnum}')

        rows.append(col_label)
        rows = [f'{BG_YELLOW}{row}{RESET}' for row in rows]

        return '\n'.join(rows)

    def __str__(self):
        return self.plaintext_board()

for size in [9, 13, 19]:
    b = Board(size)
    b.play(1, 4, 4)
    b.play(2, 3, 2)
    print(b)

# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
# %%
