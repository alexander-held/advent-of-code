import fileinput
from collections import Counter

template, _, *rest = [line.strip() for line in fileinput.input()]

rules = {}
for line in rest:
    rules.update({line.split(" -> ")[0]: line.split(" -> ")[1]})

# count individual characters and pairs of characters
char_counts = Counter(template[0])
pair_counts = Counter()
for i in range(1, len(template)):
    char_counts[template[i]] += 1
    pair_counts[template[i - 1 : i + 1]] += 1

for step in range(0, 40):
    next_counts = Counter()
    for pair, number in pair_counts.items():
        char_to_insert = rules.get(pair, None)
        if char_to_insert is None:
            continue  # not needed in practice for this problem

        char_counts[char_to_insert] += number
        next_counts[pair[0] + char_to_insert] += number
        next_counts[char_to_insert + pair[1]] += number

    pair_counts = next_counts

    if step == 9:
        print(f"part 1: {max(char_counts.values()) - min(char_counts.values())}")

print(f"part 2: {max(char_counts.values()) - min(char_counts.values())}")
