import fileinput
import re

x = [line for line in fileinput.input()]

sensors = []
beacons = []
radii = []  # length in Manhattan distance around sensor where other beacons cannot be

for line in x:
    s_x, s_y, b_x, b_y = map(int, re.findall(r"-?\d+", line))
    sensors.append((s_x, s_y))
    beacons.append((b_x, b_y))
    radii.append(abs(s_x - b_x) + abs(s_y - b_y))


def blocked(x, y, sensors, beacons, radii):  # spot cannot contain additional beacon
    for i_s, (s_x, s_y) in enumerate(sensors):
        if abs(x - s_x) + abs(y - s_y) <= radii[i_s] and (x, y) not in beacons:
            return True
    return False


x_min = min([s[0] for s in sensors]) - max(radii)
x_max = max([s[0] for s in sensors]) + max(radii)
no_beacons = sum(
    blocked(x, 2000000, sensors, beacons, radii) for x in range(x_min, x_max)
)
print(f"part 1: {no_beacons}")


def find_p2(sensors, beacons, radii):
    # distress beacon position needs to be just outside signal ranges to be unique
    for i_s, (s_x, s_y) in enumerate(sensors):
        for dx in range(-radii[i_s], radii[i_s] + 1):
            dy = radii[i_s] - abs(dx) + 1  # one outside edge
            for hemisphere in [-1, 1]:
                pos_x = s_x + dx
                pos_y = s_y + dy * hemisphere
                if not (0 <= pos_x <= 4000000 and 0 <= pos_y <= 4000000):
                    continue  # outside of range
                elif (
                    not blocked(pos_x, pos_y, sensors, beacons, radii)
                    and (pos_x, pos_y) not in beacons
                ):
                    return pos_x * 4000000 + pos_y


# run this with pypy for ~10x speedup
print(f"part 2: {find_p2(sensors, beacons, radii)}")
