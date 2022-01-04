import fileinput
import re
from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import count

x = [line.strip() for line in fileinput.input()][0]
num_players, highest_marble = map(int, re.findall(r"\d+", x))


@dataclass
class MarbleGame:
    marble_circle: dict
    current_marble: int
    marbles_remaining: deque


def place_marble(mg: MarbleGame):
    # to insert: lowest remaining marble
    lowest_remaining = mg.marbles_remaining.popleft()

    if lowest_remaining % 23 == 0:
        mc = mg.marble_circle
        # find marble counter-clockwise six times
        six_left = mc[mc[mc[mc[mc[mc[mg.current_marble][0]][0]][0]][0]][0]][0]
        marble_removed = mc[six_left][0]  # seven ccw is removed
        # link six left to previous target of removed marble (previously eight left)
        mc.update({six_left: (mc[marble_removed][0], mc[six_left][1])})
        # update spot left of removed to point to right of removed (skipping removed)
        mc.update({mc[marble_removed][0]: (mc[mc[marble_removed][0]], six_left)})
        del mc[marble_removed]  # remove marble completely
        # marble clockwise of removed marble becomes current
        mg.current_marble = six_left
        # player score: player keeps marble that was about to be placed + marble removed
        points_for_player = lowest_remaining + marble_removed
    else:
        # place next marble between one and two spots clockwise
        once_clockwise = mg.marble_circle[mg.current_marble][1]
        twice_clockwise = mg.marble_circle[once_clockwise][1]
        mg.marble_circle.update({once_clockwise: (mg.current_marble, lowest_remaining)})
        mg.marble_circle.update({lowest_remaining: (once_clockwise, twice_clockwise)})
        mg.current_marble = lowest_remaining  # marble placed becomes current next
        points_for_player = 0

    return mg, points_for_player


def play_game(marble_game: MarbleGame):
    player_scores = defaultdict(int)
    for i_turn in count(start=1):
        active_player = (i_turn - 1) % num_players + 1
        marble_game, score = place_marble(marble_game)
        player_scores[active_player] += score  # update player scores
        if not marble_game.marbles_remaining:
            return max(player_scores.values())  # all marbles placed, return max score


# represent circle as dict with links to left & right neighbors, starting with 0 marble
# current marble is 0 at game start
# deque for remaing marbles for fast .popleft()
mg = MarbleGame({0: (0, 0)}, 0, deque(range(1, highest_marble + 1)))
print(f"part 1: {play_game(mg)}")

highest_marble *= 100
mg = MarbleGame({0: (0, 0)}, 0, deque(range(1, highest_marble + 1)))
print(f"part 2: {play_game(mg)}")  # ~4x faster with pypy than CPython
