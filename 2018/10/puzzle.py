import fileinput
import re
from itertools import count

import numpy as np

x = [line.strip() for line in fileinput.input()]

positions = []
velocities = []
for line in x:
    px, py, vx, vy = map(int, re.findall(r"-?\d+", line))
    positions.append([px, py])
    velocities.append([vx, vy])
positions = np.asarray(positions)
velocities = np.asarray(velocities)

for t in count():
    max_abs = np.max(np.abs(positions))  # assumes image converges around (0, 0)
    if max_abs < 250:  # 250 found through experimentation, can start larger
        print("part 1:")
        tup = tuple(tuple(p) for p in positions)  # for checking filled positions
        for j in range(min(positions[:, 1]), max(positions[:, 1]) + 1):
            for i in range(min(positions[:, 0]), max(positions[:, 0]) + 1):
                print(f"{'#' if (i,j) in tup else '.'}", end="")
            print()
        print(f"part 2: {t}")
        input("enter to continue if not solved yet, ctrl+c to break")

    positions += velocities
