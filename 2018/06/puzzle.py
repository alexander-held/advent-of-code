import fileinput
from collections import Counter
from math import inf

x = [tuple(map(int, line.strip().split(","))) for line in fileinput.input()]

MIN_X = min(p[0] for p in x)
MAX_X = max(p[0] for p in x)
MIN_Y = min(p[1] for p in x)
MAX_Y = max(p[1] for p in x)


def closest_and_total_distance(px, py, threshold=10000):
    dist_min = inf
    dist_total = 0  # total distance for part 2
    for pos in x:
        dist = abs(px - pos[0]) + abs(py - pos[1])
        dist_total += abs(px - pos[0]) + abs(py - pos[1])
        if dist < dist_min:
            dist_min = dist
            closest_pos = pos
        elif dist == dist_min:
            closest_pos = (inf, inf)  # tie, does not count (can still get lower after)
    return closest_pos, dist_total < threshold


counter_small = Counter()  # counts areas within bounding box
counter_large = Counter()  # counts areas within sightly larger bounding box
points_within_region = 0  # counter for part 2
for px in range(MIN_X - 1, MAX_X + 2):
    for py in range(MIN_Y - 1, MAX_Y + 2):
        closest, within_region = closest_and_total_distance(px, py, threshold=10000)
        points_within_region += within_region
        if MIN_X <= px <= MAX_X and MIN_Y <= py <= MAX_Y:
            counter_small[closest] += 1
        counter_large[closest] += 1

set_small = set()  # set of area sizes
for pos, counts in counter_small.most_common():
    if pos == (inf, inf) or pos[0] in [MIN_X, MAX_X] or pos[1] in [MIN_Y, MAX_Y]:
        continue  # closest distance is tied, points at the edge lie in infinite areas
    set_small.add(counts)

set_large = set()
for pos, counts in counter_large.most_common():
    if pos == (inf, inf) or pos[0] in [MIN_X, MAX_X] or pos[1] in [MIN_Y, MAX_Y]:
        continue  # closest distance is tied, points at the edge lie in infinite areas
    set_large.add(counts)

# take largest element of intersection to solve part 1, this drops infinite areas
print(f"part 1: {max(set_small.intersection(set_large))}")
print(f"part 2: {points_within_region}")
