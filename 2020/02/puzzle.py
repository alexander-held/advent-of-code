# run: python puzzle.py < input.txt
import fileinput

x = [line for line in fileinput.input()]
range_low = [int(xi.split()[0].split("-")[0]) for xi in x]
range_high = [int(xi.split()[0].split("-")[1]) for xi in x]
letters = [xi.split()[1].strip(":") for xi in x]
pws = [xi.split(":")[-1].strip() for xi in x]

# part 1
valid = 0
for i, pw in enumerate(pws):
    count = pw.count(letters[i])
    if count >= range_low[i] and count <= range_high[i]:
        valid += 1
print(valid)

# part 2
valid = 0
for i, pw in enumerate(pws):
    if (pw[range_low[i]-1] == letters[i]) != (pw[range_high[i]-1] == letters[i]):
        valid += 1
print(valid)
