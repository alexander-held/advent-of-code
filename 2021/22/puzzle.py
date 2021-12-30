import fileinput
import re
from collections import Counter, defaultdict

x = [line.strip() for line in fileinput.input()]

state = defaultdict(bool)
for line in x:
    turn_on = True if line.startswith("on") else False
    x1, x2, y1, y2, z1, z2 = list(map(int, re.findall("-?\d+", line)))
    for xi in range(max(-50, x1), min(50 + 1, x2 + 1)):
        for yi in range(max(-50, y1), min(50 + 1, y2 + 1)):
            for zi in range(max(-50, z1), min(50 + 1, z2 + 1)):
                state[(xi, yi, zi)] = turn_on  # track each state

print(f"part 1: {Counter(state.values())[True]}")

# part 2: change approach, union of two instructions is sum minus intersection

# count how many times to consider each cube, cube states are 0 (off), 1 (on), or
# -1 (cancels out contributions from overlapping cubes that are on)
# states could have larger values if instructions contain cubes multiple times
cube_states = defaultdict(int)
for line in x:
    turn_on = 1 if line.startswith("on") else -1
    x1, x2, y1, y2, z1, z2 = list(map(int, re.findall("-?\d+", line)))

    # find intersections of current cube with already existing cubes
    # loop over clone of cube_states, as they change during loop when cubes are appended
    for cube_coordinates, state in cube_states.copy().items():
        a1, a2, b1, b2, c1, c2 = cube_coordinates
        if a1 <= x2 and a2 >= x1 and b1 <= y2 and b2 >= y1 and c1 <= z2 and c2 >= z1:
            # overlap exists
            ol_x = (max(a1, x1), min(a2, x2))
            ol_y = (max(b1, y1), min(b2, y2))
            ol_z = (max(c1, z1), min(c2, z2))
            overlap_cube = (ol_x[0], ol_x[1], ol_y[0], ol_y[1], ol_z[0], ol_z[1])
            # add overlap cube with opposite sign to existing sign
            # (this is the intersection to subtract double-counting effects)
            cube_states[overlap_cube] -= state

    if turn_on == 1:
        # add only turn on instruction, turn off instructions handled via overlap
        cube_states[(x1, x2, y1, y2, z1, z2)] += 1

total_volume = 0
for cube_coordinates, state in cube_states.items():
    x1, x2, y1, y2, z1, z2 = cube_coordinates
    cube_volume = (x2 - x1 + 1) * (y2 - y1 + 1) * (z2 - z1 + 1)
    total_volume += cube_volume * state  # add volume scaled by state

print(f"part 2: {total_volume}")
