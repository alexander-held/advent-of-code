import fileinput
from collections import defaultdict

x = [line.strip() for line in fileinput.input()]
init_pos = []
target_pos = []
for line in x:
    init_pos.append([int(y) for y in line.split(" -> ")[0].split(",")])
    target_pos.append([int(y) for y in line.split(" -> ")[1].split(",")])


def direction(increasing):
    return 1 - 2 * (not increasing)


def count_overlap(diag=False):
    field = defaultdict(int)

    for init, tar in zip(init_pos, target_pos):
        inc_x = init[0] < tar[0]  # increasing range in x
        inc_y = init[1] < tar[1]  # increasing range in y

        if init[1] == tar[1]:  # horizontal
            for pos_x in range(init[0], tar[0] + direction(inc_x), direction(inc_x)):
                field[pos_x, init[1]] += 1

        elif init[0] == tar[0]:  # vertical
            for pos_y in range(init[1], tar[1] + direction(inc_y), direction(inc_y)):
                field[init[0], pos_y] += 1

        elif diag:  # 45 degree diagonal
            for pos_x in range(init[0], tar[0] + direction(inc_x), direction(inc_x)):
                pos_y = init[1] + abs(init[0] - pos_x) * direction(inc_y)
                field[pos_x, pos_y] += 1

    return len([val for val in field.values() if val > 1])


print(f"part 1: {count_overlap(diag=False)}")
print(f"part 2: {count_overlap(diag=True)}")
