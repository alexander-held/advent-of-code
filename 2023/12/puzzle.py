import fileinput
from functools import cache

x = [line.strip() for line in fileinput.input()]


@cache
def recurse(pattern, counts):
    num_arrangements = 0

    if sum(counts) > len(pattern):
        return 0  # no characters left

    elif sum(counts) < pattern.count("#"):
        return 0  # too many damaged springs left

    elif len(counts) == 0 and "#" not in pattern:
        return 1  # valid pattern, no counts left and no broken springs remaining

    elif len(pattern) == 1 and pattern in "?#":
        return 1  # valid pattern, last broken spring as expected

    if pattern[0] in "?#":  # start pattern of broken springs
        new_pattern = pattern[: counts[0]].replace("?", "#")
        if new_pattern == "#" * counts[0]:  # can fit a full group
            if len(pattern) == len(new_pattern) or pattern[counts[0]] != "#":
                # either last pattern, or can follow broken pattern by .
                num_arrangements += recurse(pattern[counts[0] + 1 :], counts[1:])

    if pattern[0] in "?.":  # add operational spring
        num_arrangements += recurse(pattern[1:], counts)

    return num_arrangements


def count_arrangements(x, p2=False):
    sum_arrangements = 0
    for line in x:
        pattern, counts = line.split()
        counts = tuple(map(int, counts.split(",")))
        if p2:
            pattern = "?".join([pattern for _ in range(5)])
            counts *= 5
        sum_arrangements += recurse(pattern, counts)
    return sum_arrangements


print(f"part 1: {count_arrangements(x)}")
print(f"part 2: {count_arrangements(x, p2=True)}")
