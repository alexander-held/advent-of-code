import fileinput
from itertools import count

x = [line.strip() for line in fileinput.input()]
WIDTH = len(x[0])
HEIGHT = len(x)

east = [set((i, j) for j, c in enumerate(li) if c == ">") for i, li in enumerate(x)]
east = set.union(*east)
south = [set((i, j) for j, c in enumerate(li) if c == "v") for i, li in enumerate(x)]
south = set.union(*south)


def step(east, south):
    occupied = east | south
    next_east = set()
    for cucumber in east:
        i, j = cucumber
        next_j = (j + 1) % WIDTH if (i, (j + 1) % WIDTH) not in occupied else j
        next_east.add((i, next_j))

    occupied = next_east | south
    next_south = set()
    for cucumber in south:
        i, j = cucumber
        next_i = (i + 1) % HEIGHT if ((i + 1) % HEIGHT, j) not in occupied else i
        next_south.add((next_i, j))
    return next_east, next_south


for i in count(1):
    next_east, next_south = step(east, south)
    if next_east == east and next_south == south:
        print(f"part 1: {i}")
        break
    east, south = next_east, next_south
