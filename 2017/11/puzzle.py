import fileinput

x = "".join([line.strip() for line in fileinput.input()])

# https://www.redblobgames.com/grids/hexagons/#coordinates "odd-q" vertical layout
pos = 0  # complex coordinates (0, 0) -> 0+0j
distance_max = 0
for direc in x.split(","):
    if direc == "n":
        pos -= 1j
    elif direc == "ne":
        pos += 1
    elif direc == "se":
        pos += 1 + 1j
    elif direc == "s":
        pos += 1j
    elif direc == "sw":
        pos -= 1
    elif direc == "nw":
        pos -= 1 + 1j

    distance_max = max(distance_max, abs(pos.real) + abs(pos.imag))

print(f"part 1: {int(abs(pos.real) + abs(pos.imag))}")
print(f"part 2: {int(distance_max)}")
