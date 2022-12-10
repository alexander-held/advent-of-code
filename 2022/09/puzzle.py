import fileinput
from math import copysign

x = [line.strip().split() for line in fileinput.input()]

pos_knots = [0j] * 10  # positions of all knots in complex coordinates
visited_p1, visited_p2 = set(), set()
for direction, nsteps in x:
    for _ in range(int(nsteps)):
        pos_knots[0] += {"R": 1, "L": -1, "U": 1j, "D": -1j}[direction]  # head moves

        for i in range(1, 10):  # update tails
            ds = pos_knots[i - 1] - pos_knots[i]  # distance to previous knot
            if abs(ds.real) + abs(ds.imag) > 2:  # diagonal move required
                pos_knots[i] += copysign(1, ds.real) + copysign(1, ds.imag) * 1j
            elif abs(ds) == 2:  # horizontal or vertical move by one unit
                pos_knots[i] += 0.5 * ds

            visited_p1.add(pos_knots[1])
            visited_p2.add(pos_knots[-1])

print(f"part 1: {len(visited_p1)}")
print(f"part 2: {len(visited_p2)}")
