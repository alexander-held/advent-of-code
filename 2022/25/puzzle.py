import fileinput

x = [line.strip() for line in fileinput.input()]

to_10 = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
to_snafu = {v: k for k, v in to_10.items()}
base_10 = [sum(5**i * to_10[char] for i, char in enumerate(num[::-1])) for num in x]


def translate_to_snafu(num, snafu_str=""):
    if num > 0:
        snafu_str += to_snafu[((num + 2) % 5) - 2]
        snafu_str = translate_to_snafu((num + 2) // 5, snafu_str=snafu_str)
    return snafu_str[::-1]


print(f"part 1: {translate_to_snafu(sum(base_10))}")
