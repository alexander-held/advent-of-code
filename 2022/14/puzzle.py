import fileinput

x = [line.strip().split(" -> ") for line in fileinput.input()]

blocked = set()
for line in x:
    tuples = [list(map(int, val.split(","))) for val in line]
    for (x1, y1), (x2, y2) in zip(tuples, tuples[1:]):
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1
        for x_pos in range(x1, x2 + 1):
            for y_pos in range(y1, y2 + 1):
                blocked.add(x_pos + 1j * y_pos)

pos_floor = max(s.imag for s in blocked) + 2


def simulate_sand(blocked, p2=False):
    num_sand = 0
    while True:  # simulate one piece of sand
        sand = 500
        while True:  # sand moves
            if 500 in blocked:
                return num_sand  # source blocked
            if sand.imag >= pos_floor and not p2:
                return num_sand  # sand dropped out of area
            elif p2 and sand.imag == pos_floor - 1:
                break  # at rest above bottom floor
            elif sand + 1j not in blocked:  # sand drops down
                sand += 1j
            elif sand - 1 + 1j not in blocked:  # diagonally left
                sand += -1 + 1j
            elif sand + 1 + 1j not in blocked:  # diagonally right
                sand += 1 + 1j
            else:
                break  # no way to move

        blocked.add(sand)
        num_sand += 1


print(f"part 1: {simulate_sand(blocked.copy())}")
print(f"part 2: {simulate_sand(blocked.copy(), p2=True)}")
