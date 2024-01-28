import fileinput
from functools import reduce
from itertools import cycle
from operator import xor

x = [line.strip() for line in fileinput.input()][0]


def knot_hash(hash_input):  # adapted from day 10
    lengths = [ord(v) for v in hash_input] + [17, 31, 73, 47, 23]
    num_list = [i for i in range(256)]
    idx_list = cycle(num_list)  # keeps track of position
    skip = 0
    for length in lengths * 64:
        idx_to_reverse = [next(idx_list) for _ in range(length)]  # affected indices
        reverse = [num_list[idx] for idx in idx_to_reverse][::-1]  # reverse section

        for idx, new_val in zip(idx_to_reverse, reverse):
            num_list[idx] = new_val

        for _ in range(skip):
            next(idx_list)  # skip, iteration already moved by length

        skip += 1

    batches = [reduce(xor, num_list[i * 16 : (i + 1) * 16]) for i in range(16)]
    return "".join(f"{v:>02x}" for v in batches)


num_used_squares = 0
grid = dict()
for i in range(128):
    bin_hash = f"{int(''.join(knot_hash(f'{x}-{i}')), 16):>0128b}"
    num_used_squares += sum(ch == "1" for ch in bin_hash)
    for j in range(128):
        grid[i + 1j * j] = int(bin_hash[j])


def find_region(active, in_region, remaining):
    for offset in [-1, +1j, 1, -1j]:
        if active + offset in remaining:
            in_region.add(active + offset)  # neighbor is in region
            # also add neighbors of neighbor
            in_region &= find_region(active + offset, in_region, remaining - in_region)
    return in_region


num_regions = 0
remaining = set([k for k, v in grid.items() if v == 1])  # grid sites with used squares
while len(remaining):
    active = remaining.pop()  # site for which to find neighbors
    num_regions += 1
    neighbors = find_region(active, {active}, remaining)
    remaining -= neighbors  # remove all sites that are part of this region

print(f"part 1: {num_used_squares}")
print(f"part 2: {num_regions}")
