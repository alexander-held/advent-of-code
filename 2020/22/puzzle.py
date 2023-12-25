import fileinput
from collections import deque

p1_orig, p2_orig = "".join([line for line in fileinput.input()]).split("\n\n")
p1_orig = deque([int(x) for x in p1_orig.split("\n")[1:]])
p2_orig = deque([int(x) for x in p2_orig.strip().split("\n")[1:]])


def combat(p1, p2):
    while len(p1) * len(p2) > 0:
        top_p1 = p1.popleft()
        top_p2 = p2.popleft()
        if top_p1 > top_p2:
            p1.extend([top_p1, top_p2])
        else:
            p2.extend([top_p2, top_p1])


def winning_score(p1, p2):
    winning_cards = p1 if len(p1) != 0 else p2
    score = 0
    for i in range(1, len(winning_cards) + 1)[::-1]:
        score += winning_cards[len(winning_cards) - i] * i
    return score


p1, p2 = p1_orig.copy(), p2_orig.copy()
combat(p1, p2)
print(f"part 1: score {winning_score(p1, p2)}")


def recursive_combat(p1, p2):  # True if p1 wins
    decks_seen = set()
    while len(p1) * len(p2) > 0:
        this_round = (tuple(p1), tuple(p2))
        if this_round in decks_seen:
            return True  # p1 wins
        decks_seen.add(this_round)

        top_p1 = p1.popleft()
        top_p2 = p2.popleft()

        if len(p1) >= top_p1 and len(p2) >= top_p2:
            # create decks and play recursive game
            p1_sub = deque([p1[i] for i in range(top_p1)])
            p2_sub = deque([p2[i] for i in range(top_p2)])
            if recursive_combat(p1_sub, p2_sub):
                p1.extend([top_p1, top_p2])  # p1 wins recursive round
            else:
                p2.extend([top_p2, top_p1])

        else:
            # normal non-recursive round
            if top_p1 > top_p2:
                p1.extend([top_p1, top_p2])
            else:
                p2.extend([top_p2, top_p1])

    return len(p1) > 0


p1, p2 = p1_orig.copy(), p2_orig.copy()
recursive_combat(p1, p2)
print(f"part 2: score {winning_score(p1, p2)}")
