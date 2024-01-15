import fileinput
from collections import defaultdict

x = [line.strip() for line in fileinput.input()]

connection_map = defaultdict(lambda: set())
for line in x:
    start, targets = line.split(" <-> ")
    targets = set(map(int, targets.split(", ")))
    connection_map[int(start)] = connection_map[int(start)] | targets


def find_connected(node, connection_map, seen):
    for target in connection_map[node]:
        if target not in seen:
            seen |= find_connected(target, connection_map, seen | {target})
    return seen


print(f"part 1: {len(find_connected(0, connection_map, set()))}")

num_groups = 0
remaining_nodes = set(connection_map.keys())
while len(remaining_nodes):
    node = remaining_nodes.pop()  # take a new node that is not part of a group
    group = find_connected(node, connection_map, set())
    remaining_nodes -= group  # remove everything connected to it from remaining nodes
    num_groups += 1

print(f"part 2: {num_groups}")
