import fileinput
import re
from itertools import combinations, permutations, product

x = "|".join([line.strip() for line in fileinput.input()])

scanners_to_align = {}
for scanner_info in x.split("||"):
    scanner_id = int(re.search("\d+", scanner_info).group())
    coords = tuple(
        tuple(int(c) for c in coords[0].split(","))
        for coords in re.findall("((-?\d+,?){3})", scanner_info)
    )
    scanners_to_align.update({scanner_id: coords})


def get_offset_and_pos(reference_beacons, beacons_to_permute):
    # try out all possible orientations of next scanner to align it
    for perm in permutations([0, 1, 2], 3):
        for sign in product([-1, 1], repeat=3):
            # 48 permutations, but only 24 are needed: should add right hand rule
            permuted_beacons = tuple(
                (sign[0] * b[perm[0]], sign[1] * b[perm[1]], sign[2] * b[perm[2]])
                for b in beacons_to_permute
            )

            for ref_beacon in reference_beacons:
                for cur_beacon in permuted_beacons:
                    subtract_pos = lambda a, b: (a[0] - b[0], a[1] - b[1], a[2] - b[2])
                    add_pos = lambda a, b: (a[0] + b[0], a[1] + b[1], a[2] + b[2])
                    # calculate offset to reference, and align beacons to reference
                    offset = subtract_pos(ref_beacon, cur_beacon)
                    new_beacon_pos = [add_pos(b, offset) for b in permuted_beacons]
                    aligned = set(reference_beacons).intersection(set(new_beacon_pos))
                    if len(aligned) >= 12:
                        return offset, new_beacon_pos  # successful alignment
    return None, None


def align_scanner(aligned_scanner_info, to_align_info, seen, scanner_pos):
    # try pairs of aligned and unaligned scanners to align the next scanner
    for aligned_num, aligned_beacons in aligned_scanner_info.items():
        for num_to_align, beacons_to_align in to_align_info.items():
            if (aligned_num, num_to_align) in seen:
                continue  # already tried previously without success, can skip

            offset, beacon_pos = get_offset_and_pos(aligned_beacons, beacons_to_align)
            if offset:
                # found offset, now have new aligned scanner
                print(f"{num_to_align} can be aligned to {aligned_num} with {offset}")
                scanner_pos.update({num_to_align: offset})
                return num_to_align, beacon_pos, seen, scanner_pos
            else:
                seen.add((aligned_num, num_to_align))  # no match for combination


aligned_scanners = {0: scanners_to_align[0]}  # first scanner is reference
scanners_to_align.pop(0)
seen = set()  # keep track of combinations of aligned-unaligned that do not match
scanner_pos = {0: (0, 0, 0)}  # positions of scanners for part 2
while scanners_to_align:
    print("left to align:", list(scanners_to_align.keys()))
    align_info = align_scanner(aligned_scanners, scanners_to_align, seen, scanner_pos)
    num_aligned, beacon_pos, seen, scanner_pos = align_info  # extract info
    scanners_to_align.pop(num_aligned)  # one less scanner left to align
    aligned_scanners.update({num_aligned: beacon_pos})  # track aligned scanner

# get intersection of all beacons matched to each scanner
all_beacons = set(aligned_scanners[0])
for beacons in list(aligned_scanners.values())[1:]:
    all_beacons = all_beacons.union(beacons)

print(f"part 1: {len(all_beacons)}")  # takes ~2 min for input with CPython

manh = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])
print(f"part 2: {max([manh(a,b) for a,b in combinations(scanner_pos.values(), 2)])}")
