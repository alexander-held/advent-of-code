import fileinput

import scipy.optimize

x = [line for line in fileinput.input()]

monkeys = {}
for line in x:
    name, instr = line.split(": ")
    if any([char in instr for char in "+-*/"]):
        monkeys.update({name: instr.split()})
    else:
        monkeys.update({name: int(instr)})


def get_monkey_val(monkey_name, all_monkeys):
    if isinstance(all_monkeys[monkey_name], int):
        return all_monkeys[monkey_name], all_monkeys
    else:
        name_1, op, name_2 = all_monkeys[monkey_name]
        arg_1, all_monkeys = get_monkey_val(name_1, all_monkeys)
        arg_2, all_monkeys = get_monkey_val(name_2, all_monkeys)
        if op == "+":
            res = arg_1 + arg_2
        elif op == "-":
            res = arg_1 - arg_2
        elif op == "*":
            res = arg_1 * arg_2
        elif op == "/":
            res = arg_1 / arg_2
        all_monkeys[monkey_name] = res
        return res, all_monkeys


print(f"part 1: {int(get_monkey_val('root', monkeys.copy())[0])}")


def get_offset(val_to_yell, monkeys):
    root_monkeys = [monkeys["root"][0], monkeys["root"][-1]]
    res = []
    for val in val_to_yell:
        monkeys_copy = monkeys.copy()
        monkeys_copy["humn"] = int(val)
        _, monkeys_res = get_monkey_val("root", monkeys_copy)
        res.append(monkeys_res[root_monkeys[0]] - monkeys_res[root_monkeys[1]])
    return res


res = scipy.optimize.root(get_offset, x0=10e6, args=(monkeys))  # root finding
assert res.success is True  # starting x0 value may need tuning if this fails
print(f"part 2: {int(res.x[0])}")
