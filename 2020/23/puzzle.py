def move(cups):
    cur_cup = cups[0]
    pick_up = cups[1:4]
    cups_left = cups[4:]

    dest_cup_label = cur_cup - 1
    while dest_cup_label not in cups_left:
        dest_cup_label -= 1
        if dest_cup_label < min(cups):
            dest_cup_label = max(cups)

    dest_idx = cups_left.index(dest_cup_label)  # index in remaining cups
    return cups_left[: dest_idx + 1] + pick_up + cups_left[dest_idx + 1 :] + [cur_cup]


cups = [int(x) for x in "643719258"]

for _ in range(100):
    cups = move(cups)

idx_1 = cups.index(1)
part_1 = "".join([str(c) for c in cups[idx_1 + 1 :]] + [str(c) for c in cups[:idx_1]])
print(f"part 1: {part_1}")


def move_p2(cup_dict, cur_cup):
    pick_up = []
    _cup = cur_cup
    for _ in range(3):  # pick up three cups
        _cup = cup_dict[_cup]
        pick_up.append(_cup)

    # next cup after current cup is cup that comes after the cups that were picked up
    cup_dict[cur_cup] = cup_dict[_cup]

    dest_cup_label = cur_cup - 1
    if dest_cup_label == 0:
        dest_cup_label = 1_000_000
    while dest_cup_label in pick_up:  # all numbers are either picked up or left
        dest_cup_label -= 1
        if dest_cup_label < 1:  # hardcode min/max for performance
            dest_cup_label = 1_000_000

    # last picked up cup needs to point to old cup the destination cup pointed to
    cup_dict[pick_up[2]] = cup_dict[dest_cup_label]

    # destination cup needs to point to first picked up cup
    cup_dict[dest_cup_label] = pick_up[0]

    return cup_dict


def create_cup_dict(cups):
    """dictionary for better performance, key: label, value: next label"""
    cdict = {}
    for i, cup in enumerate(cups[:-1]):
        cdict.update({cup: cups[i + 1]})
    cdict.update({cups[-1]: cups[0]})
    return cdict


cups = [int(x) for x in "643719258"] + [i for i in range(10, 1_000_000 + 1)]

cup_dict = create_cup_dict(cups)
cur_cup = cups[0]
for _ in range(10_000_000):
    cup_dict = move_p2(cup_dict, cur_cup)
    cur_cup = cup_dict[cur_cup]

print(f"part 2: {cup_dict[1]*cup_dict[cup_dict[1]]}")
