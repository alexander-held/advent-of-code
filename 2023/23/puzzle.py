import fileinput
from collections import defaultdict, deque
from functools import cache

x = [line.strip() for line in fileinput.input()]

trail_map = defaultdict(lambda: "#")

for y_pos, line in enumerate(x):
    for x_pos, ch in enumerate(line):
        trail_map[x_pos + 1j * y_pos] = ch


def steps_to_target(pos, direc, p2):  # steps to reach target, otherwise None
    tile = trail_map[pos + direc]
    num_steps = 2 if (tile in ">v" and not p2) else 1  # slide in part 1
    if tile != "#":
        if (not p2) and ((tile == ">" and direc != 1) or (tile == "v" and direc != 1j)):
            return None
        else:
            return num_steps
    return None


@cache
def walk_until_split(pos_start, p2):
    neighbors = set()
    for direc_start in (-1j, 1, 1j, -1):  # start by finding paths in all directions
        steps_start = steps_to_target(pos_start, direc_start, p2)
        if steps_start is None:
            continue  # invalid direction

        pos = pos_start + direc_start * steps_start  # position after initial step
        seen = {pos_start, pos}
        pos_list = deque([(pos, steps_start)])

        if pos.imag == len(x) - 1:  # arrived at end
            neighbors.add((pos, steps_start))

        while pos_list:  # explore until finding new node
            pos, steps_so_far = pos_list.popleft()
            for direc in (-1j, 1, 1j, -1):
                steps = steps_to_target(pos, direc, p2)
                if steps and pos + direc * steps not in seen:
                    pos_list.append((pos + direc * steps, steps_so_far + steps))
                    seen.add(pos + direc * steps)
                    if (pos + direc * steps).imag == len(x) - 1:  # arrived at end
                        neighbors.add((pos + direc * steps, steps_so_far + steps))
            if len(pos_list) > 1:  # branching happened: found new node
                neighbors.add((pos, steps_so_far))
                break
    return neighbors  # return all neighboring nodes


def take_hike(start, p2=False):
    paths = deque([(start, 0, {start})])
    len_hikes = []
    while len(paths):
        cur_tile, trail_len, seen = paths.popleft()
        neighbors = walk_until_split(cur_tile, p2)  # find next node
        for target, distance in neighbors:
            if target in seen:
                continue
            elif target.imag == len(x) - 1:  # arrived at end
                len_hikes.append(trail_len + distance)
            else:  # hike more
                paths.append((target, trail_len + distance, seen | {target}))
    return len_hikes


start = next(i for i, ch in enumerate(x[0]) if ch == ".")

print(f"part 1: {max(take_hike(start))}")
print(f"part 2: {max(take_hike(start, p2=True))}")  # ~1 min with pypy
