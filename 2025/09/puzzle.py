import fileinput
from itertools import combinations

x = [list(map(int, line.split(","))) for line in fileinput.input()]

get_area = lambda a, b: (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)
pairs = [(p, get_area(*p)) for p in combinations(x, 2)]

for (a, b), area in sorted(pairs, key=lambda v: v[1])[::-1]:  # decreasing area
    # rectangle is not valid if any connection crosses it (connection empty on one side)
    for l1, l2 in zip(x, x[1:] + x[:1]):
        if (
            (min(l1[0], l2[0]) < max(a[0], b[0]))  # line not above rectangle
            and (max(l1[0], l2[0]) > min(a[0], b[0]))  # line not below rectangle
            and (max(l1[1], l2[1]) > min(a[1], b[1]))  # line not left of rectangle
            and (min(l1[1], l2[1]) < max(a[1], b[1]))  # line not right of rectangle
        ):
            break  # line crosses somewhere, rectangle is invalid
    else:
        break  # no crossing has happened

print(f"part 1: {max([p[1] for p in pairs])}")
print(f"part 2: {area}")
