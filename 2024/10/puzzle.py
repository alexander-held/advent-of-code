import fileinput
from collections import defaultdict


x = [line.strip() for line in fileinput.input()]

topo_map = defaultdict(lambda: -1)
for a in range(len(x)):
    for b in range(len(x[0])):
        topo_map[a + 1j * b] = int(x[a][b])


def get_paths(pos, path):
    if topo_map[pos] == 9:
        return [path]
    paths = []
    for direc in [-1, -1j, +1, 1j]:
        if topo_map[pos + direc] == topo_map[pos] + 1:
            paths += get_paths(pos + direc, path + [pos + direc])
    return paths


score = 0
rating = 0
for start in [k for k, v in topo_map.items() if v == 0]:
    paths = get_paths(start, [])
    score += len(set(p[-1] for p in paths))
    rating += len(paths)

print(f"part 1: {score}")
print(f"part 2: {rating}")
