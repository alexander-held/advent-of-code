import fileinput
import re
from collections import defaultdict
from itertools import cycle

x = [line.strip("\n") for line in fileinput.input()]

path = [int(p) if p.isdigit() else p for p in re.split(r"([LR])", x[-1])]
board = defaultdict(lambda: " ")
for y_pos, line in enumerate(x[:-2]):
    for x_pos, ch in enumerate(line):
        board[x_pos + 1j * y_pos] = ch


def walk_forward(board, pos, direc, move):
    # find positions to cycle through (could cache this)
    if direc.real == 0:  # move up/down
        keys_row = sorted(
            [k for k in board.keys() if k.real == pos.real], key=lambda v: v.real
        )
        col = [p for p in keys_row if board[p] != " "]  # legal tile positions
        if direc == -1j:  # flip column
            col = col[::-1]
        start_idx = (next(i for i, t in enumerate(col) if pos == t) + 1) % len(col)
        to_cycle = col[start_idx:] + col[:start_idx]
    elif direc.imag == 0:  # move left/right (-1 / 1)
        keys_row = sorted(
            [k for k in board.keys() if k.imag == pos.imag], key=lambda v: v.real
        )
        row = [p for p in keys_row if board[p] != " "]  # legal tile positions
        if direc == -1:  # flip row
            row = row[::-1]
        start_idx = (next(i for i, t in enumerate(row) if pos == t) + 1) % len(row)
        to_cycle = row[start_idx:] + row[:start_idx]

    for i, target_pos in enumerate(cycle(to_cycle)):  # take one step at a time
        if i >= move:
            break  # move completed
        if board[target_pos] == "#":  # hit a wall
            break
        else:
            pos = target_pos

    return pos


# this hardcodes cube structure from input with faces identified as follows:
#    [1][2]
#    [3]
# [5][4]
# [6]
def walk_forward_p2(board, pos, direc, move):  # for part 2
    cel = len(x[0]) // 3  # cel: cube edge length
    for _ in range(move):  # one step at a time
        if board[pos + direc] == "#":  # hit a wall
            break  # stop moving
        elif board[pos + direc] == ".":  # can move
            pos += direc
        elif board[pos + direc] == " ":  # 7 edge transitions (2 directions each)
            direc_new = direc  # no rotation by default

            # transition 2->4 via (-1) rotation
            if pos.real == cel * 3 - 1 and pos.imag in range(cel) and direc == 1:
                # move one cube down + offset from edge
                pos_new = pos + 1j * (2 * ((cel - pos.imag - 1) % cel) + 1 + cel)
                pos_new -= cel  # horizontal move: 4 is to the left of 2
                direc_new *= -1

            # transition 4->2 via (-1) rotation
            elif (
                pos.real == cel * 2 - 1
                and pos.imag in range(2 * cel, 3 * cel)
                and direc == 1
            ):
                # move one cube up + offset from edge
                pos_new = pos - 1j * (2 * (pos.imag % cel) + cel + 1)
                pos_new += cel  # horizontal move: 2 is to the right of 4
                direc_new *= -1

            # transition 1->5 via (-1) rotation
            elif pos.real == cel and pos.imag in range(cel) and direc == -1:
                # move one cube down + offset from edge
                pos_new = pos + 1j * (2 * ((cel - pos.imag - 1) % cel) + 1 + cel)
                pos_new -= cel  # horizontal move: 5 is to the left of 1
                direc_new *= -1

            # transition 5->1 via (-1) rotation
            elif pos.real == 0 and pos.imag in range(2 * cel, 3 * cel) and direc == -1:
                # move one cube up + offset from edge
                pos_new = pos - 1j * (2 * (pos.imag % cel) + cel + 1)
                pos_new += cel  # horizontal move: 1 is to the right of 5
                direc_new *= -1

            # transition 2->6, no rotation
            elif pos.real in range(2 * cel, 3 * cel) and pos.imag == 0 and direc == -1j:
                pos_new = pos - cel * 2  # horizontal move: 6 is to the left of 2
                pos_new += 1j * (cel * 4 - 1)  # vertical move: 6 is below 2

            # transition 6->2, no rotation
            elif pos.real in range(cel) and pos.imag == 4 * cel - 1 and direc == 1j:
                pos_new = pos + cel * 2  # horizontal move: 2 is to the right of 2
                pos_new -= 1j * (cel * 4 - 1)  # vertical move: 2 is above 6

            # transition 2->3 via (1j) rotation
            elif (
                pos.real in range(2 * cel, 3 * cel)
                and pos.imag == cel - 1
                and direc == 1j
            ):
                pos_new = 2 * cel - 1 + 1j * (pos.real - cel)
                direc_new *= 1j

            # transition 3->2 via (-1j) rotation
            elif (
                pos.real == 2 * cel - 1
                and pos.imag in range(cel, 2 * cel)
                and direc == 1
            ):
                pos_new = pos.imag + cel + 1j * (cel - 1)
                direc_new *= -1j

            # transition 3->5 via (-1j) rotation
            elif pos.real == cel and pos.imag in range(cel, 2 * cel) and direc == -1:
                pos_new = pos.imag - cel + 1j * 2 * cel
                direc_new *= -1j

            # transition 5->3 via (1j) rotation
            elif pos.real in range(cel) and pos.imag == 2 * cel and direc == -1j:
                pos_new = cel + 1j * (pos.real + cel)
                direc_new *= 1j

            # transition 1->6 via (1j) rotation
            elif pos.real in range(cel, 2 * cel) and pos.imag == 0 and direc == -1j:
                pos_new = 1j * (pos.real + 2 * cel)
                direc_new *= 1j

            # transition 6->1 via (-1j) rotation
            elif pos.real == 0 and pos.imag in range(3 * cel, 4 * cel) and direc == -1:
                pos_new = pos.imag - 2 * cel
                direc_new *= -1j

            # transition 4->6 via (1j) rotation
            elif (
                pos.real in range(cel, 2 * cel)
                and pos.imag == 3 * cel - 1
                and direc == 1j
            ):
                pos_new = cel - 1 + 1j * (pos.real + 2 * cel)
                direc_new *= 1j

            # transition 6->4 via (-1j) rotation
            elif (
                pos.real == cel - 1
                and pos.imag in range(3 * cel, 4 * cel)
                and direc == 1
            ):
                pos_new = pos.imag - 2 * cel + 1j * (3 * cel - 1)
                direc_new *= -1j

            if board[pos_new] != "#":  # move if new position is not wall
                pos = pos_new
                direc = direc_new
            else:  # otherwise stay at current position
                break

    return pos, direc


def rotate(direc, move):
    if move == "L":
        return -1j * direc
    elif move == "R":
        return 1j * direc


def walk(board, path, p2=False):
    pos = next(i for i, ch in enumerate(x[0]) if ch == ".")
    direc = 1  # start moving to the right
    path = path.copy()
    while len(path):
        move = path.pop(0)
        if isinstance(move, int):
            if not p2:
                pos = walk_forward(board, pos, direc, move)
            else:
                pos, direc = walk_forward_p2(board, pos, direc, move)
        else:
            direc = rotate(direc, move)

    return int(
        1000 * (pos.imag + 1) + 4 * (pos.real + 1) + {1: 0, 1j: 1, -1: 2, -1j: 3}[direc]
    )


print(f"part 1: {walk(board, path)}")
print(f"part 2: {walk(board, path, p2=True)}")
