import fileinput
from functools import reduce
from operator import add, mul

x = [line.strip("\n") + " " for line in fileinput.input()]

col_pos = [idx for idx, c in enumerate(x[-1]) if c in "*+"] + [len(x[-1])]  # columns
total_p1 = 0
total_p2 = 0
for l, r in zip(col_pos[:-1], col_pos[1:]):
    op = {"+": add, "*": mul}[x[-1][l:r].strip()]
    total_p1 += reduce(op, [int(line[l:r]) for line in x[:-1]])  # left-to-right
    rtl = [int("".join(num)) for num in list(zip(*[line[l:r] for line in x[:-1]]))[:-1]]
    total_p2 += reduce(op, rtl)  # right-to-left version (using commutativity)

print(f"part 1: {total_p1}")
print(f"part 2: {total_p2}")
