import fileinput
import re
from collections import defaultdict

x = [line for line in fileinput.input()]

valves = {}
for line in x:
    name, rate, targets = re.findall(r"Valve (\w+).*=(\d+).*valves? (.*)", line)[0]
    valves.update({name: {"rate": int(rate), "targets": targets.split(", ")}})


def simulate(time_total, valves):
    current_states = [("AA", frozenset(), 0)]  # pos, open valves, expected pressure
    best_pressure = defaultdict(lambda: -1)  # best for (pos, open_valves) state

    for t in range(1, time_total + 1):  # timer
        next_states = []  # possible choices for next second

        for pos, open_valves, pressure in current_states:
            if pressure <= best_pressure[(pos, open_valves)]:
                continue  # already had better option before
            best_pressure[(pos, open_valves)] = pressure

            for target in valves[pos]["targets"]:  # move to next valve
                next_states.append((target, open_valves, pressure))

            if valves[pos]["rate"] > 0 and pos not in open_valves:  # open valve
                next_states.append(
                    (
                        pos,
                        open_valves | {pos},
                        pressure + valves[pos]["rate"] * (time_total - t),
                    )
                )

        current_states = next_states

    return best_pressure


print(f"part 1: {max(simulate(30, valves).values())}")

pressure_per_state = simulate(26, valves)
pressure_max = 0
for (_, opened_1), score_1 in pressure_per_state.items():
    if score_1 < (pressure_max / 2):
        continue  # cannot beat max score
    for (_, opened_2), score_2 in pressure_per_state.items():
        if opened_1 & opened_2 == frozenset():  # no overlap in valves opened
            pressure_max = max(pressure_max, score_1 + score_2)

print(f"part 2: {pressure_max}")
