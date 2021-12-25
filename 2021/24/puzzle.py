import fileinput
import random

random.seed(0)

x = [line.strip() for line in fileinput.input()]

V0 = []  # first variable number, 1 or 26
V1 = []  # second variable number, -16 to 14
V2 = []  # third variable number, 1 to 14
for i in range(len(x) // 18):
    V0.append(int(x[i * 18 + 4].split()[2]))
    V1.append(int(x[i * 18 + 5].split()[2]))
    V2.append(int(x[i * 18 + 15].split()[2]))


def step_simplified(w, z, iteration):
    # instructions repeat 14 times, transcribed and simplified here
    # x, y are always initialized to zero again in each block
    # y is a temporary variable used twice and multiplied with / added to z only,
    # so y can be simplified away completely
    x = int((z % 26) + V1[iteration] != w)
    z //= V0[iteration]
    z *= (25 * x) + 1
    z += (w + V2[iteration]) * x
    return z


def run_all_steps(input):
    input_gen = (num for num in input)
    z = 0
    for i in range(14):
        z = step_simplified(next(input_gen), z, i)
    return z


def improve_input(input, threshold, num_fixed_left=0):
    # alter one input digit to get better result
    for i in range(num_fixed_left, 14):  # optionally leave left-most digits untouched
        for j in range(1, 10):
            input_tmp = input[:]
            input_tmp[i] = j
            z = run_all_steps(input_tmp)
            if z <= threshold and z > 0:  # try to improve further
                res = improve_input(input_tmp, threshold / 5, num_fixed_left)
                if res:
                    return res
            elif z == 0:
                print(f"=> found solution: {input_tmp}, z={z}")
                return input_tmp
    return None


def find_solutions(fixed_left, num_tries):
    solutions = []
    allowed_digits = [1, 2, 3, 4, 5, 6, 7, 8, 9]  # all inputs are digits 1-9
    for i in range(num_tries):
        if i % (num_tries // 20) == 0:
            print(f"{i/num_tries:.1%}")  # show progress
        input = fixed_left + random.choices(allowed_digits, k=14 - len(fixed_left))
        z = run_all_steps(input)
        if z == 0:
            print("=> already solved:", "".join(map(str, input)))
            solutions.append(input)
            break
        if z < 500:
            # close enough, try changing one digit at a time to improve
            res = improve_input(input, 250, len(fixed_left))
            if res:
                solutions.append(res)
    return solutions


# instructions (ideally run with pypy for speed)

# part 1
# fix digits from left to right, start by finding solutions starting with [9]
# with 100 Million attempts, largest solution is 949..., continue with that
# with 10 Million attempts and starting with [9,4,9], largest is 9499..
# with 10 Million attempts and starting with [9,4,9,9], largest is 9499299...
# with 10 Million attempts and starting with [9,4,9,9,2,9,9], largest is 94992992796199

# part 2:
# fix from left to right, starting with [1]
# with 10 Million attempts, smallest solution is 11..., continue with that
# with 10 Million attempts, and starting with [1,1], smallest is 119...
# with 10 Million attempts, and starting with [1,1,9], smallest is 11931...
# with 10 Million attempts, and starting with [1,1,9,3,1], smallest is 11931881141161

fixed_left = [1, 1, 9, 3, 1]
num_tries = 10_000_000

solutions = find_solutions(fixed_left, num_tries)
print("all solutions:")
for sol in sorted(solutions):
    print("".join(map(str, sol)))
