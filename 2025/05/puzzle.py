import fileinput
import re

x = "\n".join([line for line in fileinput.input()])

ranges = [(int(lo), int(hi)) for (lo, hi) in re.findall(r"(\d+)-(\d+)", x)]
fresh = sum(
    any(lo <= int(ingredient) <= hi for lo, hi in ranges)
    for ingredient in re.findall(r"\n(\d+)\n", x)
)

merged_ranges = []
# sort by lower bound to avoid creation of isolated ranges that would later need merging
for lo_new, hi_new in sorted(ranges, key=lambda r: r[0]):
    for idx, (lo, hi) in enumerate(merged_ranges):
        if lo_new <= hi and hi_new >= lo:  # merge if there is overlap
            merged_ranges[idx] = (min(lo, lo_new), max(hi, hi_new))
            break
    else:
        merged_ranges.append((lo_new, hi_new))  # new range if no overlap exists


print(f"part 1: {fresh}")
print(f"part 2: {sum(hi - lo + 1 for lo, hi in merged_ranges)}")
