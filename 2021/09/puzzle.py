import fileinput
from collections import defaultdict
from functools import reduce
from itertools import product

x = [line.strip() for line in fileinput.input()]
heights = [[int(pos) for pos in line] for line in x]

HEIGHT = len(heights)
WIDTH = len(heights[0])

height_dict = defaultdict(lambda: 9)
for i, j in product(range(HEIGHT), range(WIDTH)):
    height_dict.update({(i, j): heights[i][j]})


def low_point(d, i, j):
    # lower than all neighbors if lower than lowest neighbor
    return d[i, j] < min(d[i + 1, j], d[i - 1, j], d[i, j + 1], d[i, j - 1])


def find_neighbors(d, i, j, visited: set, neighbors: set):
    visited.add((i, j))
    for neighbor in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
        if d[neighbor] != 9:
            neighbors.add(neighbor)
            if neighbor not in visited:
                _ = find_neighbors(d, neighbor[0], neighbor[1], visited, neighbors)
    return neighbors


sum_risk = 0
num_neighbors = []
for i, j in product(range(HEIGHT), range(WIDTH)):
    if low_point(height_dict, i, j):
        sum_risk += 1 + height_dict[i, j]

        neighbors = find_neighbors(height_dict, i, j, set(), set())
        num_neighbors.append(len(neighbors))

print(f"part 1: {sum_risk}")
print(f"part 2: {reduce(lambda a, b: a*b, sorted(num_neighbors)[-3:])}")
