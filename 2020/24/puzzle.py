import fileinput

x = [line.strip() for line in fileinput.input()]


def get_next_step(instructions):
    if instructions[0] == "s" or instructions[0] == "n":
        return instructions[0:2], instructions[2:]
    else:
        return instructions[0], instructions[1:]


black_tiles = set()
for instructions in x:
    pos = [0, 0]
    while instructions != "":
        next_step, instructions = get_next_step(instructions)
        if "n" in next_step:
            pos[1] += 1
        elif "s" in next_step:
            pos[1] -= 1
        if next_step == "e":
            pos[0] += 1
        elif next_step == "w":
            pos[0] -= 1
        elif next_step == "ne" or next_step == "se":
            pos[0] += 0.5
        elif next_step == "nw" or next_step == "sw":
            pos[0] -= 0.5
    pos = tuple(pos)
    if pos in black_tiles:
        black_tiles.remove(pos)
    else:
        black_tiles.add(pos)

print(f"part 1: {len(black_tiles)}")

adj_dirs = [(1, 0), (-1, 0), (0.5, 1), (-0.5, 1), (0.5, -1), (-0.5, -1)]


def update_grid(grid):
    tiles_to_check = set()
    for x, y in grid:
        tiles_to_check.add((x, y))  # check black tiles
        # check tiles adjacent to black
        tiles_to_check.update([(x + adj[0], y + adj[1]) for adj in adj_dirs])

    next_grid = set()
    for x, y in tiles_to_check:
        n_adj = sum([(x + adj[0], y + adj[1]) in grid for adj in adj_dirs])
        if (x, y) not in grid and n_adj == 2:
            next_grid.add((x, y))  # tile becomes black
        elif (x, y) in grid and (0 < n_adj <= 2):
            next_grid.add((x, y))  # tile stays black

    return next_grid


for _ in range(100):
    black_tiles = update_grid(black_tiles)
print(f"part 2: {len(black_tiles)}")
