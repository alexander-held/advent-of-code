import fileinput

x = [int(line.strip()) for line in fileinput.input()]
x.sort()

x += [max(x)+3]  # add device at end of adapter list
cur_jolt = 0
diffs = []
while cur_jolt < max(x):
    next_jolt = next(xi for xi in x if xi > cur_jolt)
    diffs.append(next_jolt - cur_jolt)
    cur_jolt = next_jolt

print(f"part 1: {diffs.count(1)*diffs.count(3)}")


# part 2, go in reverse through adapters down until 0
x = [0] + x
paths = {max(x): 1}  # how many paths can be taken above given adapter
for adapter in x[::-1][1:]:  # skip last entry, already pre-filled in line above
    next_adapters = [xi for xi in x if (0 < xi - adapter <= 3)]  # possible next choices
    paths_above = [paths[n_a] for n_a in next_adapters]  # number of paths to take
    paths.update({adapter: sum(paths_above)})
    if adapter == 0:
        print(f"{sum(paths_above)} adapter paths above {adapter} jolts")
