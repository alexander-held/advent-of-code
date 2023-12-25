import fileinput
import numpy as np

x = [line.strip() for line in fileinput.input()]  # tree: #, empty: .
height = len(x)
width = len(x[0])

product_trees = 1
for n_right, n_down in zip([1, 3, 5, 7, 1], [1, 1, 1, 1, 2]):
    vert_pos = 0
    n_trees = 0
    for h in np.arange(0, height, n_down):
        if x[h][vert_pos % width] == "#":
            n_trees += 1
        vert_pos += n_right
    print(f"path (right {n_right}, down {n_down}): {n_trees}")
    product_trees *= n_trees
print(f"product {product_trees}")
