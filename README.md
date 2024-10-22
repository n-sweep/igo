# Igo

## Go, not golang

No, I haven't written a python > golang transpiler. A few months ago I started playing [Go](https://en.wikipedia.org/wiki/Go_(game)) and became a fast fan of the game. I and a few friends I roped into learning with me have been playing on [online-go.com (OGS)](https://online-go.com) both via their website and a third party Android app called [Sente](https://play.google.com/store/apps/details?id=io.zenandroid.onlinego&hl=en_US). As with every new website I find remotely useful, I had to check if they have an [API](https://en.wikipedia.org/wiki/Web_API). Spoiler: they do.

My goal is to make a program that, given the link to or ID of a game on OGS, will produce an animated gif of the game. Comfortable in my knowledge that OGS has an API and [charmbracelet/vhs](https://github.com/charmbracelet/vhs) exists, I chose to start with the game engine. This could be categorized as a mistake.


## Game Engine

### Representing the Board

As I intend to use [charmbracelet/vhs](https://github.com/charmbracelet/vhs) to generate the gif, my first concern was whether I can represent a Go board in a nice way in the terminal. The game pieces in Go are black and white stones and I already know I want to use emoji (⚫⚪) to represent them. There are plenty of [Unicode characters](https://symbl.cc/en/unicode/blocks/box-drawing/) for drawing boxes and grids, but the trouble is that emoji are two characters wide in monospace fonts. With this limitation, a grid of lines was impossible, but I eventually came up with the following ASCII board:

```
   A B C D E F G H J K L M N O P Q R S T    
19 ╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴ 19
18 ╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴ 18
17 ╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴ 17
16 ╶╴╶╴╶╴╺╸╶╴╶╴╶╴╶╴╶╴╺╸╶╴╶╴╶╴╶╴╶╴╺╸╶╴╶╴╶╴ 16
15 ╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴ 15
14 ╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴ 14
13 ╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴ 13
12 ╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴ 12
11 ╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴ 11
10 ╶╴╶╴╶╴╺╸╶╴╶╴╶╴╶╴╶╴╺╸╶╴╶╴╶╴╶╴╶╴╺╸╶╴╶╴╶╴ 10
 9 ╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴ 9
 8 ╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴ 8
 7 ╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴ 7
 6 ╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴ 6
 5 ╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴ 5
 4 ╶╴╶╴╶╴╺╸╶╴╶╴╶╴╶╴╶╴╺╸╶╴╶╴╶╴╶╴╶╴╺╸╶╴╶╴╶╴ 4
 3 ╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴ 3
 2 ╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴ 2
 1 ╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴ 1
   A B C D E F G H J K L M N O P Q R S T    
```


Note: This board mimics the default board display on OGS; they omit the letter I from the legend, presumably for it's similarity to 1? Seems unnecessary because 1 and I are on different axes, but perhaps there is a greater reason for this.

Considering that the board is simply a 2d array, `numpy` is the perfect choice for representing the game's state. Zeros are empty spaces, ones will be black stones, and twos will be white stones. Let's start with some constants and a board.

```py
import numpy as np

# let's start with a 9x9 board for the sake of brevity
size = 9
state = np.zeros((size,size), dtype=int)
state[4, 4] = 1
state[2, 3] = 2
print(state)
```

Great, but this can probably look nicer.

```py
array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 2, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0, 0]])
```

```py
B = "⚫"
W = "⚪"
PT = "╶╴"

for row in state:
    print(''.join([(PT,B,W)[i] for i in row]))
```

Also great, but it just doesn't look right without the star points...

```
╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴
╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴
╶╴╶╴╶╴⚪╶╴╶╴╶╴╶╴╶╴
╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴
╶╴╶╴╶╴╶╴⚫╶╴╶╴╶╴╶╴
╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴
╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴
╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴
╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴
```

I wrote this in a fever dream. Through liberal use of the walrus operator, we set the location of each star point to a -1. By creating an array the same size as our game board, we'll be able to combine them.

```py
from itertools import product

star_points = np.zeros((size,size), dtype=int)
s = 3 if size > 9 else 2
d = '-' * (s + 1)
corners = [j for i in range(3) if (j:=(s+(2*s*i))) < size]
pts = [(f:=size//2, f)] + list(product(corners, repeat=2))
star_points[*zip(*pts)] = -1

print(star_points)
```

```
array([[ 0,  0,  0,  0,  0,  0,  0,  0,  0],
       [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
       [ 0,  0, -1,  0,  0,  0, -1,  0,  0],
       [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
       [ 0,  0,  0,  0, -1,  0,  0,  0,  0],
       [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
       [ 0,  0, -1,  0,  0,  0, -1,  0,  0],
       [ 0,  0,  0,  0,  0,  0,  0,  0,  0],
       [ 0,  0,  0,  0,  0,  0,  0,  0,  0]])
```

By masking out the game pieces that have already been played, we can assign the star points to the game board for "rendering".

```py
SP = "╺╸"

# make a copy before applying the star points; we don't want our game state to
# contain anything other than zeros, ones, and twos
board = state.copy()
mask = ~state.astype(bool)
board[mask] = star_points[mask]

for row in board:
    print(''.join([(PT,B,W,SP)[i] for i in row]))
```

```
╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴
╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴
╶╴╶╴╺╸⚪╶╴╶╴╺╸╶╴╶╴
╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴
╶╴╶╴╶╴╶╴⚫╶╴╶╴╶╴╶╴
╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴
╶╴╶╴╺╸╶╴╶╴╶╴╺╸╶╴╶╴
╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴
╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴
```

Next up, row and column labels.

```py
ALPHA = 'abcdefghijklmnopqrstuvwxyz'

joined = ' '.join(list(ALPHA.replace('i', '')[:size])).upper()
rows = [col_label:=f"{d}{joined}{d}"]

for r, input_row in enumerate(board, 1):
    row = ''.join([(PT,B,W,SP)[i] for i in input_row])
    num = str(size - r + 1)
    lnum = num.rjust(int(len(str(size))))
    rnum = num.ljust(int(len(str(size))))
    rows.append(f'{lnum} {row} {rnum}')

rows.append(col_label)

print('\n'.join(rows))
```

```
--A B C D E F G H J --
9 ╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴ 9
8 ╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴ 8
7 ╶╴╶╴╺╸⚪╶╴╶╴╺╸╶╴╶╴ 7
6 ╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴ 6
5 ╶╴╶╴╶╴╶╴⚫╶╴╶╴╶╴╶╴ 5
4 ╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴ 4
3 ╶╴╶╴╺╸╶╴╶╴╶╴╺╸╶╴╶╴ 3
2 ╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴ 2
1 ╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴╶╴ 1
--A B C D E F G H J --
```

Finally, let's give it a coat of paint with some [ANSI color escape codes](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors).

```py
BLACK = '\033[30m'
GRAY = '\033[90m'
YELLOW = '\033[33m'
BG_YELLOW = '\033[43m'
RESET = '\033[0m'


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

print('\n'.join(rows))
```

<img href="images/9x9.png" />

- printing to the terminal
- finding neighbors
- finding groups

- OGS API
    - https://ogs.readme.io/docs/real-time-api
    - https://apidocs.online-go.com/
    - https://ogs.docs.apiary.io/#
    - thanks to [walken at ogs forums](https://forums.online-go.com/t/ogs-api-notes/17136)
- Smart Game Format
- vhs
    - nixos
    - docker
- plotly
- discord
- docker
