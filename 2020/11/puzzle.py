import fileinput
import numpy as np


def get_input():
    x = np.asarray([list(line.strip()) for line in fileinput.input()])
    # padding: put floor all around the grid
    x = np.vstack((["."] * x.shape[1], x, ["."] * x.shape[1]))
    x = np.insert(x, 0, ".", axis=-1)
    x = np.insert(x, x.shape[1], ".", axis=-1)
    return x


def count_adjacent(x, i, j):  # counting for part 1
    adj = (x[i - 1, j - 1] == "#") + (x[i - 1, j] == "#") + (x[i - 1, j + 1] == "#")
    adj += (x[i, j - 1] == "#") + (x[i, j + 1] == "#")
    adj += (x[i + 1, j - 1] == "#") + (x[i + 1, j] == "#") + (x[i + 1, j + 1] == "#")
    return adj


def update_grid(x, threshold, counting_func):
    """For better performance: should probably have a second grid that remembers which
    seats were updated in the previous iteration. If no surrounding seats changed, there
    is no reason to check whether the current seat will change.
    """
    next_grid = x.copy()
    for i in range(1, x.shape[0] - 1):
        for j in range(1, x.shape[1] - 1):
            if x[i, j] == ".":  # floor does not change
                continue
            count = counting_func(x, i, j)
            if x[i, j] == "L" and count == 0:  # fill seat
                next_grid[i, j] = "#"
            elif x[i, j] == "#" and count >= threshold:  # seat becomes empty
                next_grid[i, j] = "L"
    return next_grid


def prettyprint(x):
    inner_x = ["".join(l[1:-1]) for l in x[1:-1]]
    for l in inner_x:
        print(l)
    print()


# part 1
x = get_input()
while True:
    next_x = update_grid(x, 4, count_adjacent)
    # prettyprint(x)
    if (next_x == x).all():
        print(f"stable state, {len(x[x=='#'])} seats occupied")
        break
    x = next_x


def count_in_line(x, i, j):  # counting for part 2
    count = 0
    for line_of_sight in [
        x[i + 1 :, j],
        x[:i, j][::-1],
        x[i, j + 1 :],
        x[i, :j][::-1],
        [x[i + n, j + n] for n in range(1, min(x.shape[0] - i, x.shape[1] - j))],
        [x[i - n, j + n] for n in range(1, min(i, x.shape[1] - j))],
        [x[i + n, j - n] for n in range(1, min(x.shape[0] - i, j))],
        [x[i - n, j - n] for n in range(1, min(i, j))],
    ]:
        count += next((xi for xi in line_of_sight if xi != "."), -1) == "#"
    return count


# part 2
x = get_input()
while True:
    next_x = update_grid(x, 5, count_in_line)
    # prettyprint(x)
    if (next_x == x).all():
        print(f"stable state, {len(x[x=='#'])} seats occupied")
        break
    x = next_x
