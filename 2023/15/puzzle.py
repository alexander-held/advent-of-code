import fileinput
from collections import defaultdict
import re

x = "".join([line.strip() for line in fileinput.input()])


def hash(inp):
    cur = 0
    for ch in inp:
        cur = ((cur + ord(ch)) * 17) % 256
    return cur


boxes = defaultdict(dict)
for label, foc_len in re.findall(r"(\w+)[=-](\d*)", x):
    if foc_len.isdigit():  # add to box
        boxes[hash(label)][label] = foc_len  # append or update focal length
    else:  # remove from box
        boxes[hash(label)].pop(label, None)

foc_pow = 0
for i_box, box in boxes.items():
    for i_slot, foc_len in enumerate(box.values()):
        foc_pow += (1 + i_box) * (1 + i_slot) * int(foc_len)

print(f"part 1: {sum(hash(part) for part in x.split(','))}")
print(f"part 2: {foc_pow}")
