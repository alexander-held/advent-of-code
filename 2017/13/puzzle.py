import fileinput
from itertools import count

x = [line for line in fileinput.input()]

scanners = dict()
for line in x:
    depth, range_ = line.split(": ")
    scanners[int(depth)] = int(range_)


def simulate(scanners, delay=0, exit_on_detect=False):
    packet_pos = -1
    severity = 0
    for t in range(max(scanners.keys()) + 1):
        packet_pos += 1  # packet moves first
        scanner_range = scanners.get(packet_pos, None)  # look for scanner at packet pos
        if scanner_range:
            if (t + delay) % (2 * (scanner_range - 1)) == 0:  # detection
                severity += packet_pos * scanner_range
                if exit_on_detect:
                    return None  # optionally exit early upon detection
    return severity  # return severity by default


print(f"part 1: {simulate(scanners)}")

for delay in count(1):
    if simulate(scanners, delay=delay, exit_on_detect=True) is not None:
        break  # stop when no detection occurred

print(f"part 2: {delay}")  # ~1s with pypy
