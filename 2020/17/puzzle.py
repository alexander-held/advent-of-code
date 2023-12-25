import collections
import fileinput

x = [line.strip() for line in fileinput.input()]


def count_neighbors(x, y, z, w, grid, part2):
    neighbors = 0
    wi_vals = [-1, 0, 1] if part2 else [0]
    for xi in [-1, 0, 1]:
        for yi in [-1, 0, 1]:
            for zi in [-1, 0, 1]:
                for wi in wi_vals:
                    if not (xi == yi == zi == wi == 0):
                        neighbors += grid.get((x+xi, y+yi, z+zi, w+wi), False)
    return neighbors


def update_grid(grid, part2=False):
    x_range = (min([v[0] for v in grid.keys()])-1, max([v[0] for v in grid.keys()])+2)
    y_range = (min([v[1] for v in grid.keys()])-1, max([v[1] for v in grid.keys()])+2)
    z_range = (min([v[2] for v in grid.keys()])-1, max([v[2] for v in grid.keys()])+2)
    w_range = (min([v[3] for v in grid.keys()])-1, max([v[3] for v in grid.keys()])+2)
    if not part2:
        w_range = (0, 1)
    new_grid = {}
    for x in range(*x_range):
        for y in range(*y_range):
            for z in range(*z_range):
                for w in range(*w_range):
                    cn = count_neighbors(x, y, z, w, grid, part2=part2)
                    field_active = grid.get((x, y, z, w), False)
                    if field_active and ((cn < 2) or (cn > 3)):
                        # become inactive if not exactly 2 or 3 active neighbors
                        new_grid.update({(x, y, z, w): False})
                    elif (not field_active) and (cn == 3):
                        # activate for exactly 3 active neighbors
                        new_grid.update({(x, y, z, w): True})
                    elif field_active:
                        # stay active
                        new_grid.update({(x, y, z, w): True})
    return new_grid


# create initial grid
orig_grid = {}
z = 0
w = 0
for x, row in enumerate(x):
    for y, field in enumerate(list(row)):
        if field == "#":
            orig_grid.update({(x, y, z, w): True})


# part 1
n_cycles = 6
grid = orig_grid.copy()
for _i in range(n_cycles):
    grid = update_grid(grid, part2=False)
    n_active = collections.Counter(grid.values())[True]
print(f"part 1, cycle {_i+1}, active: {n_active}")


# part 2
grid = orig_grid.copy()
for _i in range(n_cycles):
    grid = update_grid(grid, part2=True)
    n_active = collections.Counter(grid.values())[True]
print(f"part 2, cycle {_i+1}, active: {n_active}")
