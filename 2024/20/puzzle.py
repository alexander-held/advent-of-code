import fileinput
from collections import defaultdict, deque

x = [line.strip() for line in fileinput.input()]
grid = defaultdict(lambda: "#")
for a in range(len(x)):
    for b in range(len(x[0])):
        grid[a + 1j * b] = x[a][b]


start = next(k for k, v in grid.items() if v == "S")
next_steps = deque([(start, [start])])  # position, path taken
while next_steps:  # no way to move past E in inputs, so will run out of steps there
    pos, path_taken = next_steps.pop()
    for direc in (-1j, -1, 1j, 1):
        if grid[pos + direc] in ".E" and pos + direc not in path_taken:
            next_steps.append((pos + direc, path_taken + [pos + direc]))


num_cheats_2ps = 0
num_cheats_20ps = 0
for idx, c_start in enumerate(path_taken):
    for c_len, c_end in enumerate(path_taken[idx + 1 :], start=1):
        c_time = abs((c_end - c_start).real) + abs((c_end - c_start).imag)
        # time saved is distance along path minus time taken
        if c_time == 2 and c_len - 2 >= 100:
            num_cheats_2ps += 1
        if c_time <= 20 and c_len - c_time >= 100:
            num_cheats_20ps += 1


print(f"part 1: {num_cheats_2ps}")
print(f"part 2: {num_cheats_20ps}")
