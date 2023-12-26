import fileinput

x = [line.strip() for line in fileinput.input()][0]

recipes = [3, 7]
p1, p2 = 0, 1  # position of elves
while True:
    recipes += [int(r) for r in str(recipes[p1] + recipes[p2])]
    p1 = (p1 + 1 + recipes[p1]) % len(recipes)  # elves move
    p2 = (p2 + 1 + recipes[p2]) % len(recipes)
    # only search through last few recipes
    recipes_made = "".join(str(r) for r in recipes[-10:])
    idx = recipes_made.find(x)
    if idx != -1:
        print(f"part 2: {idx + len(recipes) - 10}")  # ~5 sec with pypy
        break

print(f"part 1: {''.join(str(r) for r in recipes[int(x):int(x)+10])}")
