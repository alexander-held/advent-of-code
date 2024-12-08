import fileinput
from itertools import combinations

x = [line.strip() for line in fileinput.input()]

antennas = []
for a in range(len(x)):
    for b in range(len(x[0])):
        if x[a][b].strip() != ".":
            antennas.append((x[a][b], a + 1j * b))

in_grid = lambda val: (0 <= val.real < len(x)) and (0 <= val.imag < len(x[0]))

antinodes = []
for antenna_type in set([a[0] for a in antennas]):
    for comb in combinations([a for a in antennas if a[0] == antenna_type[0]], 2):
        dist = comb[0][1] - comb[1][1]
        for n in range(50):  # input is 50x50, so 50 is enough
            if in_grid(comb[0][1] - dist * n):  # antinode for part 1 for n=2
                antinodes.append((comb[0][1] - dist * n, n == 2))
            if in_grid(comb[0][1] + dist * n):  # antinode for part 1 for n=1
                antinodes.append((comb[0][1] + dist * n, n == 1))


print(f"part 1: {len(set([a[0] for a in antinodes if a[1]]))}")
print(f"part 2: {len(set([a[0] for a in antinodes]))}")
