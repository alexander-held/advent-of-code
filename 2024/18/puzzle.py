import fileinput
import heapq
from collections import defaultdict
from math import inf


x = [tuple(map(int, line.strip().split(","))) for line in fileinput.input()]


def find_path(start, end, bytes, num_bytes_fallen):  # Dijkstra's algorithm
    min_path_to_node = defaultdict(lambda: inf)
    priority_queue = []
    heapq.heappush(priority_queue, (0, *start))  # (len, x, y)

    while len(priority_queue):
        path_length, px, py = heapq.heappop(priority_queue)  # increasing length

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # adjacent nodes
            if (
                (0 <= px + dx <= end[0])
                and (0 <= py + dy <= end[1])
                and (px + dx, py + dy) not in bytes[:num_bytes_fallen]
            ):  # check if in bounds and no obstacle in the way
                path_next = path_length + 1
                if path_next < min_path_to_node[px + dx, py + dy]:
                    priority_queue.append((path_next, px + dx, py + dy))
                    min_path_to_node[px + dx, py + dy] = path_next  # new cheapest path

    return min_path_to_node[end]


bounds = [1024, len(x) + 1]
while bounds[0] + 1 != bounds[1]:  # bisect
    num_bytes = (bounds[0] + bounds[1]) // 2
    if find_path((0, 0), (70, 70), x, num_bytes) == inf:
        bounds = [bounds[0], num_bytes]
    else:
        bounds = [num_bytes, bounds[1]]

print(f"part 1: {find_path((0,0), (70, 70), x, 1024)}")
print(f"part 2: {x[bounds[0]][0]},{x[bounds[0]][1]}")
