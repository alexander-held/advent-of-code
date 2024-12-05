import fileinput
from collections import defaultdict

x = [line for line in fileinput.input()]

text = defaultdict(str)
for i, line in enumerate(x):
    for j, char in enumerate(line):
        text[i + 1j * j] = char

num_xmas = 0
num_mas = 0
for a in range(len(x)):
    for b in range(len(x[0])):
        if text[a + 1j * b] == "X":
            for direction in (1j, -1j, 1, -1, -1 + 1j, 1 + 1j, 1 - 1j, -1 - 1j):
                if (
                    text[a + 1j * b + 1 * direction]
                    + text[a + 1j * b + 2 * direction]
                    + text[a + 1j * b + 3 * direction]
                    == "MAS"
                ):
                    num_xmas += 1

        elif text[a + 1j * b] == "A":
            if (
                text[a - 1 + 1j * (b - 1)]  # top left
                + text[a - 1 + 1j * (b + 1)]  # top right
                + text[a + 1 + 1j * (b + 1)]  # bottom right
                + text[a + 1 + 1j * (b - 1)]  # bottom left
            ) in ["MMSS", "SMMS", "SSMM", "MSSM"]:
                num_mas += 1

print(f"part 1: {num_xmas}")
print(f"part 2: {num_mas}")
