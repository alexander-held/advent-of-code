import fileinput
import re

x = [line.strip() for line in fileinput.input()]


def count_tokens(p2=False):
    num_tokens = 0
    for i_block in range(len(x) // 4 + 1):
        a_x, a_y = map(int, re.findall(r"\d+", x[i_block * 4]))
        b_x, b_y = map(int, re.findall(r"\d+", x[i_block * 4 + 1]))
        prize_x, prize_y = map(int, re.findall(r"\d+", x[i_block * 4 + 2]))

        if p2:
            prize_x += 10000000000000
            prize_y += 10000000000000

        Na = (prize_x - b_x / b_y * prize_y) / (a_x - b_x / b_y * a_y)
        Nb = (prize_y - a_y * Na) / b_y

        if abs(Na - round(Na)) < 1e-3 and abs(Nb - round(Nb)) < 1e-3:
            num_tokens += 3 * Na + Nb

    return round(num_tokens)


print(f"part 1: {count_tokens()}")
print(f"part 2: {count_tokens(p2=True)}")
