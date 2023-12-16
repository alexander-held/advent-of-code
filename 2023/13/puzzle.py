import fileinput

x = "\n".join([line.strip() for line in fileinput.input()])


def get_num(x, p2=False):
    sol = 0
    for pattern in x.split("\n\n"):
        grid = pattern.split("\n")

        for i in range(1, len(grid)):  # check horizontal symmetries top to bottom
            num_wrong = 0
            for top, bottom in zip(grid[:i][::-1], grid[i:]):
                num_wrong += sum(t != b for t, b in zip(top, bottom))
            if num_wrong == (0 if not p2 else 1):
                sol += 100 * i

        for i in range(1, len(grid[0])):  # check vertical symmetries left to right
            num_wrong = 0
            for line in grid:  # count mismatches between left and right
                num_wrong += sum(l != r for l, r in zip(line[:i][::-1], line[i:]))
            if num_wrong == (0 if not p2 else 1):
                sol += i
    return sol


print(f"part 1: {get_num(x)}")
print(f"part 2: {get_num(x, p2=True)}")
