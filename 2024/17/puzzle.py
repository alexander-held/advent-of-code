import fileinput
import re

x = "".join([line for line in fileinput.input()])
a, b, c, *program = map(int, re.findall(r"\d+", x))


def run_prog(a, b, c, program):
    combo = lambda val: {0: 0, 1: 1, 2: 2, 3: 3, 4: a, 5: b, 6: c}[val]
    ip = 0  # instruction pointer
    out = ""
    while ip < len(program):
        instruction = program[ip]
        operand = program[ip + 1]

        match instruction:
            case 0:  # adv
                a = int(a / (2 ** (combo(operand))))
            case 1:  # bxl
                b ^= operand
            case 2:  # bst
                b = combo(operand) % 8
            case 3:  # jnz
                if a != 0:
                    ip = operand
            case 4:  # bxc
                b ^= c
            case 5:  # out
                out += f"{combo(operand) % 8},"
            case 6:  # bdv
                b = int(a / (2 ** (combo(operand))))
            case 7:  # cdv
                c = int(a / (2 ** (combo(operand))))

        if instruction != 3 or a == 0:
            ip += 2  # move forward

    return out[:-1]


# part 2 notes from experimenting:
# - need to produce 16 digits -> input must be in interval [8**15, 8**16-1]
# - check outputs for inputs in base8: repeating pattern
#   - last digit printed depends on first 3 input bits (one char in base-8)
#   - pick a value that produces the correct last digit
#   - repeat this process for all digits to get possible solutions
def find_solutions(b, c, program):
    solutions = []
    valid_inputs = ["0o"]
    while len(valid_inputs):
        reg_a = valid_inputs.pop()
        if len(reg_a) > 18:
            continue  # output too long
        for val in range(0, 8):  # find all settings that produce the right output tail
            out = [
                int(v)
                for v in run_prog(int(f"{reg_a}{val}", 8), b, c, program).split(",")
            ]
            if out == program:
                solutions.append(int(f"{reg_a}{val}", 8))
            elif out == program[-len(out) :]:
                valid_inputs.append(f"{reg_a}{val}")  # last digits match
    return solutions


print(f"part 1: {run_prog(a, b, c, program)}")
print(f"part 2: {min(find_solutions(b, c, program))}")
