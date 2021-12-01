import fileinput

x = [int(line.strip()) for line in fileinput.input()]

count = sum(b > a for a, b in zip(x[:-1], x[1:]))
print(f"part 1: {count}")

count = sum(sum(x[i + 1 : i + 4]) > sum(x[i : i + 3]) for i in range(0, len(x) - 3))
print(f"part 2: {count}")
