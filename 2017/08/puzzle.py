import fileinput
from collections import defaultdict
from math import inf
from operator import eq, ge, gt, le, lt, ne


x = [line.strip() for line in fileinput.input()]

registers = defaultdict(lambda: 0)
comparisons = {">": gt, "<": lt, "==": eq, "!=": ne, ">=": ge, "<=": le}
max_val = -inf
for line in x:
    target, op, val, _, ref, comp, test_val = line.split()
    if comparisons[comp](registers[ref], int(test_val)):
        registers[target] += int(val) * (1 if op == "inc" else -1)
        max_val = max(max_val, registers[target])

print(f"part 1: {max(registers.values())}")
print(f"part 2: {max_val}")
