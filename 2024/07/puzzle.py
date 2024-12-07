import fileinput
from functools import reduce
from itertools import product
from math import prod

x = [line for line in fileinput.input()]


def get_calibration(funcs_to_use):
    calibration = 0
    for line in x:
        left, right = line.split(":")
        numbers = list(map(int, right.split()))
        for operators in product(funcs_to_use, repeat=len(numbers) - 1):
            op_iter = iter(operators)
            res = reduce(lambda l, r: next(op_iter)((l, r)), numbers)
            if res == int(left):
                calibration += res
                break
    return calibration


conc = lambda inp: int(f"{inp[0]}{inp[1]}")

print(f"part 1: {get_calibration((sum, prod))}")
print(f"part 2: {get_calibration((sum, prod, conc))}")
