import fileinput

x = [line.split() for line in fileinput.input()]

print(f"part 1: {sum([len(set(line)) == len(line) for line in x])}")

valid_p2 = sum([len(set("".join(sorted(w)) for w in line)) == len(line) for line in x])
print(f"part 2: {valid_p2}")
