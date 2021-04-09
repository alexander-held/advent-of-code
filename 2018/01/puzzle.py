import fileinput
import itertools

x = [int(line.strip()) for line in fileinput.input()]

print(f"part 1: {sum(x)}")

freq = 0
seen = set()
for xi in itertools.cycle(x):
    freq += xi
    if freq in seen:
        print(f"part 2: {freq}")
        break
    seen.add(freq)
