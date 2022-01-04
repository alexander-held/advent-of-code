import fileinput
from math import inf

import numpy as np
from scipy import signal

grid_serial_number = int([line.strip() for line in fileinput.input()][0])

SIZE = 300
# index arrays with (x_pos, y_pos)
coords_y, coords_x = np.meshgrid(np.arange(1, SIZE + 1), np.arange(1, SIZE + 1))
rack_id = coords_x + 10
power_levels = (((coords_y * rack_id + grid_serial_number) * rack_id) % 1000) // 100 - 5


def get_largest(power_levels, part2=False):
    largest_any_size = -inf
    square_sizes = [3] if not part2 else range(1, 300 + 1)
    for square_size in square_sizes:
        window = np.ones(shape=(square_size, square_size))
        power_per_square = signal.convolve2d(power_levels, window, mode="valid")
        largest_sum = np.max(power_per_square)
        cx, cy = np.where(power_per_square == largest_sum)

        if largest_sum > largest_any_size:
            largest_any_size = largest_sum
            solution = (cx[0] + 1, cy[0] + 1, square_size)

        if square_size > 25:
            break  # subsequent sums all seem to be negative, so can stop early

    return solution


sol = get_largest(power_levels)
print(f"part 1: {sol[0]},{sol[1]}")

sol = get_largest(power_levels, part2=True)
print(f"part 2: {sol[0]},{sol[1]},{sol[2]}")
