import fileinput

x = list(map(int, [line.split()[-1] for line in fileinput.input()]))


def simulate(a, b, part_2=False):
    num_matches = 0
    for _ in range(40_000_000 if not part_2 else 5_000_000):
        old_a, old_b = a, b
        while a == old_a or (part_2 and a % 4 != 0):
            a = (a * 16807) % 2147483647
        while b == old_b or (part_2 and b % 8 != 0):
            b = (b * 48271) % 2147483647
        num_matches += a & 65535 == b & 65535
    return num_matches


print(f"part 1: {simulate(*x)}")
print(f"part 2: {simulate(*x, part_2=True)}")  # total ~0.5s with pypy3
