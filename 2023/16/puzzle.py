import fileinput
from collections import defaultdict, deque

x = [line.strip() for line in fileinput.input()]

beam_map = defaultdict(lambda: ".")
for y_pos in range(len(x)):
    for x_pos in range(len(x[0])):
        beam_map[x_pos + 1j * y_pos] = x[y_pos][x_pos]


def take_step(pos, direc, beam_map):
    cur_tile = beam_map[pos]
    if (
        cur_tile == "."
        or (cur_tile == "-" and direc.imag == 0)
        or (cur_tile == "|" and direc.real == 0)
    ):
        new_direcs = [direc]
    elif cur_tile == "|":
        new_direcs = [-1j, 1j]
    elif cur_tile == "-":
        new_direcs = [-1, 1]
    elif cur_tile == "\\":
        new_direcs = [(direc.conjugate()) * (1j)]
    elif cur_tile == "/":
        new_direcs = [(direc.conjugate()) * (-1j)]
    return [(pos + new_direc, new_direc) for new_direc in new_direcs]


def count_energized(cur_pos_and_direc):
    energized = defaultdict(lambda: False)
    seen = set()
    while len(cur_pos_and_direc):
        targets = take_step(*cur_pos_and_direc.popleft(), beam_map)
        for target, direc in targets:
            if (
                ((target, direc) not in seen)
                and (0 <= target.real <= len(x[0]) - 1)
                and (0 <= target.imag <= len(x) - 1)
            ):
                seen.add((target, direc))
                cur_pos_and_direc.append((target, direc))
                energized[target] = True
    return len(energized)


cur_pos_and_direc = deque([(-1, +1)])
print(f"part 1: {count_energized(cur_pos_and_direc)}")

energized = 0
for p_x in range(len(x[0])):
    energized = max(energized, count_energized(deque([(p_x - 1j, 1j)])))
    energized = max(energized, count_energized(deque([(p_x + len(x) * 1j, -1j)])))

for p_y in range(len(x)):
    energized = max(energized, count_energized(deque([(-1 + (p_y * 1j), 1)])))
    energized = max(energized, count_energized(deque([(len(x[0]) + (p_y * 1j), -1)])))

print(f"part 2: {energized}")
