import fileinput
import heapq
from collections import defaultdict
from math import inf


x = [line.strip() for line in fileinput.input()]

grid = dict()
for a in range(len(x)):
    for b in range(len(x[0])):
        grid[a + 1j * b] = x[a][b]


def explore(grid):  # Dijkstra's algorithm, see e.g. 2021 day 15
    start = next(k for k, v in grid.items() if v == "S")
    end = next(k for k, v in grid.items() if v == "E")
    min_score_to_node = defaultdict(lambda: inf)
    paths_to_end = defaultdict(set)  # score: places along path for part 2
    priority_queue = []
    # use real numbers for heapq: score, pos_x, pos_y, direction, path x/y
    heapq.heappush(
        priority_queue, (0, start.real, start.imag, 1, [(start.real, start.imag)])
    )

    while len(priority_queue):  # iterate in order of increasing risk
        node_score, pos_x, pos_y, direc, path = heapq.heappop(priority_queue)
        direc_complex = {1: 1j, 2: 1, 3: -1j, 4: -1}[direc]  # E / S / W / N

        # turn up to three times and then move forward
        for turn, num_turns in ((1, 0), (-1j, 1), (-1, 2), (1j, 1)):
            pos_next = pos_x + 1j * pos_y + direc_complex * turn
            direc_next = {1j: 1, 1: 2, -1j: 3, -1: 4}[direc_complex * turn]  # to real
            if grid[pos_next] in ".E":  # can move
                score_next = node_score + 1000 * num_turns + 1
                if score_next <= min_score_to_node[pos_next, direc_next]:
                    priority_queue.append(
                        (
                            score_next,
                            pos_next.real,
                            pos_next.imag,
                            direc_next,
                            path + [(pos_next.real, pos_next.imag)],
                        )
                    )
                    min_score_to_node[pos_next, direc_next] = score_next  # lowest score
                    if grid[pos_next] == "E":
                        paths_to_end[score_next] |= set(path)  # excluding end itself

    return min(min_score_to_node[end, d] for d in range(1, 5)), paths_to_end


min_score, paths_to_end = explore(grid)

print(f"part 1: {min_score}")
print(f"part 2: {len(paths_to_end[min(paths_to_end.keys())]) + 1}")
