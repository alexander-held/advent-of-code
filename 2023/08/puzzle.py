import fileinput
from itertools import cycle
from math import lcm

x = [line.split() for line in fileinput.input()]

map = dict()
directions = x[0][0]
for line in x[2:]:
    map[line[0]] = {"L": line[2].strip("(,"), "R": line[3].strip(")")}


def steps_to_end(pos, p2=False):
    num_steps = 0
    for direction in cycle(directions):
        pos = map[pos][direction]
        num_steps += 1
        if pos == "ZZZ" or (p2 and pos.endswith("Z")):
            return num_steps


print(f"part 1: {steps_to_end('AAA')}")

starting_nodes = [k for k in map.keys() if k.endswith("A")]
num_steps = [steps_to_end(start, p2=True) for start in starting_nodes]
print(f"part 2: {lcm(*num_steps)}")
