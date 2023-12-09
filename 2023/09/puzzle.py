import fileinput

import numpy as np

x = [np.asarray(line.split(), dtype=int) for line in fileinput.input()]


def extrapolate(diffs, extrap_sum):
    extrap_sum += diffs[-1]
    diffs = diffs[1:] - diffs[:-1]
    if np.count_nonzero(diffs) == 0:
        return extrap_sum
    else:
        return extrapolate(diffs, extrap_sum)


print(f"part 1: {sum([extrapolate(line, 0) for line in x])}")
print(f"part 2: {sum([extrapolate(line[::-1], 0) for line in x])}")
