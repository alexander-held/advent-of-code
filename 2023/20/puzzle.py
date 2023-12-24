import fileinput
from collections import deque
from copy import deepcopy
from itertools import count
from math import lcm

x = [line.strip().split(" -> ") for line in fileinput.input()]

modules = {}
conjunction_modules = []
for line in x:
    module = line[0]
    destinations = line[1:][0].split(", ")
    if module.startswith("%"):
        modules[module[1:]] = {
            "type": "%",
            "is_on": False,
            "destinations": destinations,
        }
    elif module.startswith("&"):
        modules[module[1:]] = {
            "type": "&",
            "most_recent": {},
            "destinations": destinations,
        }
        conjunction_modules.append(module[1:])
    else:
        modules[module] = {"type": "broadcaster", "destinations": destinations}

# track inputs to conjunction modules
for mod_name, mod in modules.items():
    for con in conjunction_modules:
        if con in mod["destinations"]:
            modules[con]["most_recent"].update({mod_name: -1})  # found input


def push_button(modules, last_conjunction=None):
    modules = deepcopy(modules)
    messages = deque([("broadcaster", -1)])  # sender and pulse
    num_pulses = {-1: 1, 1: 0}  # one initial low pulse from button
    high_to_conj = []  # track if high pulse is sent to last conjunction
    while messages:
        active_module, pulse = messages.popleft()  # module receives pulse

        if modules[active_module]["type"] == "%":
            if pulse == -1:  # only react to low pulses
                modules[active_module]["is_on"] = not modules[active_module]["is_on"]
                pulse_out = 1 if modules[active_module]["is_on"] else -1
            else:
                continue  # nothing happens

        elif modules[active_module]["type"] == "&":
            if all([v == 1 for v in modules[active_module]["most_recent"].values()]):
                pulse_out = -1
            else:
                pulse_out = 1

        elif modules[active_module]["type"] == "broadcaster":
            pulse_out = pulse

        for dest in modules[active_module]["destinations"]:
            num_pulses[pulse_out] += 1

            if dest == last_conjunction and pulse_out == 1:
                # high pulse sent to last conjunction module
                high_to_conj.append(active_module)

            if dest not in modules.keys():
                continue  # module is of output type
            messages.append((dest, pulse_out))  # new messages to send

            if modules[dest]["type"] == "&":  # update state of conjunction modules
                modules[dest]["most_recent"][active_module] = pulse_out

    return modules, num_pulses.values(), high_to_conj


# part 1
num_low, num_high = 0, 0
modules_for_1k = deepcopy(modules)
for _ in range(1000):
    modules_for_1k, (n_l, n_h), _ = push_button(modules_for_1k)
    num_low += n_l
    num_high += n_h

print(f"part 1: {num_low*num_high}")

# part 2
# this makes some assumptions about graph structure
# the module sending to the final output has conjunction type and multiple inputs
# if all inputs to that conjunction module send high pulse, the last output receives low
# find modules of output type and input to it (makes assumption about graph structure)
for mod_name, mod in modules.items():
    for dest in mod["destinations"]:
        if dest not in modules:
            last_conjunction = mod_name

# track when subgraph endings send first high pulse (assume cycles align)
first_high = {}  # first time when module sends to last conjunction
for i in count(1):
    modules, _, high_to_conj = push_button(modules, last_conjunction=last_conjunction)
    for mod in high_to_conj:
        if mod not in first_high:
            first_high[mod] = i
    if len(first_high) == 4:
        break

print(f"part 2: {lcm(*first_high.values())}")
