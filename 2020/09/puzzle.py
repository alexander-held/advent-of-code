import fileinput
import itertools

x = [int(line.strip()) for line in fileinput.input()]

preamble = 25

# part 1
for i, num in enumerate(x):
    if i < preamble:
        continue
    if not any([x+y == num for x, y in itertools.combinations(x[i-preamble:i], 2)]):
        print("invalid number", num)
        target = num
        break

# part 2
for i, num in enumerate(x):
    sum = num
    for j, num_next in enumerate(x[i+1:]):
        sum += num_next
        if sum == target:
            num_slice = x[i:i+j+2]
            print("min + max", min(num_slice)+max(num_slice))
        elif sum > target:
            break
