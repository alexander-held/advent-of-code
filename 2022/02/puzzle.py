import collections
import fileinput

x = [line.strip().split() for line in fileinput.input()]

pick_score = {"X": 1, "Y": 2, "Z": 3}
game_points = collections.defaultdict(
    int,
    {("AX"): 3, ("BY"): 3, ("CZ"): 3, ("AY"): 6, ("BZ"): 6, ("CX"): 6},
)
score = sum([pick_score[me] + game_points[f"{opponent}{me}"] for opponent, me in x])
print(f"part 1: {score}")

what_to_pick = {
    "X": {"A": "Z", "B": "X", "C": "Y"},  # to lose
    "Y": {"A": "X", "B": "Y", "C": "Z"},  # to draw
    "Z": {"A": "Y", "B": "Z", "C": "X"},  # to win
}
score = 0
for opponent, outcome in x:
    me = what_to_pick[outcome][opponent]
    score += pick_score[me] + game_points[f"{opponent}{me}"]
print(f"part 2: {score}")
