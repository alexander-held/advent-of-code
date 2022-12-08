import fileinput

import numpy as np

x = np.asarray([[int(tree) for tree in line.strip()] for line in fileinput.input()])

size_y, size_x = x.shape
num_visible = size_y * 2 + size_x * 2 - 4  # edges are visible
for pos_y in range(1, size_y - 1):
    for pos_x in range(1, size_x - 1):
        cur_tree = x[pos_y][pos_x]
        if (
            np.all(x[pos_y, 0:pos_x] < cur_tree)  # visible from left
            or np.all(x[0:pos_y, pos_x] < cur_tree)  # top
            or np.all(x[pos_y, pos_x + 1 : size_x] < cur_tree)  # right
            or np.all(x[pos_y + 1 : size_y, pos_x] < cur_tree)  # bottom
        ):
            num_visible += 1

print(f"part 1: {num_visible}")


def get_score(trees, house):
    # find first tree that is as tall or taller
    return next((idx + 1 for idx, t in enumerate(trees) if t >= house), len(trees))


score_max = 0
for house_y in range(size_y):
    for house_x in range(size_x):
        house = x[house_y, house_x]

        score_left = get_score(x[house_y, 0:house_x][::-1], house)
        score_top = get_score(x[0:house_y, house_x][::-1], house)
        score_right = get_score(x[house_y, house_x + 1 : size_x], house)
        score_bottom = get_score(x[house_y + 1 : size_y :, house_x], house)

        if (score := score_left * score_top * score_right * score_bottom) > score_max:
            score_max = score

print(f"part 2: {score_max}")
