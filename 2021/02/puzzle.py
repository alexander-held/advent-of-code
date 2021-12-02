import fileinput

x = [line.strip().split() for line in fileinput.input()]
x = [(a, int(b)) for a, b in x]

h = 0
d1 = 0

d2 = 0
a = 0

for direction, steps in x:
    if direction == "forward":
        h += steps
        d2 += a * steps
    elif direction == "down":
        d1 += steps
        a += steps
    elif direction == "up":
        d1 -= steps
        a -= steps

print(f"part 1: {h*d1}")
print(f"part 2: {h*d2}")
