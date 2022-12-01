import fileinput

x = "".join([line for line in fileinput.input()])
elves = [map(int, elf.split()) for elf in x.split("\n\n")]
calories_per_elf = sorted(sum(elf) for elf in elves)

print(f"part 1: {calories_per_elf[-1]}")
print(f"part 2: {sum(calories_per_elf[-3:])}")
