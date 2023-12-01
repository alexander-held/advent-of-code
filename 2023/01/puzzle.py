import fileinput
import re

x = [line.strip() for line in fileinput.input()]


def get_calib_sum(x, part_2=False):
    if not part_2:
        pattern = "(\d)"
    else:
        pattern = "(\d|one|two|three|four|five|six|seven|eight|nine|ten)"

    str_to_int = dict(
        zip(
            ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine"),
            range(1, 10),
        )
    )

    calib_sum = 0
    for line in x:
        matches = re.findall(f"(?={pattern})", line)
        for match, mult in zip((matches[0], matches[-1]), (10, 1)):
            calib_sum += (int(match) if match.isdigit() else str_to_int[match]) * mult
    return calib_sum


print(f"part 1: {get_calib_sum(x)}")
print(f"part 2: {get_calib_sum(x, part_2=True)}")
