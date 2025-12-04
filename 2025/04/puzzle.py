import fileinput

x = [line.strip() for line in fileinput.input()]
grid = {i + 1j * j for i, l in enumerate(x) for j in range(len(l)) if l[j] == "@"}

direcs = (-1 - 1j, -1, -1 + 1j, -1j, 0, 1j, 1 - 1j, 1, 1 + 1j)
removed = []
while (not removed) or (removed[-1] != 0):
    to_rm = {paper for paper in grid if sum(paper + d not in grid for d in direcs) >= 5}
    removed.append(len(to_rm))
    grid -= to_rm

print(f"part 1: {removed[0]}")
print(f"part 2: {sum(removed)}")
