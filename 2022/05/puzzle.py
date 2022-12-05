import copy
import fileinput
import re

x = "".join([line for line in fileinput.input()]).split("\n\n")
layout = x[0].split("\n")
instructions = x[1].split("\n")[:-1]
n_stacks = len(layout[-1].split())
stacks = [[] for _ in range(n_stacks)]

# set up initial stacks
for layer in layout[:-1][::-1]:
    for i_stack in range(n_stacks):
        if i_stack * 4 + 1 <= len(layer) and layer[i_stack * 4 + 1] != " ":
            stacks[i_stack] += [layer[i_stack * 4 + 1]]


def move(stacks, instructions, p2=False):
    stacks = copy.deepcopy(stacks)
    for instr in instructions:
        num_to_move, move_from, move_to = map(int, re.findall(r"\d+", instr))
        crates = [stacks[move_from - 1].pop() for _ in range(num_to_move)]
        stacks[move_to - 1] += crates[:: -2 * p2 + 1]  # flip order for part 2
    return "".join([stack[-1] for stack in stacks])


print(f"part 1: {move(stacks, instructions)}")
print(f"part 2: {move(stacks, instructions, p2=True)}")
