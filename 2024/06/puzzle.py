import fileinput
from collections import defaultdict

x = [line for line in fileinput.input()]

lab = defaultdict(str)
for a in range(len(x)):
    for b in range(len(x[0])):
        lab[a + 1j * b] = x[a][b]


def walk_to_edge(lab, cur_pos, obs=None):
    direc = -1
    states = {(cur_pos, direc)}
    while lab[cur_pos + direc] != "":  # continue until next step leaves map
        if lab[cur_pos + direc] == "#" or cur_pos + direc == obs:
            direc *= -1j  # would collide, so turn instead
        else:
            cur_pos += direc  # take step forward
        if (cur_pos, direc) in states:
            return None  # loop detected
        states.add((cur_pos, direc))
    return states


start = next(k for k, v in lab.items() if v == "^")
seen = set(s[0] for s in walk_to_edge(lab, start))  # tiles seen in part 1
# place obstacles in path of guard for part 2
num_stuck = sum(walk_to_edge(lab, start, obs=obs) is None for obs in seen - {start})

print(f"part 1: {len(seen)}")
print(f"part 2: {num_stuck}")
