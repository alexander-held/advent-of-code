import fileinput
from collections import Counter

x = [[int(fish) for fish in line.strip().split(",")] for line in fileinput.input()][0]


def simulate_number(fish, num_days):
    for _ in range(num_days):
        fish = Counter(
            {
                0: fish[1],
                1: fish[2],
                2: fish[3],
                3: fish[4],
                4: fish[5],
                5: fish[6],
                6: fish[0] + fish[7],
                7: fish[8],
                8: fish[0],
            }
        )
    return sum(fish.values())


print(f"part 1: {simulate_number(Counter(x), 80)}")
print(f"part 2: {simulate_number(Counter(x), 256)}")
