import fileinput
from collections import deque
from functools import cache
from math import inf

x = [line.strip() for line in fileinput.input()]


num_pad = dict(
    (a + 1j * b, str([[7, 8, 9], [4, 5, 6], [1, 2, 3], [None, 0, "A"]][a][b]))
    for a in range(4)
    for b in range(3)
)
num_pad.pop(3 + 0j)
num_inv = dict((v, k) for k, v in num_pad.items())
direc_pad = {1j: "^", 2j: "A", 1: "<", 1 + 1j: "v", 1 + 2j: ">"}
direc_inv = dict((v, k) for k, v in direc_pad.items())
direc_to_char = {-1j: "<", -1: "^", 1j: ">", 1: "v"}


def paths_for_segment(start_char, end_char, pad_type):
    """best paths between two positions on numeric or directional keypad"""
    pad_dict = {"num": num_pad, "direc": direc_pad}[pad_type]
    all_paths = []
    start_pos = {"num": num_inv, "direc": direc_inv}[pad_type][start_char]
    next_steps = deque([(start_pos, "", {start_pos})])
    while next_steps:
        pos, path, seen = next_steps.popleft()
        if pad_dict[pos] == end_char:
            path += "A"  # need to press "A" at the end
            if len(path) <= min([len(p) for p in all_paths]) if all_paths else inf:
                all_paths.append(path)
        for direc in (-1j, -1, 1j, 1):
            if pos + direc in pad_dict.keys() and pos + direc not in seen:
                next_steps.append(
                    (pos + direc, path + direc_to_char[direc], seen | {pos + direc})
                )
    return all_paths


@cache
def paths_for_sequence(sequence, pad_type):
    """best paths for sequence to be entered on numeric or directional keypad"""
    paths = [""]
    for start, end in zip("A" + sequence[:-1], sequence):  # each robot starts at "A"
        paths_seg = paths_for_segment(start, end, pad_type)
        paths = [p_old + p_new for p_old in paths for p_new in paths_seg]
    return paths


@cache
def sequence_length_at_depth(full_sequence, depth):
    """best length of a sequence at given depth"""
    length = 0
    for sequence in [p + "A" for p in full_sequence.split("A")[:-1]]:
        next_sequences = paths_for_sequence(sequence, "direc")
        if depth == 1:
            length += min(len(p) for p in next_sequences)  # last direc robot
        elif sequence == "A":
            length += 1  # press same button again
        else:
            seq_lengths = set()
            for path in next_sequences:
                seq_lengths.add(sequence_length_at_depth(path, depth - 1))
            length += min(seq_lengths)  # use best path
    return length


def get_complexity(num_direc):
    complexity_sum = 0
    for code in x:
        seq_lengths = set()
        for path in paths_for_sequence(code, "num"):  # paths of innermost robot
            seq_lengths.add(sequence_length_at_depth(path, num_direc))
        complexity_sum += min(seq_lengths) * int(code[:-1])  # use best outermost path
    return complexity_sum


print(f"part 1: {get_complexity(2)}")
print(f"part 2: {get_complexity(25)}")
