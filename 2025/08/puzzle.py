import fileinput
from itertools import combinations
from math import dist, prod

x = [list(map(int, line.split(","))) for line in fileinput.input()]

circuits = {(tuple(box),) for box in x}
for i, (b1, b2) in enumerate(sorted(combinations(x, 2), key=lambda d: dist(*d))):
    c1 = next(c for c in circuits if tuple(b1) in c)
    if tuple(b2) in c1:
        continue  # already in same circuit
    c2 = next(c for c in circuits if tuple(b2) in c)
    circuits = (circuits - {c1, c2}) | {c1 + c2}  # merge circuits
    if i + 1 == 1000:
        p1 = prod(sorted(len(c) for c in circuits)[-3:])
    if len(circuits) == 1:
        break

print(f"part 1: {p1}")
print(f"part 2: {b1[0]*b2[0]}")
