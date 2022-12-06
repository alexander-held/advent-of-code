import fileinput

x = "".join([line.strip() for line in fileinput.input()])


def get_pos(message, n_chars):
    for i_pos in range(n_chars, len(message)):
        if len(set(message[i_pos - n_chars : i_pos])) == n_chars:
            return i_pos


print(f"part 1: {get_pos(x, 4)}")
print(f"part 2: {get_pos(x, 14)}")
