import fileinput
import re
from functools import cmp_to_key

x = "".join([line for line in fileinput.input()])

rules = re.findall(r"(\d+)\|(\d+)", x)


def compare(a, b):
    if (a, b) in rules:
        return -1  # a is smaller than b
    elif (b, a) in rules:
        return 1  # a is larger than b
    else:
        return 0  # equal


sum_p1 = 0
sum_p2 = 0
for matches in re.findall(r"((\d+,)+\d+)", x):
    pages = matches[0].split(",")
    sorted_pages = sorted(pages, key=cmp_to_key(compare))
    num_mid = int(sorted_pages[len(sorted_pages) // 2])
    if pages == sorted_pages:  # was correctly sorted already
        sum_p1 += num_mid
    else:
        sum_p2 += num_mid


print(f"part 1: {sum_p1}")
print(f"part 2: {sum_p2}")
