import collections

x = [10, 16, 6, 0, 1, 17]

for which_part in [("part 1", 2020), ("part 2", 30000000)]:
    counter = collections.Counter()
    last_seen = collections.defaultdict(int)

    for i, xi in enumerate(x):
        counter.update({xi: 1})
        last_seen.update({xi: i})

    last_num = x[-1]
    for i in range(len(x), which_part[1]):
        if counter[last_num] == 1:
            next_num = 0
        else:
            next_num = i - last_seen[last_num] - 1

        counter.update({next_num: 1})
        last_seen.update({last_num: i - 1})
        last_num = next_num

    print(f"{which_part[0]}: {next_num}")
