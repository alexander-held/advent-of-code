import fileinput

x = [line.strip() for line in fileinput.input()]

error_score = 0
scores = []
for line in x:
    stack = []
    invalid = False
    for char in line:
        if char in ["(", "[", "{", "<"]:
            stack.append(char)
        else:
            if char == {"(": ")", "[": "]", "{": "}", "<": ">"}[stack[-1]]:
                stack.pop()
            else:
                error_score += {")": 3, "]": 57, "}": 1197, ">": 25137}[char]
                invalid = True
                break

    if not invalid:
        tot_score = 0
        for left_to_close in stack[::-1]:
            tot_score = 5 * tot_score + {"(": 1, "[": 2, "{": 3, "<": 4}[left_to_close]
        scores.append(tot_score)

print(f"part 1: {error_score}")
print(f"part 2: {sorted(scores)[len(scores)//2]}")
