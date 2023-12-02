import fileinput
from collections import defaultdict
from math import prod
import re

x = [line.strip() for line in fileinput.input()]

id_sum = 0
power_sum = 0

for gid, game in enumerate(x, start=1):
    possible = True
    cubes_needed = defaultdict(int)
    for draw in game.split(": ")[1].split("; "):
        for num, col in re.findall(r"(\d+) (\w+)", draw):
            cubes_needed[col] = max(cubes_needed[col], int(num))  # keep track of max
            if int(num) > {"red": 12, "green": 13, "blue": 14}[col]:
                possible = False

    power_sum += prod(cubes_needed.values())

    if possible:
        id_sum += gid

print(f"part 1: {id_sum}")
print(f"part 2: {power_sum}")
