import fileinput
import math

x = [line.strip() for line in fileinput.input()]

rules = {}
for line in x:
    if ":" in line and "or" in line:
        name, values = line.split(":")
        values = [[int(r) for r in v.strip().split("-")] for v in values.split(" or ")]
        rules.update({name: values})

your_ticket = next(x[i+1] for i in range(len(x)) if "your ticket:" in x[i]).split(",")
your_ticket = [int(t) for t in your_ticket]
nearby_tickets = next(x[i+1:] for i in range(len(x)) if "nearby tickets:" in x[i])
nearby_tickets = [[int(t) for t in ticket.split(",")] for ticket in nearby_tickets]

val_nums = set()
for rule in rules.values():
    for i in range(2):
        val_nums = val_nums.union(range(rule[i][0], rule[i][1]+1))

error_rate = 0
valid_nearby = []  # valid tickets for part 2
for ticket in nearby_tickets:
    is_valid = True
    for n in ticket:
        if n not in val_nums:
            error_rate += n
            is_valid = False
    if is_valid:
        valid_nearby.append(ticket)

print(f"part 1: {error_rate}")

rules_per_type = []
rule_names = []
num_rules = len(your_ticket)
for name, rule in rules.items():
    rule_set = set()  # allowed values per rule
    for i in range(2):
        rule_set = rule_set.union(range(rule[i][0], rule[i][1]+1))
    rules_per_type.append(rule_set)
    rule_names.append(name)

rules_available = [True]*num_rules  # rules not yet assigned to column
cols_to_distribute = [True]*num_rules  # column not yet assigned to rule

col_names = [""]*num_rules
while "" in col_names:
    for t_col in range(num_rules):  # loop over columns in ticket
        if not cols_to_distribute[t_col]:  # column already assigned to rule
            continue

        vals_nearby_tickets = [v[t_col] for v in valid_nearby]  # column values
        possible_rules = []  # rules that match column

        for rule_idx in range(num_rules):  # loop over rules to see which match
            if not rules_available[rule_idx]:  # rule already used
                continue
            elif all([v in rules_per_type[rule_idx] for v in vals_nearby_tickets]):
                possible_rules.append(rule_idx)

        if len(possible_rules) == 1:  # unique rule matched to column
            col_names[t_col] = rule_names[possible_rules[0]]
            rules_available[possible_rules[0]] = False
            cols_to_distribute[t_col] = False

vals = [your_ticket[i] for i, cn in enumerate(col_names) if cn.startswith("departure")]
print(f"part 2: {math.prod(vals)}")
