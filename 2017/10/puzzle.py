import fileinput
from functools import reduce
from itertools import cycle
from operator import xor

x = [line.strip() for line in fileinput.input()][0]


def knot_hash(lengths, num_rounds=1):
    num_list = [i for i in range(256)]
    idx_list = cycle(num_list)  # keeps track of position
    skip = 0
    for length in lengths * num_rounds:
        idx_to_reverse = [next(idx_list) for _ in range(length)]  # affected indices
        reverse = [num_list[idx] for idx in idx_to_reverse][::-1]  # reverse section

        for idx, new_val in zip(idx_to_reverse, reverse):
            num_list[idx] = new_val

        for _ in range(skip):
            next(idx_list)  # skip, iteration already moved by length

        skip += 1

    return num_list


num_list = knot_hash(list(map(int, x.split(","))))
print(f"part 1: {num_list[0]*num_list[1]}")

sparse_hash = knot_hash([ord(v) for v in x] + [17, 31, 73, 47, 23], num_rounds=64)
batches = [reduce(xor, sparse_hash[i * 16 : (i + 1) * 16]) for i in range(16)]
print(f"part 2: {''.join(f'{v:>02x}' for v in batches)}")
