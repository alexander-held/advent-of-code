import fileinput
import collections

x = [line.strip() for line in fileinput.input()]

grid = collections.defaultdict(int)

for claim in x:
    x_pos, y_pos = map(int, claim.split("@")[-1].split(":")[0].split(","))
    dx, dy = map(int, claim.split(":")[-1].split("x"))
    for idx in range(dx):
        for idy in range(dy):
            grid[(x_pos + idx, y_pos + idy)] += 1

two_or_more = 0
for key, value in collections.Counter(grid).items():
    if value >= 2:
        two_or_more += 1
print(f"part 1: {two_or_more}")


# loop over claims and find the one where grid == 1 in the whole claim area
for claim in x:
    no_overlap = True
    x_pos, y_pos = map(int, claim.split("@")[-1].split(":")[0].split(","))
    dx, dy = map(int, claim.split(":")[-1].split("x"))
    for idx in range(dx):
        for idy in range(dy):
            if grid[(x_pos + idx, y_pos + idy)] != 1:
                no_overlap = False
    if no_overlap:
        print(f"part 2: {claim}")
