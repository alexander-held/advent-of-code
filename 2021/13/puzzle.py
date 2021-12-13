import fileinput
from collections import Counter
from itertools import product

x = [line.strip() for line in fileinput.input()]

dots = dict()
fold_instructions = []
for line in x:
    if "," in line:
        dots.update({tuple([p for p in map(int, line.split(","))]): "#"})
    elif "fold" in line:
        fold_instructions.append([line.split("=")[-2][-1], int(line.split("=")[-1])])


def fold_paper(dots, width, height, axis, pos):
    if axis == "y":
        for i, j in product(range(width), range(pos)):
            if dots.get((i, height - j - 1)):
                dots[i, j] = dots.pop((i, height - j - 1))
        return dots, width, pos

    elif axis == "x":
        for i, j in product(range(pos), range(height)):
            if dots.get((width - i - 1, j)):
                dots[i, j] = dots.pop((width - i - 1, j))
        return dots, pos, height


width = max([p[0] for p in dots]) + 1
height = max([p[1] for p in dots]) + 1

for i, fold in enumerate(fold_instructions):
    dots, width, height = fold_paper(dots, width, height, fold[0], fold[1])
    if i == 0:
        print(f"part 1: {Counter(dots.values())['#']}")

print(f"part 2:")
for j in range(height):
    print(" ".join(dots.get((i, j), " ") for i in range(width)))
