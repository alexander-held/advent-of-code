import fileinput
from functools import cache

x = [line.strip() for line in fileinput.input()]
patterns = x[0].split(", ")


@cache
def count_solutions(design):
    if design == "":
        return 1  # fully matched
    remaining_designs = [design[len(p) :] for p in patterns if design.startswith(p)]
    return sum(count_solutions(remaining) for remaining in remaining_designs)


print(f"part 1: {sum(1 for design in x[2:] if count_solutions(design))}")
print(f"part 2: {sum(count_solutions(design) for design in x[2:])}")
