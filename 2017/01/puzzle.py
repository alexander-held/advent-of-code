import fileinput

x = [line.strip() for line in fileinput.input()][0]

res_p1 = sum(int(x[i]) for i in range(len(x)) if x[i] == x[(i + 1) % len(x)])
res_p2 = sum(int(x[i]) for i in range(len(x)) if x[i] == x[(i - len(x) // 2) % len(x)])

print(f"part 1: {res_p1}")
print(f"part 2: {res_p2}")
