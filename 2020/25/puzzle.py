import fileinput

card_pub_key, door_pub_key = list(map(int, [line for line in fileinput.input()]))


def get_loop_size(subj_num, pub_key):
    val = 1
    loop_size = 0
    while val != pub_key:
        val = (val * subj_num) % 20201227
        loop_size += 1
    return loop_size


loop_size_card = get_loop_size(7, card_pub_key)
encryption_key = 1
for _ in range(loop_size_card):
    encryption_key = (encryption_key * door_pub_key) % 20201227

print(f"part 1: {encryption_key}")
