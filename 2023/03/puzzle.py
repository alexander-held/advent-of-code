import fileinput
from math import prod
import re


x = [line.strip() for line in fileinput.input()]

part_sum = 0
gear_ratio = 0
for i, line in enumerate(x):
    for num in re.finditer(r"\d+", line):  # part 1
        adj = False  # search for adjacent symbols
        for y_pos in (i - 1, i, i + 1):
            for x_pos in range(num.start() - 1, num.end() + 1):
                if not ((0 < y_pos < len(x) - 1) and (0 < x_pos < len(x[0]) - 1)):
                    continue  # out of bounds
                ch = x[y_pos][x_pos]
                if not ch.isdigit() and ch != ".":
                    adj = True
        if adj:
            part_sum += int(num.group())

    for j, ch in enumerate(line):  # part 2
        if ch == "*":
            gear_adj = []  # track adjacent gears
            for y_pos in (i - 1, i, i + 1):
                if not (0 <= y_pos <= len(x) - 1):
                    continue  # out of bounds
                for num in re.finditer(r"\d+", x[y_pos]):
                    if j in range(num.start() - 1, num.end() + 1):  # check adjacency
                        gear_adj.append(int(num.group()))
            if len(gear_adj) == 2:
                gear_ratio += prod(gear_adj)

print(f"part 1: {part_sum}")
print(f"part 2: {gear_ratio}")
