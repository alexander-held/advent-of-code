import fileinput
import heapq
from collections import defaultdict
from math import inf

x = [line.strip() for line in fileinput.input()]

loss_map = {}
for y_pos in range(len(x)):
    for x_pos in range(len(x[0])):
        loss_map[x_pos, y_pos] = int(x[y_pos][x_pos])


def explore(loss_map, p2=False):
    # Dijkstra's algorithm, adapted from 2021 day 15
    priority_queue = []
    # queue with (heat loss, pos x & y, number of straight moves, last direction x & y)
    heapq.heappush(priority_queue, (0, 0, 0, 0, (0, 0)))
    # need to also keep track of number of straight moves and direction for best paths
    min_loss = defaultdict(lambda: inf)

    while len(priority_queue):
        # explore in increasing heat loss
        heat_loss, px, py, n_straight, (lx, ly) = heapq.heappop(priority_queue)

        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:  # up, right, down, left
            if p2 and n_straight < 4 and ((dx, dy) != (lx, ly) and (lx, ly) != (0, 0)):
                continue  # need to go at least four times straight

            n_straight_next = n_straight + 1 if (dx, dy) == (lx, ly) else 1
            if n_straight_next > (3 if not p2 else 10):
                continue  # can only go straight three / ten times in a row

            if (dx and (dx, dy) == (-lx, ly)) or (dy and (dx, dy) == (lx, -ly)):
                continue  # can not go backwards

            if not (0 <= px + dx < len(x[0]) and 0 <= py + dy < len(x)):
                continue  # out of bounds

            heat_loss_next = heat_loss + loss_map[px + dx, py + dy]
            if heat_loss_next < min_loss[px + dx, py + dy, n_straight_next, dx, dy]:
                priority_queue.append(
                    (heat_loss_next, px + dx, py + dy, n_straight_next, (dx, dy))
                )
                min_loss[px + dx, py + dy, n_straight_next, dx, dy] = heat_loss_next

    for k, loss in min_loss.items():
        if (k[0], k[1]) == (len(x[0]) - 1, len(x) - 1):  # at target
            if not p2 or k[2] >= 4:  # able to stop in time
                return loss


print(f"part 1: {explore(loss_map)}")
print(f"part 2: {explore(loss_map, p2=True)}")
