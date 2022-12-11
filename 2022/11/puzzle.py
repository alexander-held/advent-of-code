import copy
import fileinput
import re
from collections import deque
from math import prod

x = "".join([line for line in fileinput.input()]).split("\n\n")


class Monkey:
    def __init__(self, op, num, divisor, target_true, target_false, items):
        self.op = op
        self.num = num
        self.divisor = divisor
        self.target_true = target_true
        self.target_false = target_false
        self.items_held = deque(items)
        self.num_inspected = 0

    def update(self, worry, modulo_val, p2=False):
        self.num_inspected += 1
        if self.op == "*":
            worry *= self.num
        elif self.op == "+":
            worry += self.num
        elif self.op == "**":
            worry *= worry
        if not p2:
            worry //= 3
        else:
            worry %= modulo_val  # take modulo with product of all values used in tests
        target = self.target_true if worry % self.divisor == 0 else self.target_false
        return target, worry


monkeys = []
for monkey in x:
    all_numbers = [int(n) for n in re.findall(r"\d+", monkey)]
    items = all_numbers[1:-4]  # worry level per item
    op = monkey.split()[-18]
    if "old * old" in monkey:  # handle squaring for updates
        op = "**"
        items.append(int(all_numbers[-4]))
    num, divisor, target_true, target_false = all_numbers[-4:]
    monkeys.append(Monkey(op, num, divisor, target_true, target_false, items))


def simulate(monkeys, num_rounds, p2=False):
    monkeys_sim = copy.deepcopy(monkeys)
    prod_dividers = prod([m.divisor for m in monkeys_sim])
    for _ in range(1, num_rounds + 1):
        for monkey in monkeys_sim:
            for _ in range(len(monkey.items_held)):
                target, item = monkey.update(
                    monkey.items_held.popleft(), modulo_val=prod_dividers, p2=p2
                )
                monkeys_sim[target].items_held.append(item)
    return prod(sorted([m.num_inspected for m in monkeys_sim])[-2:])


print(f"part 1: {simulate(monkeys, 20)}")
print(f"part 2: {simulate(monkeys, 10000, p2=True)}")
