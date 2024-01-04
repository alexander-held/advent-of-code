import fileinput

x = [line.strip() for line in fileinput.input()][0]

idx = 0
in_garbage = False
depth = 0
score = 0
num_garbage = 0

while idx < len(x):
    if x[idx] == "<" and not in_garbage:  # starting garbage
        in_garbage = True

    elif x[idx] == ">" and in_garbage:  # ending garbage
        in_garbage = False

    elif x[idx] == "{" and not in_garbage:  # starting group
        depth += 1

    elif x[idx] == "}" and not in_garbage:  # ending group
        score += depth
        depth -= 1

    elif x[idx] == "!":  # ignoring character
        idx += 1

    elif in_garbage:  # counting garbage
        num_garbage += 1

    idx += 1

print(f"part 1: {score}")
print(f"part 2: {num_garbage}")
