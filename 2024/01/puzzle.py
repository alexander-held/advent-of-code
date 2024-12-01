import fileinput
from collections import Counter
import numpy as np

x = np.asarray([list(map(int, line.split())) for line in fileinput.input()])
stack = np.vstack([sorted(x[:, 0]), sorted(x[:, 1])])

c = Counter(stack[1])
sim = 0
for num in stack[0]:
    sim += num * c[num]

print(f"part 1: {sum(abs(stack[0] - stack[1]))}")
print(f"part 2: {sim}")
