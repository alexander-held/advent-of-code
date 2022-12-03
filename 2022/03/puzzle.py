import fileinput

x = [line.strip() for line in fileinput.input()]

priority = lambda char: ord(char) - 65 + 27 if char.isupper() else ord(char) - 96

prios = 0
for line in x:
    mid = len(line) // 2
    prios += priority(set.intersection(set(line[:mid]), set(line[mid:])).pop())
print(f"part 1: {prios}")

prios = 0
for i in range(len(x) // 3):
    prios += priority(set.intersection(*(set(r) for r in x[i * 3 : i * 3 + 3])).pop())
print(f"part 2: {prios}")
