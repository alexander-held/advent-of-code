def read_input(fname):
    with open(fname) as f:
        lines = f.readlines()
    x = [int(l) for l in lines]
    return x

def sum_to_2020(x):
    for val in x:
        val_needed = 2020-val
        if val_needed in x:
            print(f"{val}, {val_needed}")
            return [val, val_needed]

def three_to_2020(x):
    for val_1 in x:
        val_max = 2020-val_1
        for val_2 in x:
            if val_2 > val_max:
                continue
            val_3 = 2020-val_1-val_2
            if val_3 in x:
                print(f"{val_1}, {val_2}, {val_3}")
                return [val_1, val_2, val_3]

if __name__ == "__main__":
    # part 1
    x = read_input("input.txt")
    y = sum_to_2020(x)
    print(f"{y[0]*y[1]}")

    # part 2
    x = read_input("input.txt")
    y = three_to_2020(x)
    print(f"{y[0]*y[1]*y[2]}")
