import fileinput


x = "".join([line.strip() for line in fileinput.input()])

FREE = -1  # ID for free space
f_id = 0
disk = []
file_idx_and_size = {}  # store initial index and size
for idx, num in enumerate(x):
    if idx % 2 == 0:  # is file
        file_idx_and_size[f_id] = (len(disk), int(num))
        disk += [f_id] * int(num)
        f_id += 1
    else:
        disk += [FREE] * int(num)


d1 = disk.copy()  # part 1
while True:
    free_idx = next(idx for idx, val in enumerate(d1) if val == FREE)

    # find part of file to move
    f_idx = len(d1) - next(idx for idx, val in enumerate(d1[::-1]) if val != FREE) - 1

    if free_idx < f_idx:  # perform update
        d1[free_idx], d1[f_idx] = d1[f_idx], d1[free_idx]
    else:
        break


d2 = disk.copy()  # part 2
for f_id in sorted(file_idx_and_size.keys())[::-1]:  # files in decreasing order of ID
    f_idx, size = file_idx_and_size[f_id]

    # find leftmost FREE contiguous space of sufficient size
    free_space = [FREE] * size
    free_idx = next(
        (idx for idx in range(len(d2)) if d2[idx : idx + size] == free_space), None
    )

    if free_idx and free_idx < f_idx:  # perform update
        d2[free_idx : free_idx + size] = [f_id] * size
        d2[f_idx : f_idx + size] = [FREE] * size


checksum = lambda d: sum([idx * f_id for idx, f_id in enumerate(d) if f_id != FREE])

print(f"part 1: {checksum(d1)}")
print(f"part 2: {checksum(d2)}")  # ~15 sec with pypy
