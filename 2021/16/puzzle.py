import fileinput
from math import prod
from operator import lt, eq, gt

x = [line.strip() for line in fileinput.input()][0]

OPERATORS = [sum, prod, min, max, None, gt, lt, eq]


class Decoder:
    def __init__(self, hex_stream):
        self.stream = "".join([format(int(c, 16), "b").zfill(4) for c in hex_stream])
        self.pos = 0
        self.version_sum = 0

    def next_stream_segment(self, length):
        res = self.stream[self.pos : self.pos + length]
        self.pos += length
        return res

    def decode_literal(self):
        literal_value = ""
        while True:
            group = self.next_stream_segment(5)
            literal_value += group[1:]
            if group[0] == "0":
                break  # last group
        return int(literal_value, 2)

    def decode_operator(self):
        length_type_id = int(self.next_stream_segment(1), 2)

        if length_type_id == 0:
            length_subpackets = int(self.next_stream_segment(15), 2)
            packets = []
            last_pos = self.pos + length_subpackets
            while self.pos < last_pos:
                packets.append(self.decode_packet())

        elif length_type_id == 1:
            num_subpackets = int(self.next_stream_segment(11), 2)
            packets = [self.decode_packet() for _ in range(num_subpackets)]

        return packets

    def decode_packet(self):
        version = int(self.next_stream_segment(3), 2)
        self.version_sum += version
        type = int(self.next_stream_segment(3), 2)
        if type <= 3:
            return OPERATORS[type](self.decode_operator())
        elif type == 4:
            return self.decode_literal()
        else:
            return int(OPERATORS[type](*self.decode_operator()))


dec = Decoder(x)
result = dec.decode_packet()
print(f"part 1: {dec.version_sum}")
print(f"part 2: {result}")
