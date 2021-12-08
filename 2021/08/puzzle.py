import fileinput
from itertools import permutations

x = [line.strip() for line in fileinput.input()]
all_signals = [line.split(" | ")[0].split() for line in x]
all_out = [line.split(" | ")[1].split() for line in x]

print(f"part 1: {sum(sum(len(sig) in [2,4,3,7] for sig in line) for line in all_out)}")

sum_output = 0
all_letters = "abcdefg"
translate_to_num = {
    "abcefg": 0,
    "cf": 1,
    "acdeg": 2,
    "acdfg": 3,
    "bcdf": 4,
    "abdfg": 5,
    "abdefg": 6,
    "acf": 7,
    "abcdefg": 8,
    "abcdfg": 9,
}
for signals, outputs in zip(all_signals, all_out):
    scramble = permutations(all_letters, 7)
    for scram in scramble:
        translation = str.maketrans(all_letters, "".join(scram))
        translate = lambda word: "".join(sorted(word.translate(translation)))

        translation_is_good = True
        for sig in signals:
            if translate(sig) not in translate_to_num.keys():
                translation_is_good = False
                break
        if not translation_is_good:
            continue

        output_numbers = [translate_to_num[translate(outval)] for outval in outputs]
        sum_output += int("".join(map(str, output_numbers)))

print(f"part 2: {sum_output}")
