import fileinput
from functools import cache

x = [line.strip() for line in fileinput.input()][0]


@cache
def dance(commands, programs):
    programs = [ch for ch in programs]
    for cmd in commands.split(","):
        if cmd[0] == "s":  # spin of given size
            size = int(cmd[1:])
            programs = programs[-size:] + programs[:-size]
        elif cmd[0] == "x":  # swap programs at two positions
            pos_1, pos_2 = [int(pos) for pos in cmd[1:].split("/")]
            tmp = programs[pos_2]
            programs[pos_2] = programs[pos_1]
            programs[pos_1] = tmp
        elif cmd[0] == "p":  # swap programs with given names
            ch_1, ch_2 = cmd[1:].split("/")
            idx_1, idx_2 = programs.index(ch_1), programs.index(ch_2)
            programs[idx_1] = ch_2
            programs[idx_2] = ch_1
    return "".join(programs)


print(f"part 1: {dance(x, 'abcdefghijklmnop')}")

programs = "abcdefghijklmnop"
for _ in range(1_000_000_000):
    programs = dance(x, programs)  # ~90 seconds via brute force with cache

print(f"part 2: {programs}")
