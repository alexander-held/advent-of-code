import fileinput
from collections import defaultdict, Counter
from itertools import product

x = [line.strip() for line in fileinput.input()]
algorithm = x[0]

image = defaultdict(lambda: ".")
for i, line in enumerate(x[2:]):
    for j, char in enumerate(line):
        image[(i, j)] = char


def get_number(image, i, j):
    num = ""
    for offset_i, offset_j in product([-1, 0, 1], repeat=2):
        num += "1" if image[(i + offset_i, j + offset_j)] == "#" else "0"
    return int(num, 2)

def step(image, algorithm, default_char):
    # next default character depends on previous default, look up in algorithm for
    # two cases: previous default was "." -> index 0, or "#" -> index 511
    new_default = algorithm[0] if default_char == "." else algorithm[511]
    new_image = defaultdict(lambda: new_default)

    seen = set()  # sites already visited

    # loop over sites filled with "#", need copy as access of empty fields changes len
    for i, j in filter(lambda pos: image[pos] == "#", image.copy().keys()):
        # loop over all adjacent sites
        for offset_i, offset_j in product([-2, -1, 0, 1, 2], repeat=2):
            if (i + offset_i, j + offset_j) in seen:
                continue  # only visit each site once
            num = get_number(image, i + offset_i, j + offset_j)
            new_image[(i + offset_i, j + offset_j)] = algorithm[num]
            seen.add((i + offset_i, j + offset_j))
    return new_image, new_default


for part_i, num_steps in enumerate([2, 50]):
    next_image = image.copy()
    default_char = "."  # pixels are off by default at start
    for i_step in range(num_steps):
        next_image, default_char = step(next_image, algorithm, default_char)
    print(f"part {part_i+1}: {Counter(next_image.values())['#']}")
