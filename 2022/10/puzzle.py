import fileinput
from itertools import accumulate

x = [line.strip() for line in fileinput.input()]

# noop takes one cycle, equivalent to adding 0
# addx N takes two cycles, equivalent to adding 0 and then N
add_per_cycle = []
for instruction in x:
    if instruction.startswith("addx"):
        add_per_cycle += [0, int(instruction.split()[1])]
    else:
        add_per_cycle.append(0)

signal_strength_sum = 0
crt = ""
for i, register in enumerate(accumulate(add_per_cycle[:-1], initial=1)):
    crt += "⬜" if abs(register - i % 40) > 1 else "⬛"
    if (i + 1) % 40 == 0 and i > 0 and i:
        crt += "\n"  # next CRT line
    if (i + 1) % 40 == 20:
        signal_strength_sum += (i + 1) * register

print(f"\npart 1: {signal_strength_sum}")
print(f"part 2:\n{crt}")
