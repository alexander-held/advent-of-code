import fileinput
from operator import gt, lt
import re
import time

x = [line.strip() for line in fileinput.input()]

workflows = {}
for workflow in x[: x.index("")]:
    name, next_default = re.findall(r"(\w+){.*,(\w+)}", workflow)[0]
    rules = re.findall(r"(\w)([><])(\d+):(\w+)", workflow)
    workflows[name] = [(r[0], r[1], int(r[2]), r[3]) for r in rules] + [next_default]

parts = [p.strip("{}") for p in x[x.index("") + 1 :]]
parts = [
    dict((v.split("=")[0], int(v.split("=")[1])) for v in p)
    for p in [p.split(",") for p in parts]
]


def apply_rule(part, rule):
    # rule looks like this: ('a', '<', '2006', 'qkq')
    r0, r1, r2, r3 = rule
    pp = part[r0]
    if (r1 == "<" and pp < r2) or (r1 == ">" and pp > r2):
        return r3
    # version below is slower
    # if {"<": lt, ">": gt}[rule[1]](int(part[rule[0]]), int(rule[2])):
    #     return rule[3]
    return None  # rule not satisfied, need to check next rule


def get_rating(part, workflows):
    wf_name = "in"  # start with "in"
    while wf_name not in ["A", "R"]:
        rules = workflows[wf_name].copy()
        wf_name = None  # find next workflow
        while wf_name is None:  # handle all rules for one workflow
            rule = rules.pop(0)
            if len(rules) == 0:
                wf_name = rule  # workflow did not satisfy any rules
            else:
                wf_name = apply_rule(part, rule)
    return sum(map(int, part.values())) if wf_name == "A" else 0


print(f"part 1: {sum(get_rating(part, workflows) for part in parts)}")


# find all places where decisions branch
branch_points = {"x": [], "m": [], "a": [], "s": []}
for ch in branch_points.keys():
    for workflow in workflows.values():
        for rule in workflow[:-1]:
            if rule[0] == ch:
                branch_points[ch].append(int(rule[2]) - (1 if rule[1] == "<" else 0))
    branch_points[ch] = sorted(branch_points[ch] + [0, 4000])

t0 = time.time()
num_combinations = 0
# this approach is _very_ slow (~1h with pypy on full input), presumably much better
# to (recursively) traverse graph of workflows and track accepted / rejected ranges
for i, (x1, x2) in enumerate(zip(branch_points["x"][:-1], branch_points["x"][1:])):
    print(f"{i/(len(branch_points['x'])-1):.2%}, {(time.time()-t0)/60:.2f} min")
    for m1, m2 in zip(branch_points["m"][:-1], branch_points["m"][1:]):
        for a1, a2 in zip(branch_points["a"][:-1], branch_points["a"][1:]):
            for s1, s2 in zip(branch_points["s"][:-1], branch_points["s"][1:]):
                # if x2, m2, a2, s2 is accepted, the full hypercube is
                if get_rating({"x": x2, "m": m2, "a": a2, "s": s2}, workflows):
                    num_combinations += (x2 - x1) * (m2 - m1) * (a2 - a1) * (s2 - s1)

print(f"part 2: {num_combinations}")
