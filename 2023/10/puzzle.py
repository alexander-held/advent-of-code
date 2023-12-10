import fileinput
from collections import defaultdict


# use better characters https://en.wikipedia.org/wiki/Box-drawing_character
trans = str.maketrans({"|": "║", "-": "═", "F": "╔", "7": "╗", "J": "╝", "L": "╚"})
x = [str.translate(line.strip(), trans) for line in fileinput.input()]

pipe_map = defaultdict(lambda: ".")
for y_pos in range(len(x)):
    for x_pos in range(len(x[0])):
        pipe_map.update({x_pos + 1j * y_pos: x[y_pos][x_pos]})


def get_neighbors(pipe_map, pos):
    # available pipies: ║ ═ ╔ ╗ ╝ ╚
    # up, right, left, down: (-1j, 1, 1j, -1)
    # directions to check given current pipe type
    dirs_to_check = {
        "S": (-1j, 1, 1j, -1),
        "║": (-1j, 1j),
        "═": (-1, 1),
        "╔": (1, 1j),
        "╗": (1j, -1),
        "╝": (-1j, -1),
        "╚": (-1j, 1),
    }
    # pipes in neighboring field that can form connection, given direction of neighbor
    connecting_targets = {-1j: "║╔╗S", 1: "═╗╝S", 1j: "║╝╚S", -1: "═╔╚S"}
    neighbors = set()
    for direction in dirs_to_check[pipe_map[pos]]:
        if pipe_map[pos + direction] in connecting_targets[direction]:
            neighbors.add(pos + direction)
    return neighbors


s_pos = [k for k, v in pipe_map.items() if v == "S"][0]
pos_1, pos_2 = get_neighbors(pipe_map, s_pos)
seen_1, seen_2 = {s_pos, pos_1}, {s_pos, pos_2}
num_steps = 1
# simultaneously go along pipe in both directions until finding second common position
while len(seen_1 & seen_2) == 1:
    pos_1 = (get_neighbors(pipe_map, pos_1) - seen_1).pop()  # always pick unseen field
    seen_1.add(pos_1)
    pos_2 = (get_neighbors(pipe_map, pos_2) - seen_2).pop()
    seen_2.add(pos_2)
    num_steps += 1

print(f"part 1: {num_steps}")

# replace S in map with the proper pipe character given the neighbors it has
dirs = [n - s_pos for n in get_neighbors(pipe_map, s_pos)]
possible_s_repl = {-1j: "║╝╚", 1: "═╔╚", 1j: "║╔╗", -1: "═╗╝"}
pipe_map[s_pos] = (set(possible_s_repl[dirs[0]]) & set(possible_s_repl[dirs[1]])).pop()

seen_all = seen_1 | seen_2
num_enclosed = 0
for pos in pipe_map.keys():  # can contain out-of-bounds entries, but no pipes there
    if pos in seen_all:
        continue
    # look towards the top and count blocking pipes, including those with vertical
    # connection to the left (can count left or right here), odd number -> enclosed
    pipes_in_the_way = 0
    for y_pos in range(0, int(pos.imag)):
        scan_pos = pos.real + 1j * y_pos
        if scan_pos in seen_all and pipe_map[scan_pos] in "═╝╗":
            pipes_in_the_way += 1
    if pipes_in_the_way % 2:
        num_enclosed += 1

print(f"part 2: {num_enclosed}")
