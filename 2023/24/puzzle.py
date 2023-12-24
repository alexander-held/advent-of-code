import fileinput
from itertools import combinations

import sympy

x = [line for line in fileinput.input()]

hailstones = []
for line in x:
    px, py, pz, vx, vy, vz = map(int, line.replace("@", ",").split(", "))
    hailstones.append({"px": px, "py": py, "pz": pz, "vx": vx, "vy": vy, "vz": vz})

target = (200000000000000, 400000000000000)
num_within_test_area = 0
for comb in combinations(hailstones, 2):
    h1, h2 = comb
    # calculate p1 + t1*v1 = p2 + t2*v2, solve for t1 (time for A to intersect with B)
    denom = h1["vy"] - h2["vy"] / h2["vx"] * h1["vx"]
    if denom == 0:
        continue  # parallel paths

    # solve for time
    t1 = 1 / denom * (h2["py"] - h1["py"] + h2["vy"] / h2["vx"] * (h1["px"] - h2["px"]))
    t2 = (h1["px"] - h2["px"] + t1 * h1["vx"]) / h2["vx"]

    if t1 < 0 or t2 < 0:
        continue  # intersection lies in the past

    px_inter = h1["px"] + t1 * h1["vx"]  # intersection
    py_inter = h1["py"] + t1 * h1["vy"]

    if target[0] <= px_inter <= target[1] and target[0] <= py_inter <= target[1]:
        num_within_test_area += 1

print(f"part 1: {num_within_test_area}")

# part 2: rock at \vec{p_0} with \vec{v_0}, hailstones at \vec{p_i} with \vec{v_i}
# then for each hailstone i: \vec{p_0} - \vec{p_i} = -t [\vec{v_0} - \vec{v_i}]
# cross product to eliminate time
# [\vec{p_0} - \vec{p_i}] \cross [\vec{v_0 - v_i}] = 0
# solve this simultaneously for multiple hailstones
# in principle this is 3 equations per hailstone and 6 unknowns total, but in practice
# 2 hailstones are not enough to solve, there must be some degeneracy

# symbols for rock (to solve for)
px0, py0, pz0, vx0, vy0, vz0 = sympy.symbols("px0,py0,pz0,vx0,vy0,vz0")
p0, v0 = sympy.Matrix([px0, py0, pz0]), sympy.Matrix([vx0, vy0, vz0])

to_vec = lambda h, ch: sympy.Matrix([h[f"{ch}x"], h[f"{ch}y"], h[f"{ch}z"]])

equations = []
for i in range(3):
    pi, vi = to_vec(hailstones[i], "p"), to_vec(hailstones[i], "v")  # hailstone vectors
    # equations to solve: vanishing cross products for rock with hailstones
    equations.append((p0 - pi).cross(v0 - vi))

res = sympy.solve(equations, [px0, py0, pz0, vx0, vy0, vz0], dict=True)
print(f"part 2: {res[0][px0] + res[0][py0] + res[0][pz0]}")
