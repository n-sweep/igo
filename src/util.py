from __future__ import annotations

from bs4 import BeautifulSoup as bs
from itertools import accumulate, permutations
import imageio
import numpy as np
import os
import plotly.graph_objects as go
import re
import requests

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.baduk import Board, OGSGame

B = "⚫"
W = "⚪"


def get_star_points(size: int) -> np.ndarray:
    board = np.zeros((size, size))
    s = 3 if size > 9 else 2
    star_points = [j for i in range(3) if (j:=(s+(2*s*i))) < size]

    for p in star_points:
        board[p][p] = -1
    for x, y in permutations(star_points, 2):
        board[x][y] = -1

    return board


def sgf_data() -> dict:
    r = requests.get('https://www.red-bean.com/sgf/proplist_ff.html')
    soup = bs(r.content, 'html.parser')
    lines = soup.find('pre').text.strip().split('\n')  # pyright: ignore
    field_lengths = [len(d) for d in lines.pop(1).split(' ') if d]

    coords = list(zip(
        accumulate(field_lengths, lambda a, v: a + v + 2, initial=0),
        field_lengths
    ))

    processed_lines = list(map(lambda ln: [ln[x:x+l].strip() for x, l in coords], lines))
    keys = [field.lower().replace(' ', '_') for field in processed_lines.pop(0)]

    return {ln[0]: dict(zip(keys[1:], ln[1:])) for ln in processed_lines}


def read_sgf(sgf: str) -> tuple:
    text = sgf.strip(')').split(';')
    meta = dict(re.findall(r'(\w+)\[(.*?)\]\n?', text[1]))
    moves = [tuple(m.strip('\n()]').split('[')) for m in text[2:]]

    return meta, moves


def draw_go_board(board: Board, game_id: str|int, path: str = '/tmp/ogs', overwrite: bool = False) -> str:

    dir = f"{path}/{game_id}"
    if not os.path.isdir(dir):
        os.makedirs(dir, exist_ok=True)

    path = f"{dir}/{board.move:03}.png"

    if not overwrite and os.path.isfile(path):
        return path

    fig_size = 800
    zi_size = board.size - 1
    margin_ext = 1.5
    stone_size = {19: 35, 13: 48, 9: 66}[board.size]
    text_size = {19: 24, 13: 30, 9: 46}[board.size]

    fig = go.Figure()

    fig.update_layout(
        width=fig_size,
        height=fig_size,
        plot_bgcolor='#DCB35C',
        xaxis=dict(
            zeroline=False,
            range=[-margin_ext, zi_size + margin_ext],
            scaleanchor='y',
            showgrid=False,
            showticklabels=False
        ),
        yaxis=dict(
            zeroline=False,
            range=[-margin_ext, zi_size + margin_ext],
            showgrid=False,
            showticklabels=False
        ),
        showlegend=False,
        margin={x: 0 for x in 'lrtb'}
    )

    # draw lines
    for i in range(board.size):
        for x, y in (lines:=([i, i], [0, zi_size]), lines[::-1]):
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='black', width=1)))

    # draw star points
    for x, y in list(zip(*np.where(get_star_points(board.size) < 0))):
        fig.add_trace(go.Scatter(x=[x], y=[y], mode='markers', marker=dict(color='black', size=10)))

    # draw text
    for i in range(board.size):
        c = chr(65 + i)
        s = str(i + 1)
        args = [
            (-1, i, s),
            (i, -1, c),
            (board.size, i, s),
            (i, board.size, c)
        ]
        for x, y, text in args:
            fig.add_annotation(
                x=x, y=y,
                text=text,
                showarrow=False,
                font=dict(
                    color='#424242',
                    family='Roboto Black',
                    size=text_size,
                    weight='bold'
                )
            )

    # draw stones
    for stone in board.stones:
        y, x = stone.location
        emoji = [B, W][stone.color - 1]
        fig.add_annotation(x=x, y=zi_size - y, text=emoji, showarrow=False, font=dict(size=stone_size))

    fig.write_image(path, scale=2)

    return path


def create_gif(game: OGSGame):
    for board in game.turns:
        draw_go_board(board, game.id)

    path = f'/tmp/ogs/{game.id}'
    files = sorted([f"{path}/{f}" for f in os.listdir(path)])
    frames = [imageio.imread(f) for f in files]
    imageio.mimsave("another_test.gif", frames, fps=1/0.25, loop=0)  # pyright: ignore
