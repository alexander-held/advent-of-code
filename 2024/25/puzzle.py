import fileinput

x = "".join([line for line in fileinput.input()])[:-1]

locks = []
keys = []
for inp in x.split("\n\n"):
    pins = ["".join([inp[i * 6 + j] for i in range(1, 6)]).count("#") for j in range(5)]
    if inp[0] == "#":
        locks.append(pins)
    else:
        keys.append(pins)

fit = sum(all(l + k <= 5 for l, k in zip(lock, key)) for key in keys for lock in locks)

print(f"part 1: {fit}")
