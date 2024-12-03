import fileinput
import re
from math import prod

x = "".join([line for line in fileinput.input()])

enabled = True
sum_res_p1 = 0
sum_res_p2 = 0
for res in re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", x):
    if res == "do()":
        enabled = True
    elif res == "don't()":
        enabled = False
    else:
        to_add = prod(map(int, re.findall(r"\d+", res)))
        sum_res_p1 += to_add
        sum_res_p2 += to_add * enabled

print(f"part 1: {sum_res_p1}")
print(f"part 2: {sum_res_p2}")
