import fileinput
import re


x = [line for line in fileinput.input()]

seeds = list(map(int, x[0].split()[1:]))
almanac = {}
matches = re.findall(r"(\w+-\w+-\w+) map:\n((?:\d+ \d+ \d+\n)+)", "".join(x))
for match in matches:
    source, dest = match[0].replace("-to-", "-").split("-")
    almanac.update(
        {source: {"dest": dest, "dest_pos": [], "source_pos": [], "lens": []}}
    )
    for line in [list(map(int, m.split())) for m in match[1].split("\n")[:-1]]:
        almanac[source]["dest_pos"].append(line[0])
        almanac[source]["source_pos"].append(line[1])
        almanac[source]["lens"].append(line[2])


def source_to_dest(source_type, source_num):
    al_s = almanac[source_type]
    for i in range(len(al_s["source_pos"])):
        start = al_s["source_pos"][i]
        if source_num in range(start, start + al_s["lens"][i]):
            pos = al_s["dest_pos"][i] + (source_num - start)
            return al_s["dest"], pos
    return al_s["dest"], source_num


def get_location(pos):
    obj_type = "seed"
    while obj_type != "location":
        obj_type, pos = source_to_dest(obj_type, pos)
    return pos


min_loc_p1 = min([get_location(pos) for pos in seeds])
print(f"part 1: {min_loc_p1}")


def scan_range(left, range_len, skip):
    # scan a range with given resolution, then increase resolution by 10x to converge
    min_loc_and_range = (1e99, 0, 0)  # location, left, range_len
    for pos in range(left, left + range_len, skip):
        loc = get_location(pos)
        if loc < min_loc_and_range[0]:
            min_loc_and_range = (loc, max(pos - skip, left), min(skip, range_len))
    if skip == 1:
        return min_loc_and_range[0]
    return scan_range(min_loc_and_range[1], min_loc_and_range[2], skip // 10)


# starting resolution might need adjustments depending on input
min_loc_p2 = min(
    [
        scan_range(seeds[i * 2], seeds[i * 2 + 1], 1_000_000)
        for i in range(len(seeds) // 2)
    ]
)
print(f"part 2: {min_loc_p2}")
