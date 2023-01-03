import fileinput
from itertools import cycle

x = "".join([line.strip() for line in fileinput.input()])

# rocks denoted as filled positions counting from bottom left corner
# horizontal: real, vertical: imaginary
ROCKS = [
    (0, 1, 2, 3),
    (1, 1j, 1 + 1j, 1 + 2j, 2 + 1j),
    (0, 1, 2, 2 + 1j, 2 + 2j),
    (0, 1j, 2j, 3j),
    (0, 1, 1j, 1 + 1j),
]
tower_height = lambda blocked_fields: int(max(t.imag for t in blocked_fields))


def simulate(jet_pattern, p2=False):
    rock_cycler = cycle(ROCKS)
    blocked = set((0, 1, 2, 3, 4, 5, 6))  # positions filled by rock (starts with floor)
    current_rock = None  # tuple with absolute position of constituents
    n_rocks = 0  # number of rocks spawned

    # variables for cycle detection
    last_height = 0  # height at start of cycle
    last_height_diff = 0  # height gained in last cycle
    last_rock = None  # type of rock at start of cycle
    last_n_rocks = 0  # number of rocks spawned at start of cycle

    for i, jet_dir in enumerate(cycle(jet_pattern)):
        # cycle detection for part 2
        if (
            i % len(x) == 0  # start of jet pattern
            and i > 0
            and (last_rock is None or n_rocks % 5 == last_rock)  # same rock type
            and p2
        ):
            height = tower_height(blocked)
            if height - last_height == last_height_diff:
                # cycle detected: same height gained as last time at this configuration
                rocks_per_cycle = n_rocks - last_n_rocks
                # determine how many full cycles are left (plus remaining extra spawns)
                num_cycles_left, remainder = divmod(1e12 - n_rocks, rocks_per_cycle)
                # height gained from full cycles
                height_offset = num_cycles_left * last_height_diff
                # move the whole tower up by the amount it would gain from these cycles
                n_rocks = 1e12 - remainder  # only need to take care of remaining spawns
                blocked = set(b + height_offset * 1j for b in blocked)  # move tower
                if current_rock is not None:  # update rock position
                    current_rock = tuple(r + height_offset * 1j for r in current_rock)

            last_height_diff = height - last_height
            last_height = height
            last_rock = n_rocks % 5
            last_n_rocks = n_rocks

        if current_rock is None:
            if n_rocks == 2022 and not p2:
                return tower_height(blocked)
            elif n_rocks == 1e12 and p2:
                return tower_height(blocked)

            # spawn a rock if none is currently active
            n_rocks += 1
            pos_bot_left = tower_height(blocked) * 1j + 4j + 2
            current_rock = tuple(p + pos_bot_left for p in next(rock_cycler))

        # push rock left/right
        moved_rock = tuple(r + {">": 1, "<": -1}[jet_dir] for r in current_rock)
        if (
            min(r.real for r in moved_rock) >= 0  # left edge
            and max(r.real for r in moved_rock) <= 6  # right edge
            and all(r not in blocked for r in moved_rock)  # previous rocks and floor
        ):
            # rock stays within bounds, so it can move
            current_rock = moved_rock

        # rock falls
        moved_rock = tuple(r - 1j for r in current_rock)
        if all(r not in blocked for r in moved_rock):
            # does not collide with previous rocks or floor
            current_rock = moved_rock
        else:
            # rock has reached final spot and becomes inactive
            blocked.update(current_rock)
            current_rock = None  # need new rock


print(f"part 1: {simulate(x)}")
print(f"part 2: {simulate(x, p2=True)}")
