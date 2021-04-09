import fileinput
import string

x = [line.strip() for line in fileinput.input()][0]


def react(polymer):
    lower_bound = 0
    while True:
        remove_idx = None
        for i in range(lower_bound, len(polymer) - 1):
            if (
                polymer[i] == polymer[i + 1].swapcase()
                and polymer[i].lower() == polymer[i + 1].lower()
            ):
                remove_idx = i
                lower_bound = max(i - 1, 0)  # set starting point for next step
                break
        if remove_idx is None:
            break  # fully reacted
        else:
            polymer = polymer[:remove_idx] + polymer[remove_idx + 2 :]  # segment reacts
    return polymer


polymer = react(x)
print(f"part 1: {len(polymer)}")


shortest_poly = len(polymer)
for ch in string.ascii_lowercase:
    polymer = react(x.replace(ch, "").replace(ch.upper(), ""))  # characters removed
    shortest_poly = min(shortest_poly, len(polymer))
print(f"part 2: {shortest_poly}")
