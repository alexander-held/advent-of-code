import fileinput
import json
from functools import cmp_to_key
from math import prod


x = "".join([line for line in fileinput.input()]).split("\n")


def cmp(l, r):
    # right order: -1, keep going: 0, wrong order: 1
    if isinstance(l, int) and isinstance(r, int):
        return -1 if l < r else (0 if l == r else 1)

    elif isinstance(l, list) and isinstance(r, list):
        for l_entry, r_entry in zip(l, r):
            if (res := cmp(l_entry, r_entry)) != 0:
                return res
        return -1 if len(l) < len(r) else (0 if len(l) == len(r) else 1)

    return cmp(l, [r]) if isinstance(l, list) else cmp([l], r)


ap = [json.loads(packet) for packet in x if packet.strip() != ""]  # all packets
p1 = sum([i + 1 for i in range(len(ap) // 2) if cmp(ap[i * 2], ap[i * 2 + 1]) == -1])
print(f"part 1: {p1}")

divider_packets = [[[2]], [[6]]]
sorted_packets = sorted(ap + divider_packets, key=cmp_to_key(cmp))
p2 = prod(sorted_packets.index(dp)+1 for dp in divider_packets)
print(f"part 2: {p2}")
