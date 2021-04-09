import fileinput
import collections

x = [line.strip() for line in fileinput.input()]

two_times = 0
three_times = 0
for line in x:
    counter = collections.Counter(line)
    two_times += 2 in counter.values()
    three_times += 3 in counter.values()
print(f"part 1: {two_times*three_times}")

for i in range(len(x[0])):
    # remove single character
    x_copy = ["".join([xii for j, xii in enumerate(xi) if j != i]) for xi in x]
    counter = collections.Counter(x_copy)
    for key, value in counter.items():
        if value == 2:
            print(f"part 2: {key}")
