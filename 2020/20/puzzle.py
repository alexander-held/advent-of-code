import fileinput
import collections
import re

x = "".join([line for line in fileinput.input()]).split("\n\n")
tile_dict = {}
for xi in x:
    tile_dict.update({xi.split(":")[0]: xi.split(":")[1].strip()})

tile_keys = list(tile_dict.keys())


def edge_to_binary_reps(edge):
    """binary representation of edge - edges are unique in input"""
    edge = edge.replace(".", "0").replace("#", "1")
    edge_forward = int(edge, 2)
    edge_reverse = int(edge[::-1], 2)
    # sort
    if edge_forward < edge_reverse:
        return (edge_forward, edge_reverse)
    else:
        return (edge_reverse, edge_forward)


def get_binary_edges(tile):
    """order: top, left, right, bottom"""
    top_edge = tile.split("\n")[0]
    top_edge_binary = edge_to_binary_reps(top_edge)

    left_edge = "".join([line[0] for line in tile.split("\n")])
    left_edge_binary = edge_to_binary_reps(left_edge)

    right_edge = "".join([line[-1] for line in tile.split("\n")])
    right_edge_binary = edge_to_binary_reps(right_edge)

    bottom_edge = tile.split("\n")[-1]
    bottom_edge_binary = edge_to_binary_reps(bottom_edge)

    return top_edge_binary, left_edge_binary, right_edge_binary, bottom_edge_binary


tile_dict_binary = {}
for tk in tile_keys:
    binary_edges = get_binary_edges(tile_dict[tk])
    tile_dict_binary.update({tk: binary_edges})

all_edges = []
for tile in tile_dict_binary.values():
    all_edges += [tile[0], tile[1], tile[2], tile[3]]
counter = collections.Counter(tuple(all_edges))


# count how many edges of a given tile match other tiles
prod_corners = 1
corner_ids = []
for tk in tile_keys:
    sum_neighbors = 0
    for edge in tile_dict_binary[tk]:
        if counter[edge] == 2:
            sum_neighbors += 1
    if sum_neighbors == 2:
        prod_corners *= int(tk.split()[-1])
        corner_ids.append(tk)

print(f"part 1: {prod_corners}")


def flip(tile):
    """vertical mirror (left <-> right)"""
    flipped_tile = "\n".join([line[::-1] for line in tile.split("\n")])
    return flipped_tile


def rotate(tile):
    """rotate clockwise 90 degrees"""
    lines = tile.split("\n")
    columns = [[c for c in l] for l in lines]
    for i, l in enumerate(lines):
        for j in range(len(lines)):
            columns[j][i] = l[j]
    columns = "\n".join(["".join(c) for c in columns])
    return flip(columns)


# pick a single corner and start with it on the top left
# need to rotate / flip such that left edge and top edge are unique
CORNER_START = 0
first_corner = tile_dict[corner_ids[CORNER_START]]

# keep track of all tiles that are already used and not available anymore
tile_keys_remaining = tile_keys.copy()
tile_keys_remaining.pop(tile_keys_remaining.index(corner_ids[CORNER_START]))


def permutate_until_both_unique(tile):
    """make top and left edge unique"""
    while True:
        # rotate until top edge is unique
        if counter[get_binary_edges(tile)[0]] == 1:
            break
        else:
            tile = rotate(tile)

    if counter[get_binary_edges(tile)[1]] != 1:
        tile = flip(tile)  # flip along vertical axis if left edge is not unique

    return tile


# permutate until top and left edges are unique, then the piece is correctly oriented
first_corner = permutate_until_both_unique(first_corner)

# make a grid to put solved tiles in
GRID_LEN = int(len(x) ** 0.5)
TILE_LEN = len(first_corner.split("\n")[0])
placeholder_tile = "".join(["".join(["/" * TILE_LEN + "\n"]) * TILE_LEN])
grid = [[placeholder_tile] * GRID_LEN for _ in range(GRID_LEN)]
grid[0][0] = first_corner  # put correctly oriented tile in the grid


def print_grid(grid):
    """visualize grid for debugging"""
    for i_row in range(GRID_LEN):
        for tile_row in range(TILE_LEN):
            for j_col in range(GRID_LEN):
                tile_rows = grid[i_row][j_col].split("\n")
                print("".join(tile_rows[tile_row]), end=" ")
            print()
        print()


def find_matching(edges_needed, tile_keys_remaining):
    """find tile that contains given edges, remove id from list of remaining ids"""
    for tk in tile_keys_remaining:
        edges = tile_dict_binary[tk]
        if all([e in edges for e in edges_needed]):  # found match
            tile_keys_remaining.pop(tile_keys_remaining.index(tk))
            return tk, tile_keys_remaining


def permutate_until_left_matches_top_unique(tile, left_edge_req):
    """match left edge, make top edge unique"""
    while True:
        # rotate until left edge matches requirement
        if get_binary_edges(tile)[1] == left_edge_req:
            break
        else:
            tile = rotate(tile)

    if counter[get_binary_edges(tile)[0]] != 1:
        # flip along horizontal axis if top edge is not unique
        tile = flip(rotate(rotate(tile)))

    return tile


def permutate_until_top_matches_left_unique(tile, top_edge_req):
    """match top edge, make left edge unique"""
    while True:
        # rotate until top edge matches requirement
        if get_binary_edges(tile)[0] == top_edge_req:
            break
        else:
            tile = rotate(tile)

    if counter[get_binary_edges(tile)[1]] != 1:
        tile = flip(tile)  # flip along vertical axis if left edge is not unique

    return tile


def permutate_until_left_top_match(tile, top_edge_req, left_edge_req):
    """match top and left edges"""
    while True:
        # rotate until top edge matches requirement
        if get_binary_edges(tile)[0] == top_edge_req:
            break
        else:
            tile = rotate(tile)

    if get_binary_edges(tile)[1] != left_edge_req:
        tile = flip(tile)  # flip along vertical axis if left edge does not match

    return tile


# fill first row with tiles, matching edge with tile to the left
I_ROW = 0
for j_col in range(1, GRID_LEN):
    previous_tile = grid[I_ROW][j_col - 1]
    right_edge_prev = get_binary_edges(previous_tile)[2]
    # find next tile that contains right edge from previous tile
    next_id, tile_keys_remaining = find_matching([right_edge_prev], tile_keys_remaining)
    next_tile = tile_dict[next_id]
    next_tile = permutate_until_left_matches_top_unique(next_tile, right_edge_prev)
    grid[I_ROW][j_col] = next_tile


# fill left column with tiles, matching edge with tile on top
J_COL = 0
for i_row in range(1, GRID_LEN):
    previous_tile = grid[i_row - 1][J_COL]
    bottom_edge_prev = get_binary_edges(previous_tile)[3]
    # find next tile that contains bottom edge from previous tile
    next_id, tile_keys_remaining = find_matching(
        [bottom_edge_prev], tile_keys_remaining
    )
    next_tile = tile_dict[next_id]
    next_tile = permutate_until_top_matches_left_unique(next_tile, bottom_edge_prev)
    grid[i_row][J_COL] = next_tile


# fill remaining rows and columns, matching edges with tiles on top and to the left
for i_row in range(1, GRID_LEN):
    for j_col in range(1, GRID_LEN):
        left_tile = grid[i_row][j_col - 1]
        top_tile = grid[i_row - 1][j_col]
        right_edge_prev = get_binary_edges(left_tile)[2]
        bottom_edge_prev = get_binary_edges(top_tile)[3]
        # find next tile that contains both required edges
        next_id, tile_keys_remaining = find_matching(
            [right_edge_prev, bottom_edge_prev], tile_keys_remaining
        )
        next_tile = tile_dict[next_id]
        next_tile = permutate_until_left_top_match(
            next_tile, bottom_edge_prev, right_edge_prev
        )
        grid[i_row][j_col] = next_tile


def grid_as_tile(grid):
    """turn grid without the tile edges into one big tile"""
    tile = ""
    for i_row in range(GRID_LEN):
        for tile_row in range(1, TILE_LEN - 1):
            for j_col in range(GRID_LEN):
                tile_rows = grid[i_row][j_col].split("\n")
                tile += "".join(tile_rows[tile_row][1:-1])
            tile += "\n"
    return tile.strip()


# now the grid is solved, convert it to a single tile for further processing
grid_tile = grid_as_tile(grid)

# try out all 8 possible tile permutations to find correct orientation
for i in range(8):
    grid_tile = rotate(grid_tile)
    if i == 4:
        grid_tile = flip(grid_tile)

    # sea monster regex
    # need to account for overlapping matches https://stackoverflow.com/a/5616910
    sea_monster_top = r"(?=(..................\#.))"
    sea_monster_mid = r"(?=(\#....\#\#....\#\#....\#\#\#))"
    sea_monster_bottom = r"(?=(.\#..\#..\#..\#..\#..\#...))"

    sea_monsters = 0
    lines = grid_tile.split("\n")
    for i, line in enumerate(lines):
        if i == 0 or i == len(lines) - 1:
            continue  # skip first and last line, looking for middle of sea monster
        top = re.compile(sea_monster_top)
        mid = re.compile(sea_monster_mid)
        bottom = re.compile(sea_monster_bottom)
        for match_mid in mid.finditer(line):
            for match_bottom in bottom.finditer(lines[i + 1]):
                for match_top in top.finditer(lines[i - 1]):
                    if match_mid.start() == match_bottom.start() == match_top.start():
                        sea_monsters += 1  # all matches coincide

    if sea_monsters == 0:
        continue  # no sea monsters found, try next grid permutation

    # count "#" that are not part of sea monsters, subtract 15 per sea monster
    sol = collections.Counter(grid_tile)["#"] - sea_monsters * 15
    print(f"part 2: {sea_monsters} sea monsters, solution: {sol}")
