import fileinput
from collections import defaultdict
import re


x = [line for line in fileinput.input()]

cards_won = defaultdict(lambda: 1)  # starting with one of each card
points = 0
for i, card in enumerate(x, start=1):
    winning, have = [
        set(map(int, re.findall(r"\d+", nums)))
        for nums in card.split(":")[1].split("|")
    ]
    num_wins = len(winning & have)
    if num_wins > 0:
        points += 2 ** (num_wins - 1)

    for ii in range(i + 1, i + num_wins + 1):
        cards_won[ii] += cards_won[i]  # win additional cards down the list

print(f"part 1: {points}")
print(f"part 2: {sum([cards_won[i] for i in range(1, len(x)+1)])}")
