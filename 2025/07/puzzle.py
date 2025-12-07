import fileinput
from collections import defaultdict

x = [line.strip() for line in fileinput.input()]

num_split = 0
pos = {x[0].find("S"): 1}
for line in x[1:]:
    pos_next = defaultdict(int)
    for p, num in pos.items():
        if line[int(p)] == "^":
            num_split += 1
            pos_next[p - 1] += num
            pos_next[p + 1] += num
        else:
            pos_next[p] += num
    pos = pos_next

print(f"part 1: {num_split}")
print(f"part 2: {sum(pos.values())}")
