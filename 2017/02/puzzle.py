import fileinput
from itertools import permutations

x = [list(map(int, line.strip().split())) for line in fileinput.input()]

checksum = sum(max(line) - min(line) for line in x)
sum_p2 = 0
for line in x:
    for num1, num2 in permutations(line, 2):
        if num1 % num2 == 0:
            sum_p2 += num1 // num2

print(f"part 1: {checksum}")
print(f"part 2: {sum_p2}")
