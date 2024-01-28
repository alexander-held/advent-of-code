import fileinput

x = int([line for line in fileinput.input()][0])

buffer = [0]
idx = 0
for i in range(2017):
    idx = (idx + 1 + x) % len(buffer)
    buffer.insert(idx, i + 1)

print(f"part 1: {buffer[(idx+1) % len(buffer)]}")

# part 2: only track position to the right of 0, buffer otherwise not needed
buffer_len = 1
idx = 0
idx_0 = 0  # track position of zero in buffer
num_after_0 = None
for i in range(50_000_000):
    idx = (idx + 1 + x) % buffer_len
    buffer_len += 1

    if (idx_0 + 1) % (buffer_len - 1) == idx:
        num_after_0 = i + 1  # insert happened directly after 0

    if idx <= idx_0:
        idx_0 += 1  # insert happened to the left, update position of 0

print(f"part 2: {num_after_0}")  # ~0.5 seconds with pypy3
