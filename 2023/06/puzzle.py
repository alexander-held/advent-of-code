import fileinput


durations, records = [list(map(int, line.split()[1:])) for line in fileinput.input()]


def solve(times, records):
    num_ways_prod = 1
    for t, r in zip(times, records):
        num_ways_prod *= sum(t_ch * (t - t_ch) > r for t_ch in range(0, t + 1))
    return num_ways_prod


print(f"part 1: {solve(durations, records)}")

durations = [int("".join([str(t) for t in durations]))]
records = [int("".join([str(r) for r in records]))]
# surprisingly, brute force is still fast enough for part 2, no rewrite needed
print(f"part 2: {solve(durations, records)}")
