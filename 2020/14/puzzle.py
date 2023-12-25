import fileinput

x = [line.strip() for line in fileinput.input()]

memory = {}
for line in x:
    if "mask" in line:
        bitmask = line.split("= ")[-1]
    else:
        addr, val = line.split(" = ")
        addr = addr.split("[")[-1].replace("]", "")
        res = int(bitmask.replace("X", "0"), 2)
        res |= int(bitmask.replace("X", "1"), 2) & int(val)
        memory.update({addr: res})

print(f"part 1: {sum(memory.values())}")

# part 2
memory = {}
for line in x:
    if "mask" in line:
        bitmask = line.split("= ")[-1]
    else:
        addr, val = line.split(" = ")
        addr = addr.split("[")[-1].replace("]", "")
        addr_bin = bin(int(addr))[2:].zfill(len(bitmask))
        new_addr = ["0"]*len(bitmask)
        for i in range(len(bitmask)):
            if bitmask[i] == "0":
                new_addr[i] = addr_bin[i]
            elif bitmask[i] == "1":
                new_addr[i] = "1"
            elif bitmask[i] == "X":
                new_addr[i] = "X"
        new_addr = "".join(new_addr)

        num_floating = new_addr.count("X")  # number of floating bits
        for i in range(2**num_floating):  # loop over all floating bit permutations
            float_repl = bin(i)[2:].zfill(num_floating)  # floating replacement
            perm_addr = new_addr
            float_locs = [i_loc for i_loc, c in enumerate(perm_addr) if c == "X"]
            for loc_idx, loc in enumerate(float_locs):
                perm_addr = perm_addr[:loc] + float_repl[loc_idx] + perm_addr[loc+1:]
            memory.update({int(perm_addr, 2): int(val)})

print(f"part 2: {sum(memory.values())}")
