import fileinput
import lark

grammar, messages = "".join([line for line in fileinput.input()]).split("\n\n")

# for reference: https://lark-parser.readthedocs.io/en/latest/grammar.html
# grammar consists of lowercase rules (part 2: terminals do not support recursion)
transl = grammar.maketrans("0123456789", "abcdefghij")
grammar = grammar.translate(transl)
grammar = grammar + "\nstart: a"  # need to find messages matching first rule


def count_valid(parser, messages):
    valid = 0
    for sentence in messages.split():
        try:
            parser.parse(sentence)
            valid += 1
        except:
            ...  # invalid sentence

    return valid


print(f"part 1: {count_valid(lark.Lark(grammar), messages)} valid messages")


# part 2
grammar = grammar.replace(
    "8: 42".translate(transl), "8: 42 | 42 8".translate(transl)
)
grammar = grammar.replace(
    "11: 42 31".translate(transl), "11: 42 31 | 42 11 31".translate(transl)
)

print(f"part 2: {count_valid(lark.Lark(grammar), messages)} valid messages")
