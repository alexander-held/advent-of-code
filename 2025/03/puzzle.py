import fileinput

x = [line.strip() for line in fileinput.input()]


def get_largest(bank, num_b, digits):
    if num_b == 0:
        return int(digits)
    idx = max(range(0, len(bank) - (num_b - 1)), key=lambda i: bank[i])
    return get_largest(bank[idx + 1 :], num_b - 1, digits + bank[idx])


print(f"part 1: {sum(get_largest(bank, 2, "") for bank in x)}")
print(f"part 2: {sum(get_largest(bank, 12, "") for bank in x)}")
