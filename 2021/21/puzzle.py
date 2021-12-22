import fileinput
import re
from collections import Counter
from itertools import cycle, product
from functools import lru_cache

x = [line.strip() for line in fileinput.input()]
start_pos = [int(re.search("\d+$", line).group()) for line in x]


def play(player_pos):
    rolls = 0
    scores = [0, 0]  # player 1, player 2
    die = cycle(range(1, 101))
    while max(scores) < 1000:
        player_pos[0] = (player_pos[0] + sum(next(die) for _ in range(3))) % 10 or 10
        rolls += 3
        scores[0] += player_pos[0]

        if scores[0] >= 1000:
            break  # player 1 won

        player_pos[1] = (player_pos[1] + sum(next(die) for _ in range(3))) % 10 or 10
        rolls += 3
        scores[1] += player_pos[1]

    return min(scores) * rolls


print(f"part 1: {play(start_pos[:])}")  # copy position to not alter it


roll_counter = Counter(sum(rolls) for rolls in product([1, 2, 3], repeat=3))


@lru_cache(maxsize=None)
def play_quantum(pos_active, pos_other, score_active, score_other):
    if score_other >= 21:
        return 0, 1  # only other player can win here, since they just took a turn

    num_wins_1 = 0
    num_wins_2 = 0

    for roll, multiplier in roll_counter.items():
        # active player takes turn
        new_pos_active = (pos_active + roll) % 10 or 10
        new_score_active = score_active + new_pos_active

        # play again with order switched
        w2, w1 = play_quantum(pos_other, new_pos_active, score_other, new_score_active)
        num_wins_1 += w1 * multiplier  # account for copies of universes
        num_wins_2 += w2 * multiplier

    return num_wins_1, num_wins_2


print(f"part 2: {max(play_quantum(start_pos[0], start_pos[1], 0, 0))}")
