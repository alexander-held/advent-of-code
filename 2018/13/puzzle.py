import fileinput
from collections import defaultdict
from copy import deepcopy

x = [line.rstrip() for line in fileinput.input()]


class Cart:
    def __init__(self, pos, direc):
        self.pos = pos
        self.direc = {"^": -1j, ">": 1, "v": 1j, "<": -1}[direc]
        self.num_turns = 0

    def turn(self):  # left, straight, right
        self.direc *= {0: -1j, 1: 1, 2: 1j}[self.num_turns % 3]
        self.num_turns += 1


tracks = defaultdict(lambda: " ")
carts = []
trans = str.maketrans("^>v<", "|-|-")  # replace carts by their tracks underneath
for y_pos, line in enumerate(x):
    for x_pos, ch in enumerate(line):
        if ch in "^>v<":
            carts.append(Cart(x_pos + 1j * y_pos, ch))
        tracks[x_pos + 1j * y_pos] = ch.translate(trans)


def tick(tracks, carts, p2):
    carts = sorted(carts, key=lambda c: (c.pos.real, c.pos.imag))  # sort carts
    for cart in carts:
        colliding = next((c for c in carts if c.pos == cart.pos + cart.direc), None)
        if colliding:
            if not p2:
                return tracks, carts, cart.pos + cart.direc  # return collision spot
            # remove both carts
            carts = [c for c in carts if c.pos not in [cart.pos, colliding.pos]]
            continue

        target = tracks[cart.pos + cart.direc]
        cart.pos += cart.direc  # cart moves
        if target == "+":
            cart.turn()
        elif target == "/":  # clockwise if vertical, counterclockwise otherwise
            cart.direc *= 1j * (1 if cart.direc.imag != 0 else -1)
        elif target == "\\":  # clockwise if horizontal, counterclockwise otherwise
            cart.direc *= 1j * (1 if cart.direc.imag == 0 else -1)

        if len(carts) == 1:
            return tracks, carts, cart.pos  # location of last remaining cart

    return tracks, carts, None


def simulate(tracks, carts, p2=False):
    sol = None
    carts = deepcopy(carts)
    while sol is None:
        tracks, carts, sol = tick(tracks, carts, p2)
    return f"{int(sol.real)},{int(sol.imag)}"


print(f"part 1: {simulate(tracks, carts)}")
print(f"part 2: {simulate(tracks, carts, p2=True)}")
