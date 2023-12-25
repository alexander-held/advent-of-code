import fileinput

x = [line.strip() for line in fileinput.input()]
x = [(xi[0], int(xi[1:])) for xi in x]

direction = 1 + 0j  # facing east
pos = 0 + 0j
for op, units in x:
    if op == "N":
        pos += 1j * units
    elif op == "S":
        pos -= 1j * units
    elif op == "E":
        pos += units
    elif op == "W":
        pos -= units
    elif op == "L":
        direction *= 1j ** (units // 90)
    elif op == "R":
        direction *= (-1j) ** (units // 90)
    elif op == "F":
        pos += direction * units

print(f"part 1: {int(abs(pos.real) + abs(pos.imag))}")


# part 2
waypoint_offset = 10 + 1j
pos = 0 + 0j  # ship position
for op, units in x:
    if op == "N":
        waypoint_offset += 1j * units
    elif op == "S":
        waypoint_offset -= 1j * units
    elif op == "E":
        waypoint_offset += units
    elif op == "W":
        waypoint_offset -= units
    elif op == "L":
        waypoint_offset *= 1j ** (units // 90)
    elif op == "R":
        waypoint_offset *= (-1j) ** (units // 90)
    elif op == "F":
        pos += waypoint_offset * units

print(f"part 2: {int(abs(pos.real) + abs(pos.imag))}")
