import fileinput
from math import ceil

x = [int(line.strip()) for line in fileinput.input()][0]

square_num = ceil((x**0.5 - 1) / 2)  # concentric squares of size (2*n+1)^2
# find positions of midpoints of edges of square
midpoints = [(2 * square_num + 1) ** 2 - square_num * (1 + 2 * i) for i in range(4)]
# total distance: steps to closest midpoint and then straight to center
num_steps = square_num + min([abs(x - midpoint) for midpoint in midpoints])

print(f"part 1: {num_steps}")

spiral = {0: 1}
pos, direc = 0, 1  # create spiral by walking (complex coordinates)
while True:
    pos += direc
    sum_neighbors = sum([v for k, v in spiral.items() if abs(k - pos) < 2])
    if sum_neighbors > x:
        break
    spiral[pos] = sum_neighbors  # continue spiral
    if pos + direc * (-1j) not in spiral.keys():
        direc *= -1j  # turn left if possible

print(f"part 2: {sum_neighbors}")
