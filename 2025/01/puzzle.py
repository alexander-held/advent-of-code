import fileinput

x = [({"L": -1, "R": 1}[line[0]], int(line[1:])) for line in fileinput.input()]

pos = 50
p1 = 0
p2 = 0
for dir, nsteps in x:
    for _ in range(nsteps):
        pos = (pos + dir) % 100
        p2 += pos == 0

    p1 += pos == 0

print(f"part 1: {p1}")
print(f"part 2: {p2}")
