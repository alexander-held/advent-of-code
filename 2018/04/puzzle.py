import fileinput
import collections

x = sorted([line.strip() for line in fileinput.input()])

guards = collections.defaultdict(list)
minutes_asleep = []
for line in x:
    if "Guard" in line:
        if len(minutes_asleep):
            guards[guard_id] += minutes_asleep
            minutes_asleep = []  # reset
        guard_id = int(line.split()[-3].strip("#"))
    else:
        minute = int(line.split()[1].split(":")[1].strip("]"))
        if "falls asleep" in line:
            falls_asleep = minute
        elif "wakes up" in line:
            wakes_up = minute
            minutes_asleep += [m for m in range(falls_asleep, wakes_up)]
guards[guard_id] += minutes_asleep  # last entry


minutes_total = -1
for guard, minutes in guards.items():
    if len(minutes) > minutes_total:
        minutes_total = len(minutes)
        guard_times_minute = guard * collections.Counter(minutes).most_common(1)[0][0]

print(f"part 1: {guard_times_minute}")


times_asleep = -1
for guard, minutes in guards.items():
    minute, times = collections.Counter(minutes).most_common(1)[0]
    if times > times_asleep:
        times_asleep = times
        guard_times_minute = guard * minute

print(f"part 2: {guard_times_minute}")
