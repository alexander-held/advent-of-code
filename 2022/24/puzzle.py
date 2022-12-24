import fileinput
from itertools import count

x = [line.strip() for line in fileinput.input()]

blizzards = set()
edges = [[0, len(x[0]) - 1], [0, len(x) - 1]]  # wall positions, inaccessible
for pos_y, line in enumerate(x):
    for pos_x, char in enumerate(line):
        pos = pos_x + 1j * pos_y
        if pos_y == 0 and char == ".":
            start = pos
        elif pos_y == len(x) - 1 and char == ".":
            end = pos
        elif char in "^v<>":
            blizzards.add((pos, {"^": -1j, "v": 1j, "<": -1, ">": 1}[char]))


def update_blizzards(blizzards):
    new_blizzards = set()
    for b in blizzards:
        new_pos = b[0] + b[1]
        if new_pos.real == edges[0][1]:  # right edge -> move to left
            new_pos = 1 + 1j * new_pos.imag
        elif new_pos.real == edges[0][0]:  # left edge -> move to right
            new_pos = edges[0][1] - 1 + 1j * new_pos.imag
        elif new_pos.imag == edges[1][1]:  # bottom edge -> move top
            new_pos = new_pos.real + 1j
        elif new_pos.imag == edges[1][0]:  # top edge -> move bottom
            new_pos = new_pos.real + 1j * (edges[1][1] - 1)
        new_blizzards.add((new_pos, b[1]))
    return new_blizzards


def get_possible_moves(pos, blocked, edges):
    targets = set()
    for direction in [0, 1, -1, 1j, -1j]:
        p = pos + direction
        if p in [start, end]:
            targets.add(p)
        elif p not in blocked:
            if (
                edges[0][0] < p.real < edges[0][1]  # horizontally in bounds
                and edges[1][0] < p.imag < edges[1][1]  # vertically in bounds
            ):
                targets.add(p)
    return targets


def explore(start, end, blizzards, edges):
    # flood fill to get all accessible positions per time
    cur_pos = {start}
    for t in count(1):
        blizzards = update_blizzards(blizzards)
        blocked = {b[0] for b in blizzards}
        moves = set.union(*(get_possible_moves(p, blocked, edges) for p in cur_pos))
        if end in moves:
            return t, blizzards
        cur_pos = moves


t1, blizzards = explore(start, end, blizzards, edges)  # start to end
print(f"part 1: {t1}")

t2, blizzards = explore(end, start, blizzards, edges)  # back to start
t3, _ = explore(start, end, blizzards, edges)  # again to end
print(f"part 2: {t1 +t2 + t3}")
