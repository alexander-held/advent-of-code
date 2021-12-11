import fileinput
from collections import defaultdict
from itertools import count, product

x = [line.strip() for line in fileinput.input()]
energies = [[int(pos) for pos in line] for line in x]

HEIGHT = len(energies)
WIDTH = len(energies[0])

energy_dict = defaultdict(lambda: -9)  # 9: out of bounds
for i, j in product(range(HEIGHT), range(WIDTH)):
    energy_dict.update({(i, j): energies[i][j]})

flashes = 0
step = 0
for step in count(start=1):
    # increase energy level of all octopuses by 1
    for i, j in product(range(HEIGHT), range(WIDTH)):
        energy_dict[i, j] += 1

    # while any octopuses with energy > 9 remain, they flash
    while any([val > 9 for val in energy_dict.values()]):
        for i, j in product(range(HEIGHT), range(WIDTH)):
            if energy_dict[i, j] > 9:
                flashes += 1
                energy_dict[i, j] = -1  # octopus cannot flash any more this round

                neighbors = [(i + a, j + b) for a, b in product([-1, 0, 1], [-1, 0, 1])]
                neighbors.remove((i, j))
                for neighbor in neighbors:
                    # if neighbor is not out of bounds and active, energy increases
                    energy_dict[neighbor] += energy_dict[neighbor] not in [-9, -1]

    # reset all octopuses that flashed
    for i, j in product(range(HEIGHT), range(WIDTH)):
        if energy_dict[i, j] == -1:
            energy_dict[i, j] = 0

    if step == 100:
        print(f"part 1: {flashes}")

    if all([val in [0, -9] for val in energy_dict.values()]):
        print(f"part 2: {step}")
        break
