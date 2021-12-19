import fileinput
import math
import re
from collections import Counter
from itertools import permutations

x = [line.strip().replace(" ", "") for line in fileinput.input()]


def _str_repl(string: str, idx_start: int, idx_stop: int, new_chars: str) -> str:
    return string[:idx_start] + new_chars + string[idx_stop:]


def explode(expression: str, start: int, stop: int) -> str:
    # edit from right to left to not change relevant indices for subsequent edits
    pair_to_explode = tuple(map(int, expression[start + 1 : stop - 1].split(",")))

    nums_right = re.search("\d+", expression[stop:])  # numbers to the right
    if nums_right:
        idx_start = nums_right.start() + stop
        idx_end = nums_right.end() + stop
        new_num_right = str(int(nums_right.group()) + int(pair_to_explode[1]))
        expression = _str_repl(expression, idx_start, idx_end, new_num_right)

    expression = expression[:start] + "0" + expression[stop:]  # remove exploded pair

    nums_left = re.search("\d+", expression[:start][::-1])  # numbers to the left
    if nums_left:
        idx_start = start - nums_left.end()
        idx_end = start - nums_left.start()
        # since we searched through reversed list, need to flip number again here
        new_num_left = str(int(nums_left.group()[::-1]) + int(pair_to_explode[0]))
        expression = _str_repl(expression, idx_start, idx_end, new_num_left)

    return expression


def split(expression: str, num: int) -> str:
    match = re.search(str(num), expression)  # match is guaranteed when split is called
    new_pair = "[" + str(num // 2) + "," + str(math.ceil(num / 2)) + "]"
    return expression[: match.start()] + new_pair + expression[match.end() :]


def reduce_once(expression: str) -> str:
    # explode when possible, otherwise try to split, return changed expression
    depth = 0
    for i, char in enumerate(expression):
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1

        if depth >= 5:  # explode leftmost simple pair
            idx_closing = i + expression[i:].find("]")  # position of closing bracket
            if Counter(expression[i + 1 : idx_closing])["["] > 0:
                continue  # not simple pair yet, go deeper
            return explode(expression, i, i + expression[i:].find("]") + 1)

    # split leftmost number if possible
    nums_gt_10 = [num for num in map(int, re.findall("\d+", expression)) if num >= 10]
    if nums_gt_10:
        expression = split(expression, nums_gt_10[0])

    return expression


def reduce_num(expression: str) -> str:
    while True:  # keep reducing until reduction does not change expression anymore
        new_expr = reduce_once(expression)
        if new_expr == expression:
            return expression
        expression = new_expr


def add_numbers(numbers: list) -> str:
    result = numbers[0]
    for i in range(len(numbers) - 1):
        result = "[" + result + "," + numbers[i + 1] + "]"
        result = reduce_num(result)  # reduce before adding further
    return result


def get_magnitude(expression: str) -> int:
    while "[" in expression:
        match = re.search("\[\d+,\d+\]", expression)
        nums = [num for num in map(int, match.group()[1:-1].split(","))]
        magnitude = 3 * nums[0] + 2 * nums[1]
        expression = _str_repl(expression, match.start(), match.end(), str(magnitude))
    return int(expression)


print(f"part 1: {get_magnitude(reduce_num(add_numbers(x)))}")

max_magnitude = 0
for nums in permutations(x, 2):
    max_magnitude = max(max_magnitude, get_magnitude(reduce_num(add_numbers(nums))))
print(f"part 2: {max_magnitude}")


RUN_TESTS = False
if RUN_TESTS:
    import test_cases

    for test in test_cases.tests_reduce_all():
        assert reduce_num(test[0]) == test[1]

    for test in test_cases.tests_add_and_reduce():
        assert reduce_num(add_numbers(test[0])) == test[1]

    for test in test_cases.test_magnitude():
        assert get_magnitude(test[0]) == test[1]
