import fileinput

x = [list(map(int, line.split())) for line in fileinput.input()]


def is_unsafe(levels):
    diff = [levels[idx + 1] - levels[idx] for idx in range(len(levels) - 1)]
    # check that all are increasing or decreasing and all are 1<=abs(diff)<=3
    return (min(diff) < 0 and max(diff) > 0) or (set(diff) - {-3, -2, -1, 1, 2, 3})


print(f"part 1: {sum([not is_unsafe(report) for report in x])}")


num_safe_p2 = 0
for report in x:
    for idx in range(len(report)):  # drop one level at a time
        if not is_unsafe(report[:idx] + report[idx + 1 :]):
            num_safe_p2 += 1
            break

print(f"part 2: {num_safe_p2}")
