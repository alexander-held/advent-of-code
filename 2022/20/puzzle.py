import fileinput
from itertools import cycle

x = [(i, int(line)) for i, line in enumerate(fileinput.input())]  # idx for uniqueness


def mix(file, p2=False):
    file = file.copy()
    if p2:
        file = [(idx, num * 811589153) for (idx, num) in file]
    cycle_file = cycle(file.copy())
    for _ in range(len(file) * (1 + p2 * 9)):
        cur = next(cycle_file)  # get next number to mix
        cur_idx = file.index(cur)
        file.remove(cur)
        file.insert((cur_idx + cur[1]) % (len(file)), cur)  # insert at new position

    zero_idx = file.index(next((idx, num) for idx, num in x if num == 0))
    res = sum(file[(zero_idx + offset) % len(file)][1] for offset in [1000, 2000, 3000])
    return res


print(f"part 1: {mix(x)}")
print(f"part 2: {mix(x, p2=True)}")
