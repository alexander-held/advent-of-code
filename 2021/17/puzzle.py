import fileinput
import re

x_min, x_max, y_min, y_max = map(int, re.findall("-?\d+", fileinput.input().readline()))

max_height_overall = 0
num_hits = 0
for vel_x in range(0, x_max + 1):  # overshoot if speed is higher than x_max
    for vel_y in range(y_min, -y_min):  # overshoot if speed is higher than -y_min-1
        pos = [0, 0]
        vel = [vel_x, vel_y]
        max_height = 0

        while pos[1] >= y_min:
            pos = [pos[0] + vel[0], pos[1] + vel[1]]
            vel[0] += -1 * (vel[0] > 0) + 1 * (vel[0] < 0)  # 1 step towards 0
            vel[1] -= 1
            max_height = max(max_height, pos[1])
            if x_min <= pos[0] <= x_max and y_min <= pos[1] <= y_max:
                max_height_overall = max(max_height_overall, max_height)
                num_hits += 1
                break

print(f"part 1: {max_height_overall}")
print(f"part 2: {num_hits}")
