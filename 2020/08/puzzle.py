import fileinput

x = [line.strip().split() for line in fileinput.input()]
program = [(op, int(arg)) for op, arg in x]

def run(program):
    acc = 0
    idx = 0
    idx_seen = set()

    while idx < len(program):
        if idx in idx_seen:
            return (acc, "stuck_in_loop")
        idx_seen.add(idx)
        op, arg = program[idx]
        if op == "acc":
            acc += arg
            idx += 1
        elif op == "jmp":
            idx += arg
        elif op == "nop":
            idx += 1

    return (acc, "terminated")

# part 1
print(run(program))

# part 2
for i in range(len(x)):
    # exchange one nop to jmp or jmp to nop
    if program[i][0] == "jmp":
        op = "nop"
    elif program[i][0] == "nop":
        op = "jmp"
    else:
        continue

    program_edit = program[:i] + [(op, program[i][1])] + program[i+1:]
    result = run(program_edit)

    if result[1] == "terminated":
        print(result)
