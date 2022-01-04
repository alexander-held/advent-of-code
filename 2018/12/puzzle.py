import fileinput
from collections import defaultdict

x = [line.strip() for line in fileinput.input()]
state = defaultdict(lambda: ".")
state.update(dict((i, c) for i, c in enumerate(x[0].split(":")[1].strip())))
rules = dict([line.split(" => ") for line in x[2:]])  # {pattern: replacement}


def step(state, rules):
    new_state = defaultdict(lambda: ".")
    for i in range(min(state.keys()) - 2, max(state.keys()) + 3):
        window = state[i - 2] + state[i - 1] + state[i] + state[i + 1] + state[i + 2]
        replacement = rules.get(window, None)
        if replacement:
            new_state[i] = replacement  # apply rule if one matches
    return new_state


def sum_pots(state, rules, num_generations):
    last_pattern = None
    last_left = None

    for i in range(1, num_generations + 1):
        state = step(state, rules)

        # extract "active" area: everything between first and last "#"
        all_active = [k for k, v in state.items() if v == "#"]
        active_range = range(min(all_active), max(all_active))
        new_pattern = "".join([state[a] for a in active_range])
        if new_pattern == last_pattern:
            # pattern repeats, figure out direction and how many steps are left
            direction = min(all_active) - last_left
            days_left = num_generations - i
            return sum(k + days_left * direction for k, v in state.items() if v == "#")
        last_pattern = new_pattern  # remember pattern for next iteration
        last_left = min(all_active)  # remember start of pattern for next iteration

    return sum(k for k, v in state.items() if v == "#")  # for part 1


print(f"part 1: {sum_pots(state.copy(), rules, 20)}")
print(f"part 2: {sum_pots(state.copy(), rules, 50_000_000_000)}")
