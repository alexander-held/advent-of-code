import fileinput
import heapq
import math
from collections import defaultdict

x = [[int(risk) for risk in line.strip()] for line in fileinput.input()]

LEN_I = len(x)
LEN_J = len(x[0])


def get_risk(i: int, j: int, part2: bool = False):
    if not part2:
        return x[i][j]
    else:
        return (x[i % LEN_I][j % LEN_J] + i // LEN_I + j // LEN_J) % 9 or 9


def explore(len_i: int, len_j: int, part2: bool = False):
    # Dijkstra's algorithm
    min_risk_to_node = defaultdict(lambda: math.inf)
    priority_queue = []
    heapq.heappush(priority_queue, (0, 0, 0))  # (cost, i, j), start with 0 risk at 0,0

    while len(priority_queue):
        node_risk, i, j = heapq.heappop(priority_queue)  # explore in increasing risk

        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # adjacent nodes
            if (0 <= i + di <= len_i - 1) and (0 <= j + dj <= len_j - 1):  # in bounds
                # total risk at new node is current risk + next risk
                risk_next = node_risk + get_risk(i + di, j + dj, part2=part2)
                if risk_next < min_risk_to_node[i + di, j + dj]:
                    priority_queue.append((risk_next, i + di, j + dj))
                    min_risk_to_node[i + di, j + dj] = risk_next  # new cheapest path
    return min_risk_to_node[(len_i - 1, len_j - 1)]


print(f"part 1: {explore(LEN_I, LEN_J)}")
print(f"part 2: {explore(LEN_I * 5, LEN_J * 5, part2=True)}")
