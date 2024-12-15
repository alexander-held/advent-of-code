import fileinput


x = "\n".join([line.strip() for line in fileinput.input()])

grid_p1 = dict()
grid_p2 = dict()
chars_p2 = {"#": "##", "O": "[]", ".": "..", "@": "@."}
for a, line in enumerate(x.split("\n\n")[0].split()):
    for b in range(len(line)):
        grid_p1[a + 1j * b] = line[b]
        grid_p2[a + 1j * 2 * b] = chars_p2[line[b]][0]
        grid_p2[a + 1j * (2 * b + 1)] = chars_p2[line[b]][1]


def get_gps(grid):
    for step in "".join(x.split("\n\n")[1]).replace("\n", ""):
        d = {"^": -1, ">": +1j, "v": +1, "<": -1j}[step]
        to_move = [next(k for k, v in grid.items() if v == "@")]  # robot
        for pos in to_move:
            if grid[pos + d] == ".":
                continue
            elif grid[pos + d] == "#":
                break  # cannot move walls, so nothing moves

            # when moving up/down, also bring along other part of box for part 2
            if d in [1, -1] and grid[pos + d] == "[" and pos + d + 1j not in to_move:
                to_move.append(pos + d + 1j)
            elif d in [1, -1] and grid[pos + d] == "]" and pos + d - 1j not in to_move:
                to_move.append(pos + d - 1j)

            if pos + d not in to_move:
                to_move.append(pos + d)

        else:  # move all pieces if no wall was found
            for pos in to_move[::-1]:
                grid[pos], grid[pos + d] = grid[pos + d], grid[pos]

    return int(sum(100 * k.real + k.imag for k, v in grid.items() if v in "O["))


print(f"part 1: {get_gps(grid_p1)}")
print(f"part 2: {get_gps(grid_p2)}")
