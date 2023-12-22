import fileinput
from functools import cache

x = [line.strip() for line in fileinput.input()]

bricks = {}
for i, line in enumerate(x):
    start, end = [list(map(int, l.split(","))) for l in line.split("~")]
    bricks[i] = {
        "x": range(start[0], end[0] + 1),
        "y": range(start[1], end[1] + 1),
        "z": range(start[2], end[2] + 1),
        "supported_by": set(),
        "supporting": set(),
    }

# sort from bottom to top
bricks = dict(sorted(bricks.items(), key=lambda c: c[1]["z"].start))


def xy_overlap(c1, c2):
    x_overlap = any([pos_x in c1["x"] for pos_x in c2["x"]])
    y_overlap = any([pos_y in c1["y"] for pos_y in c2["y"]])
    return x_overlap and y_overlap


for active_brick in bricks.values():  # try dropping all active bricks
    has_target = False
    sorted_ref = dict(sorted(bricks.items(), key=lambda c: c[1]["z"].stop))
    for ref_brick in list(sorted_ref.values())[::-1]:  # target bricks, highest first
        if ref_brick["z"].stop > active_brick["z"].start:
            continue  # reference brick is too high, cannot fall onto it
        if xy_overlap(active_brick, ref_brick):  # overlap in x-y plane allows dropping
            drop = active_brick["z"].start - ref_brick["z"].stop
            active_brick["z"] = range(
                active_brick["z"].start - drop, active_brick["z"].stop - drop
            )
            has_target = True
            break
    if not has_target:  # no brick to drop to, drop to floor instead
        drop = active_brick["z"].start - 1
        active_brick["z"] = range(
            active_brick["z"].start - drop, active_brick["z"].stop - drop
        )

# check which bricks each brick supports and is supported by
for active_brick in bricks.values():
    for id_r, ref_brick in bricks.items():
        if xy_overlap(active_brick, ref_brick):
            if active_brick["z"].stop == ref_brick["z"].start:
                active_brick["supporting"].add(id_r)
            elif active_brick["z"].start == ref_brick["z"].stop:
                active_brick["supported_by"].add(id_r)

# handle disintegration
num_disintegrated = 0
for id_a, active_brick in bricks.items():
    can_disintegrate = True
    for id_s in active_brick["supporting"]:
        if len(bricks[id_s]["supported_by"] - {id_a}) == 0:
            can_disintegrate = False  # brick is only support for target

    if can_disintegrate:
        num_disintegrated += 1

print(f"part 1: {num_disintegrated}")


@cache
def get_falling(id_a, supporting, falling=None):
    # very inefficient algorithm, can presumably be significantly improved
    if falling is None:
        falling = set()
    else:
        falling = set(falling)  # use set internally, tuple for cache
    falling_new = set()
    for id_s in supporting:
        if len(bricks[id_s]["supported_by"] - falling) == 0:
            falling_new |= {id_s}  # all supports are falling, so this will fall too
        if len(bricks[id_s]["supported_by"] - {id_a}) == 0:
            falling_new |= {id_s}  # no other supports, so this will fall too

    for id_s in falling_new:  # recursively get full list of falling bricks
        falling |= get_falling(
            id_s, tuple(bricks[id_s]["supporting"]), tuple(falling | falling_new)
        )
    return falling


sum_falling = 0
for id_a, active_brick in bricks.items():
    sum_falling += len(get_falling(id_a, tuple(active_brick["supporting"])))

print(f"part 2: {sum_falling}")
