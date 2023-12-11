import fileinput
from itertools import combinations

x = [line for line in fileinput.input()]

galaxy_list = []
for y_pos in range(len(x)):
    for x_pos in range(len(x[0])):
        if x[y_pos][x_pos] == "#":
            galaxy_list.append(x_pos + 1j * y_pos)


def expand(galaxy_list, factor):
    expanded_galaxies = galaxy_list.copy()

    len_x = int(max([k.real for k in galaxy_list]))
    empty_columns = set(range(len_x + 1)) - set([k.real for k in galaxy_list])

    len_y = int(max([k.imag for k in galaxy_list]))
    empty_rows = set(range(len_y + 1)) - set([k.imag for k in galaxy_list])

    for i_gal in range(len(galaxy_list)):
        for col_pos in sorted(empty_columns):
            if galaxy_list[i_gal].real > col_pos:
                expanded_galaxies[i_gal] += factor - 1  # move affected galaxies
        for row_pos in sorted(empty_rows):
            if galaxy_list[i_gal].imag >= row_pos:
                expanded_galaxies[i_gal] += 1j * (factor - 1)
    return expanded_galaxies


def sum_paths(galaxy_list, factor=2):
    expanded_galaxies = expand(galaxy_list, factor)
    sum_len = 0
    for pair in combinations(expanded_galaxies, 2):
        sum_len += abs(pair[0].real - pair[1].real) + abs(pair[0].imag - pair[1].imag)
    return int(sum_len)


print(f"part 1: {sum_paths(galaxy_list)}")
print(f"part 2: {sum_paths(galaxy_list, factor=1_000_000)}")
