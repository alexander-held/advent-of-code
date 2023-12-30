import fileinput
from itertools import count

x = [int(line) for line in fileinput.input()]


def jump(x, p2=False):
    idx = 0
    for i in count(0):
        if idx >= len(x):
            return i
        jump = x[idx]
        x[idx] += -1 if jump >= 3 and p2 else 1
        idx += jump


print(f"part 1: {jump(x.copy())}")
print(f"part 2: {jump(x.copy(), p2=True)}")
