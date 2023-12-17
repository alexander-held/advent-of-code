import fileinput
from collections import defaultdict, deque


x = [line.strip() for line in fileinput.input()]
rock_map = defaultdict(lambda: "#")
for y_pos, line in enumerate(x):
    for x_pos, ch in enumerate(line):
        rock_map[x_pos + y_pos * 1j] = ch


def tilt(rock_map):
    # tilt north, iterate in increasing vertical position
    all_rocks = deque(
        sorted([k for k, v in rock_map.items() if v == "O"], key=lambda v: v.imag)
    )
    while all_rocks:
        pos = all_rocks.popleft()  # next rock
        # rock can move until character is not .
        chars = "".join([rock_map[pos - dy * 1j] for dy in range(1, int(pos.imag) + 1)])
        num_moves = next((i for i, c in enumerate(chars) if c != "."), len(chars))
        rock_map[pos] = "."  # rock moves
        rock_map[pos - num_moves * 1j] = "O"
    return rock_map


def rotate(rock_map):
    new_map = defaultdict(lambda: "#")
    for k, v in rock_map.items():
        new_map[len(x) - 1 - k.imag + k.real * 1j] = v  # rotate clockwise
    return new_map


def calculate_load(rock_map):
    total_load = 0
    for pos_y in range(len(x)):
        n_rocks = sum([1 for k, v in rock_map.items() if v == "O" and k.imag == pos_y])
        total_load += n_rocks * (len(x) - pos_y)
    return total_load


def do_cycles(rock_map, num_cycles):
    seen = dict()  # contains tuple versions of map as keys and cycle number as values
    for i_cyc in range(num_cycles):
        for _ in range(4):
            rock_map = tilt(rock_map)
            rock_map = rotate(rock_map)

        if tuple((k, v) for k, v in rock_map.items()) in seen:
            cyc_start = seen[tuple((k, v) for k, v in rock_map.items())]
            return cyc_start, i_cyc - cyc_start  # cycle start and length

        seen[tuple((k, v) for k, v in rock_map.items())] = i_cyc

    return calculate_load(rock_map)


print(f"part 1: {calculate_load(tilt(rock_map))}")

# the implementation would benefit from more suitable data structures to speed this up
c_start, c_len = do_cycles(rock_map, 1_000_000)  # find repeating cycle
print(f"part 2: {do_cycles(rock_map, c_start + (1_000_000_000 - c_start) % c_len)}")
