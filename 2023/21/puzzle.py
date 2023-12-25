import fileinput
from collections import defaultdict

import sympy

x = [line.strip() for line in fileinput.input()]

garden = defaultdict(lambda: "#")
for pos_y, line in enumerate(x):
    for pos_x, ch in enumerate(line):
        garden[pos_x + 1j * pos_y] = ch


def find_next_positions(garden, n_steps, p2=False):
    cur_positions = {next((k for k, v in garden.items() if v == "S"))}  # starting point
    num_plots = []  # number of garden plots to reach per number of steps
    for i in range(max(n_steps)):
        next_positions = set()  # list of valid garden plots to move to
        for cur_pos in cur_positions:
            for offset in (-1j, 1, 1j, -1):  # try all four directions
                if not p2:
                    is_valid = garden[cur_pos + offset] != "#"
                else:
                    pos_x = (cur_pos + offset).real % len(x[0])
                    pos_y = (cur_pos + offset).imag % len(x)
                    is_valid = garden[pos_x + 1j * pos_y] != "#"

                if is_valid:
                    next_positions.add(cur_pos + offset)  # valid target
        cur_positions = next_positions
        if i + 1 in n_steps:
            num_plots.append(len(next_positions))
    return num_plots


print(f"part 1: {find_next_positions(garden, [64])[0]}")

# part 2
# can travel straight in all cardinal directions with zero obstacles in the way
# input size is 131 x 131 (65 steps in each direction to edge)
# 26501365 steps will end up at edge of the square number (26501365-65)/131=202300

# scaling looks quadratic by inspection, which makes sense for 2d area, so interpolate
# with edges of grid (where patterns repeat)
to_edge, to_next_square = (len(x) - 1) // 2, len(x)
n_steps = [to_edge, to_edge + to_next_square, to_edge + 2 * to_next_square]
targets = find_next_positions(garden, n_steps, p2=True)

a, b, c = sympy.symbols("a,b,c")
equations = [n_steps[i] ** 2 * a + n_steps[i] * b + c - targets[i] for i in range(3)]
res = sympy.solve(equations, [a, b, c], dict=True)[0]
print(f"part 2: {26501365**2 * res[a] + 26501365 * res[b] + res[c]}")
