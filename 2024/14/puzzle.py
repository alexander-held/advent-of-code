import fileinput
import re

x = [line.strip() for line in fileinput.input()]

rpos = []  # positions
rvel = []  # velocities
for line in x:
    px, py, vx, vy = map(int, re.findall(r"-?\d+", line))
    rpos.append(px + 1j * py)
    rvel.append(vx + 1j * vy)

MAX_X = 101
MAX_Y = 103

for step in range(10_000):
    for i in range(len(rpos)):
        new_pos = rpos[i] + rvel[i]
        rpos[i] = new_pos.real % MAX_X + 1j * (new_pos.imag % MAX_Y)

    if step == 99:
        num_q1 = sum([1 for r in rpos if r.real < MAX_X // 2 and r.imag < MAX_Y // 2])
        num_q2 = sum([1 for r in rpos if r.real > MAX_X // 2 and r.imag < MAX_Y // 2])
        num_q3 = sum([1 for r in rpos if r.real < MAX_X // 2 and r.imag > MAX_Y // 2])
        num_q4 = sum([1 for r in rpos if r.real > MAX_X // 2 and r.imag > MAX_Y // 2])

    if len(set(rpos)) == len(rpos):  # find step when no robots overlap
        str_out = ""
        for py in range(MAX_Y):
            for px in range(MAX_X):
                str_out += "■" if any([1 for r in rpos if r == px + 1j * py]) else " "
            str_out += "\n"
        print(str_out)  # check output to verify tree present

        num_steps_p2 = step + 1

print(f"part 1: {num_q1*num_q2*num_q3*num_q4}")
print(f"part 2: {num_steps_p2}")
