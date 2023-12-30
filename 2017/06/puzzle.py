import fileinput
from itertools import count

x = [list(map(int, line.split())) for line in fileinput.input()][0]

seen = dict()
for i_cycle in count(1):
    idx = x.index(max(x))
    num_blocks = x[idx]
    x[idx] = 0  # remove all blocks
    for offset in range(num_blocks):
        x[(idx + offset + 1) % len(x)] += 1  # redistribute
    if tuple(x) in seen.keys():
        break  # cycle detected
    seen[tuple(x)] = i_cycle

print(f"part 1: {i_cycle}")
print(f"part 2: {i_cycle - seen[tuple(x)]}")
