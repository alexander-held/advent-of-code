import fileinput
import math
from collections import Counter, defaultdict
import heapq

x = [line.strip().replace("#", "") for line in fileinput.input()][2:-1]
cols = ["." + "".join([x[j][i] for j in range(len(x))]) for i in range(len(x[0]))]
state = (".", ".", cols[0], ".", cols[1], ".", cols[2], ".", cols[3], ".", ".")

# solutions for parts 1 and 2
SOLVED_P1 = (".", ".", ".AA", ".", ".BB", ".", ".CC", ".", ".DD", ".", ".")
SOLVED_P2 = (".", ".", ".AAAA", ".", ".BBBB", ".", ".CCCC", ".", ".DDDD", ".", ".")

# set up a constants for navigation
ROOMS = [2, 4, 6, 8]
HALLWAY = [0, 1, 3, 5, 7, 9, 10]
ROOM_FOR_LETTER = {"A": 2, "B": 4, "C": 6, "D": 8}
LETTER_FOR_ROOM = {2: "A", 4: "B", 6: "C", 8: "D"}
MULTIPLIER = {"A": 1, "B": 10, "C": 100, "D": 1000}


def print_state(state):
    # for debugging purposes: visualize a state (hallway and rooms)
    for col in state:
        print(col[0], end="")
    print()
    for j in range(1, len(state[2])):
        for i in [2, 4, 6, 8]:
            print(f"{'  '*(i==2)}{state[i][j]}", end=" ")
        print("\n", end="")


def path_has_collisions(state, start, end):
    # check whether target is occupied and hallway moving is blocked
    if state[end][0] != ".":
        return True  # target position is not empty
    # find possible collisions within hallway
    if end < start:
        start, end = end, start  # ensure start is left of end for range below
    return not all([state[idx][0] == "." for idx in range(start + 1, end)])


def extract_from_room(state, room):
    # get letter out of room alongside its depth
    max_depth = len(state[room]) - 1
    letter, depth = next(
        ((c, i) for i, c in enumerate(state[room]) if c != "."), (".", max_depth)
    )
    return letter, depth


def available_room_depth(state, room):
    # check how far into a room a letter can move
    # this does NOT check that rest of room follows rules
    max_depth = len(state[room])  # one larger than accessible, see -1 below
    # find first non-"." spot, otherwise default to max_depth
    # then move back up one spot to get lowest free position
    depth = next((idx for idx, c in enumerate(state[room]) if c != "."), max_depth) - 1
    return depth


def room_done(state, room):
    # check whether a room is correctly filled already
    target_letter = LETTER_FOR_ROOM[room]
    num_expected = len(state[2]) - 1  # expected letters per room
    return Counter(state[room])[target_letter] == num_expected


def get_moves(state):
    # get all possible moves for a given state, if any moves are possible that put
    # letter into its final position, only return such moves
    moves = []

    # move from hallway to room if room is otherwise correctly filled so far
    start_filter = filter(lambda h: h[0] != ".", ((state[idx], idx) for idx in HALLWAY))
    # loop over filled hallway spots
    for letter, hallway_start in start_filter:
        room_target = ROOM_FOR_LETTER[letter]  # one possible target room per letter

        if path_has_collisions(state, hallway_start, room_target):
            continue  # hallway collision, move not possible

        elif any([l not in [letter, "."] for l in state[room_target]]):
            continue  # target room must only contain correct letters (or ".")

        # depth in room: where will new letter go
        depth = available_room_depth(state, room_target)
        # cost: move from hallway start to spot above room, then move down into room
        cost = (abs(room_target - hallway_start) + depth) * MULTIPLIER[letter]
        moves.append((hallway_start, room_target, cost))

    if len(moves):
        # found legal moves from hallway to room, do only those as they are optimal
        return moves

    # move topmost letter in room to hallway
    for room_start in ROOMS:
        letter, depth = extract_from_room(state, room_start)

        if letter == ".":
            continue  # room is already empty

        elif room_done(state, room_start):
            continue  # room is already fully done

        for hallway_target in HALLWAY:
            if path_has_collisions(state, room_start, hallway_target):
                continue  # target is not empty, or there is a hallway collision

            # cost: move out of room to hallway (depth), then move within hallway
            cost = (depth + abs(hallway_target - room_start)) * MULTIPLIER[letter]
            moves.append((room_start, hallway_target, cost))

    return moves


def update_state(state, start, end):
    # does NOT do collision checking, assumes moves are legal
    # moves are assumed to be room-to-hallway or vice versa, not r-to-r or h-to-h
    # could include depth information in move instruction to skip duplicate calculations
    state_ = list(state)
    if start in ROOMS:
        # moving from room to hallway
        letter, depth = extract_from_room(state, start)
        state_[end] = letter
        state_[start] = f"{state[start][:depth]}.{state[start][depth + 1 :]}"
    else:
        # hallway to room
        depth = available_room_depth(state, end)
        state_[end] = f"{state[end][:depth]}{state[start]}{state[end][depth + 1 :]}"
        state_[start] = "."

    return tuple(state_)


def explore(state_start):  # Dijkstra's algorithm, see also day 15
    print_state(state_start)
    min_cost_to_state = defaultdict(lambda: math.inf)
    priority_queue = []
    heapq.heappush(priority_queue, (0, state_start))  # start at initial state, 0 cost

    while len(priority_queue):
        state_cost, state = heapq.heappop(priority_queue)  # explore in increasing cost

        for start, end, move_cost in get_moves(state):  # all possible moves
            cost_next = state_cost + move_cost  # cost so far plus cost from next move
            next_state = update_state(state, start, end)
            if cost_next < min_cost_to_state[next_state]:
                priority_queue.append((cost_next, next_state))
                min_cost_to_state[next_state] = cost_next  # new cheapest path to state

    return min_cost_to_state


def part_2_state(state):
    # insert extra room content to turn a part 1 state into a part 2 state
    state_ = list(state)
    additions_part_2 = ["DD", "CB", "BA", "AC"]
    for i in range(1, 5):
        state_[i * 2] = f"{state[i*2][0:2]}{additions_part_2[i-1]}{state[i*2][2]}"
    return tuple(state_)


costs_p1 = explore(state)
print(f"part 1: {costs_p1[SOLVED_P1]}")

state = part_2_state(state)  # insert extra room content
costs_p2 = explore(state)
print(f"part 2: {costs_p2[SOLVED_P2]}")
