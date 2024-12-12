import fileinput
from collections import defaultdict

x = [line.strip() for line in fileinput.input()]

garden = defaultdict(str)
all_plots = set()
for a in range(len(x)):
    for b in range(len(x[0])):
        garden[a + 1j * b] = x[a][b]
        all_plots.add(a + 1j * b)


def get_region(pos, plot_type, seen):
    edges = 0
    for direc in (-1, 1j, 1, -1j):
        if garden[pos + direc] == plot_type and pos + direc not in seen:
            new_seen, new_edges = get_region(
                pos + direc, plot_type, seen | {pos + direc}
            )
            seen |= new_seen  # collect all matching plots
            edges += new_edges
        elif garden[pos + direc] != plot_type and pos + direc not in seen:
            edges += 1

    return seen, edges


price_p1 = 0
price_p2 = 0
while len(all_plots):
    plot = list(all_plots)[0]  # pick a single plot
    seen, edges = get_region(plot, garden[plot], {plot})
    price_p1 += len(seen) * edges
    all_plots -= seen

    num_corners = 0  # count edges by counting corners instead
    for s in seen:  # find plots in corner positions
        if (s - 1 not in seen) and (s - 1j not in seen) and (s - 1 - 1j not in seen):
            num_corners += 1  # top left outer
        if (s - 1 not in seen) and (s + 1j not in seen) and (s - 1 + 1j not in seen):
            num_corners += 1  # too right outer
        if (s + 1 not in seen) and (s + 1j not in seen) and (s + 1 + 1j not in seen):
            num_corners += 1  # bottom right outer
        if (s + 1 not in seen) and (s - 1j not in seen) and (s + 1 - 1j not in seen):
            num_corners += 1  # bottom left outer

        if (s - 1j not in seen) and (s - 1 - 1j in seen):
            num_corners += 1  # top left inner
        if (s + 1j not in seen) and (s - 1 + 1j in seen):
            num_corners += 1  # top right inner
        if (s + 1j not in seen) and (s + 1 + 1j in seen):
            num_corners += 1  # bottom right inner
        if (s - 1j not in seen) and (s + 1 - 1j in seen):
            num_corners += 1  # bottom left inner

    price_p2 += len(seen) * num_corners


print(f"part 1: {price_p1}")
print(f"part 2: {price_p2}")
