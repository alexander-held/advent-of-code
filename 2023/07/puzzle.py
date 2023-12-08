import fileinput
from collections import Counter
from functools import cmp_to_key

x = [line.strip().split() for line in fileinput.input()]


def card_rank(hand, p2):  # higher value corresponds to better rank
    if p2 and "J" in hand:
        # jokers should turn into most frequent other card, try out all and get max rank
        return max([card_rank(hand.replace("J", ch), False) for ch in "AKQT98765432"])

    # only most common items matter for ranking
    last_two_counts = sorted(Counter(hand).values())[-2:]
    return [[1, 1], [1, 2], [2, 2], [1, 3], [2, 3], [1, 4], [5]].index(last_two_counts)


def get_comparison(p2):
    def compare(hand_1, hand_2):  # if hand_1 > hand_2, returns positive number
        if not p2:
            CARD_RANK = "AKQJT98765432"
        else:
            CARD_RANK = "AKQT98765432J"

        rank_diff = card_rank(hand_1, p2) - card_rank(hand_2, p2)
        if rank_diff:
            return rank_diff

        # tie breaker by card rank
        for i_card in range(5):
            idx_diff = CARD_RANK.index(hand_1[i_card]) - CARD_RANK.index(hand_2[i_card])
            if idx_diff < 0:
                return 1
            elif idx_diff > 0:
                return -1

        return 0  # tie, does not happen in problem

    return compare


def get_total_winnings(hands, bids, p2=False):
    sorted_hands = sorted(hands, key=cmp_to_key(get_comparison(p2)))
    return sum(bids[i] * (sorted_hands.index(hands[i]) + 1) for i in range(len(hands)))


hands = [player[0] for player in x]
bids = [int(player[1]) for player in x]

print(f"part 1: {get_total_winnings(hands, bids)}")
print(f"part 2: {get_total_winnings(hands, bids, p2=True)}")
