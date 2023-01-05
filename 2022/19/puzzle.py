import fileinput
import re
from math import prod

x = "".join([line.strip() for line in fileinput.input()])

blueprints = []
for m in re.findall(r"Blueprint \d+:([\w\d\n. ]*?obsidian\.)", x):
    c = re.findall(r"\d+", m)  # resource costs
    blueprints.append(
        {
            "ore_r": {"ore": int(c[0])},
            "clay_r": {"ore": int(c[1])},
            "obs_r": {"ore": int(c[2]), "clay": int(c[3])},
            "geo_r": {"ore": int(c[4]), "obs": int(c[5])},
        }
    )


def simulate(t_total, bp):
    # state: number of (ore, clay, obs, geo) and number of robots (ore, clay obs, geo)
    current_states = [((0, 0, 0, 0), (1, 0, 0, 0))]

    # largest possible number of ore that can be spent per minute
    max_ore_pm = max([rob_cost["ore"] for rob_cost in bp.values()])

    for t in range(1, t_total + 1):  # timer
        next_states = set()  # possible states for next minute

        # apply pruning to keep search space small
        # keep all states if they have at most 1 geode robots less than the current max
        max_geo_rs = max([s[1][3] for s in current_states])
        current_states = [s for s in current_states if s[1][3] >= max_geo_rs - 1]

        # also ensure they have at most 5 geodes less than the max (tunable)
        # this may be too strict for some inputs!
        max_geo = max([s[0][3] for s in current_states])
        current_states = [s for s in current_states if s[0][3] >= max_geo - 5]

        for state in current_states:
            (ore, clay, obs, geo), (ore_r, clay_r, obs_r, geo_r) = state

            # do nothing this round (wait for more resources)
            next_states.add(
                (
                    (ore + ore_r, clay + clay_r, obs + obs_r, geo + geo_r),
                    (ore_r, clay_r, obs_r, geo_r),
                )
            )

            if t >= t_total:
                continue  # no point in building more robots at the last time step

            # only build ore robot if current ore per minute is less than what can
            # can possibly be spent per minute
            if ore >= bp["ore_r"]["ore"] and ore_r < max_ore_pm:
                next_states.add(
                    (
                        (
                            ore - bp["ore_r"]["ore"] + ore_r,
                            clay + clay_r,
                            obs + obs_r,
                            geo + geo_r,
                        ),
                        (ore_r + 1, clay_r, obs_r, geo_r),
                    )
                )  # build ore robot
            if ore >= bp["clay_r"]["ore"]:
                next_states.add(
                    (
                        (
                            ore - bp["clay_r"]["ore"] + ore_r,
                            clay + clay_r,
                            obs + obs_r,
                            geo + geo_r,
                        ),
                        (ore_r, clay_r + 1, obs_r, geo_r),
                    )
                )  # build clay robot
            if ore >= bp["obs_r"]["ore"] and clay >= bp["obs_r"]["clay"]:
                next_states.add(
                    (
                        (
                            ore - bp["obs_r"]["ore"] + ore_r,
                            clay - bp["obs_r"]["clay"] + clay_r,
                            obs + obs_r,
                            geo + geo_r,
                        ),
                        (ore_r, clay_r, obs_r + 1, geo_r),
                    )
                )  # build obsidian robot
            if ore >= bp["geo_r"]["ore"] and obs >= bp["geo_r"]["obs"]:
                next_states.add(
                    (
                        (
                            ore - bp["geo_r"]["ore"] + ore_r,
                            clay + clay_r,
                            obs - bp["geo_r"]["obs"] + obs_r,
                            geo + geo_r,
                        ),
                        (ore_r, clay_r, obs_r, geo_r + 1),
                    )
                )  # build geode robot

        current_states = next_states

    return max([s[0][3] for s in current_states])


def solve(blueprints, p2=False):
    t_total = 24 if not p2 else 32
    max_per_bp = []
    if p2:
        blueprints = blueprints[:3]
    for bp in blueprints:
        max_per_bp.append(simulate(t_total, bp))
    if not p2:
        return sum([(i + 1) * g for i, g in enumerate(max_per_bp)])
    else:
        return prod(max_per_bp)


# on test input: 5s with pypy, 11s with CPython
print(f"part 1: {solve(blueprints)}")
print(f"part 2: {solve(blueprints, p2=True)}")
