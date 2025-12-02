import fileinput

x = [line.split(",") for line in fileinput.input()][0]

sum_invalid_p1 = 0
sum_invalid_p2 = 0
for entry in x:
    first, last = map(int, entry.split("-"))
    for num in range(first, last + 1):
        s = str(num)
        if s[len(s) // 2 :] == s[: len(s) // 2]:
            sum_invalid_p1 += num
        for sl in range(1, len(s) // 2 + 1):
            if len(s) % sl == 0:  # only use divisors of num as segment length
                segments = [s[i * sl : (i + 1) * sl] for i in range(len(s) // sl)]
                if len(set(segments)) == 1:  # all segments equal
                    sum_invalid_p2 += num
                    break

print(f"part 1: {sum_invalid_p1}")
print(f"part 2: {sum_invalid_p2}")
