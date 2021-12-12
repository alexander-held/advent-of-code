import fileinput
from collections import defaultdict

x = [line.strip() for line in fileinput.input()]

connections = defaultdict(list)

for line in x:
    start, end = line.split("-")
    connections[start] += [end]
    connections[end] += [start]


def get_paths(cur_cave: str, seen_low: set, can_see_twice: bool = False):
    if cur_cave == "end":
        yield []

    for next_cave in connections[cur_cave]:
        if next_cave not in seen_low:
            next_seen = (seen_low | {next_cave}) if next_cave.islower() else seen_low
            for path in get_paths(next_cave, next_seen, can_see_twice):
                yield [next_cave] + path
        elif can_see_twice and next_cave not in ["start", "end"]:
            for path in get_paths(next_cave, seen_low, can_see_twice=False):
                yield [next_cave] + path


print(f"part 1: {len([p for p in get_paths('start', {'start'})])}")
print(f"part 2: {len([p for p in get_paths('start', {'start'}, can_see_twice=True)])}")
