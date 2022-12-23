import fileinput

from collections import Counter
from itertools import count

x = [line for line in fileinput.input()]

grid = set()
for i_y, line in enumerate(x[::-1]):
    for i_x, char in enumerate(line):
        if char == "#":
            grid.add(i_x + 1j * i_y)


def move_north(elf, grid):
    if all(pos not in grid for pos in (elf + 1j, elf + 1 + 1j, elf - 1 + 1j)):
        return (elf, elf + 1j)


def move_south(elf, grid):
    if all(pos not in grid for pos in (elf - 1j, elf + 1 - 1j, elf - 1 - 1j)):
        return (elf, elf - 1j)


def move_west(elf, grid):
    if all(pos not in grid for pos in (elf - 1, elf - 1 + 1j, elf - 1 - 1j)):
        return (elf, elf - 1)


def move_east(elf, grid):
    if all(pos not in grid for pos in (elf + 1, elf + 1 + 1j, elf + 1 - 1j)):
        return (elf, elf + 1)


# proposals in order (cycling every turn)
prop_order = [move_north, move_south, move_west, move_east]

# 8 neighboring cells
# fmt: off
adj = lambda elf: (elf-1+1j, elf+1j, elf+1+1j, elf-1, elf+1, elf-1-1j, elf-1j, elf+1-1j)
# fmt: on

for i_round in count():
    old_grid = grid.copy()
    proposals = []

    for elf in grid:
        if all(pos not in grid for pos in adj(elf)):
            continue  # no elves in surrounding 8 cells

        # move proposals in cycling order
        if (proposal := prop_order[i_round % 4](elf, grid)) is not None:
            proposals.append(proposal)
        elif (proposal := prop_order[(i_round + 1) % 4](elf, grid)) is not None:
            proposals.append(proposal)
        elif (proposal := prop_order[(i_round + 2) % 4](elf, grid)) is not None:
            proposals.append(proposal)
        elif (proposal := prop_order[(i_round + 3) % 4](elf, grid)) is not None:
            proposals.append(proposal)

    # execute move proposals to unique destinations
    unique_dests = [k for k, v in Counter(p[1] for p in proposals).items() if v == 1]
    for elf, destination in proposals:
        if destination in unique_dests:
            grid -= {elf}
            grid |= {destination}

    if i_round + 1 == 10:
        min_x, max_x = int(min(g.real for g in grid)), int(max(g.real for g in grid))
        min_y, max_y = int(min(g.imag for g in grid)), int(max(g.imag for g in grid))
        rectangle_tiles = (max_x - min_x + 1) * (max_y - min_y + 1) - len(grid)
        print(f"part 1: {rectangle_tiles}")

    if old_grid == grid:
        print(f"part 2: {i_round+1}")
        break
