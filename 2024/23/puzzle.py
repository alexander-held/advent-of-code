import fileinput
from collections import defaultdict

x = [line.strip() for line in fileinput.input()]

connected = defaultdict(set)
for line in x:
    c1, c2 = line.split("-")
    connected[c1].add(c2)
    connected[c2].add(c1)

triplets = set()
for c1 in connected.keys():
    for c2 in connected[c1] - {c1}:
        for c3 in connected[c1] & connected[c2] - {c1, c2}:
            if any(c.startswith("t") for c in (c1, c2, c3)):
                triplets.add(tuple(sorted([c1, c2, c3])))


def bron_kerbosch(r, p, x):
    # see https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
    if not p and not x:
        yield r
    for comp in p:
        yield from bron_kerbosch(r | {comp}, p & connected[comp], x & connected[comp])
        p = p - {comp}
        x |= {comp}


cliques = [clique for clique in bron_kerbosch(set(), set(connected.keys()), set())]
lengths = [len(c) for c in cliques]

print(f"part 1: {len(triplets)}")
print(f"part 2: {','.join(sorted(cliques[lengths.index(max(lengths))]))}")
