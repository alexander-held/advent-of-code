import fileinput

cubes = set(tuple(map(int, line.split(","))) for line in fileinput.input())

offsets = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
neighbors = lambda x, y, z: [(x + o[0], y + o[1], z + o[2]) for o in offsets]

# surface area: count all neighboring cubes that are not in list of cubes
surface = sum(sum(n not in cubes for n in neighbors(*cube)) for cube in cubes)
print(f"part 1: {surface}")

# visit all positions in a [-1, 20] cube to determine accessible surface positions
pos_to_visit = [(-1, -1, -1)]  # start at outside
seen = set()
while pos_to_visit:
    current = pos_to_visit.pop()
    for n in neighbors(*current):
        if n not in seen and n not in cubes and all([-1 <= c <= 20 for c in n]):
            pos_to_visit.append(n)
    seen.add(current)

# surface area: all neighbors of cubes that are accessible from the outside
surface_p2 = sum(sum(n in seen for n in neighbors(*cube)) for cube in cubes)
print(f"part 2: {surface_p2}")
