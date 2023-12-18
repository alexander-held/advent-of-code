import fileinput

x = [line.split() for line in fileinput.input()]

direc_map = {"R": 1, "D": +1j, "L": -1, "U": -1j, "0": 1, "1": 1j, "2": -1, "3": -1j}


def get_area(x, p2=False):
    vertices = [0]  # position of vertices as complex numbers
    len_trench = 0
    for line in x:
        if not p2:
            direc, n_steps, _ = line
        else:
            n_steps = int(line[-1][2:-2], 16)
            direc = line[-1][-2]

        len_trench += int(n_steps)
        vertices.append(vertices[-1] + direc_map[direc] * int(n_steps))

    # Shoelace formula will miss contributions from trench due to size of each cube
    # need to add half of trench, plus one extra for outer contribution from closed loop
    # (see also Pick's theorem)
    shoelace_area = 0
    for v1, v2 in zip(vertices[:-1], vertices[1:]):
        shoelace_area += (v1.real * v2.imag) - (v2.real * v1.imag)
    return int(shoelace_area / 2 + len_trench / 2 + 1)


print(f"part 1: {get_area(x)}")
print(f"part 2: {get_area(x, p2=True)}")
