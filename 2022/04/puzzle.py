import fileinput

x = [line.strip() for line in fileinput.input()]

overlap_p1, overlap_p2 = 0, 0
for pair in x:
    sec1, sec2 = pair.split(",")
    sec1_l, sec1_r = map(int, sec1.split("-"))
    sec2_l, sec2_r = map(int, sec2.split("-"))

    if sec1_l <= sec2_l and sec1_r >= sec2_r or sec1_l >= sec2_l and sec1_r <= sec2_r:
        overlap_p1 += 1

    if sec1_r >= sec2_l and sec1_l <= sec2_l or sec2_r >= sec1_l and sec2_l <= sec1_l:
        overlap_p2 += 1

print(f"part 1: {overlap_p1}")
print(f"part 2: {overlap_p2}")
