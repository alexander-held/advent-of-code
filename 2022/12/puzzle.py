import fileinput
from collections import defaultdict, deque
from math import inf

x = [line.strip() for line in fileinput.input()]

map = defaultdict(lambda: chr(0))  # lower than anything else for edges of map
for pos_y, line in enumerate(x):
    for pos_x, char in enumerate(line):
        pos = pos_x + 1j * pos_y
        if char == "S":
            start = pos
            char = "a"
        elif char == "E":
            end = pos
            char = "z"
        map.update({pos: char})


def get_possible_moves(map, pos):
    possible_moves = []
    for direction in [1, -1, 1j, -1j]:
        if ord(map[pos]) - ord(map[pos + direction]) <= 1:
            # move down by at most one level (can only go up one in forward direction)
            possible_moves.append(direction)
    return possible_moves


def explore(map, starting_position):  # breadth-first search
    min_cost_to_node = defaultdict(lambda: inf)  # lowest cost to node
    nodes_to_explore = deque([(starting_position, 0)])  # position and cost

    while len(nodes_to_explore):
        pos, cost = nodes_to_explore.popleft()

        for move in get_possible_moves(map, pos):
            cost_next = cost + 1
            pos_next = pos + move
            if cost_next < min_cost_to_node[pos_next]:
                nodes_to_explore.append((pos_next, cost_next))
                min_cost_to_node[pos_next] = cost_next

    return min_cost_to_node


costs = explore(map, end)  # start exploring from the end
min_cost = min(costs[pos_of_a] for pos_of_a in [k for k, v in map.items() if v == "a"])

print(f"part 1: {costs[start]}")
print(f"part 2: {min_cost}")
