import fileinput
from collections import defaultdict

x = list(map(int, "".join([line.strip() for line in fileinput.input()]).split()))

stone_dict = defaultdict(int)
for stone in x:
    stone_dict[stone] += 1


def blink(stone_dict, num_blinks):
    for _ in range(num_blinks):
        new_stone_dict = defaultdict(int)
        for stone, num in stone_dict.items():
            if stone == 0:
                new_stone_dict[1] += num
            elif len(str(stone)) % 2 == 0:
                new_stone_dict[int(str(stone)[: len(str(stone)) // 2])] += num
                new_stone_dict[int(str(stone)[len(str(stone)) // 2 :])] += num
            else:
                new_stone_dict[stone * 2024] += num

        stone_dict = new_stone_dict
    return sum(stone_dict.values())


print(f"part 1: {blink(stone_dict, 25)}")
print(f"part 2: {blink(stone_dict, 75)}")
