import fileinput

x = list(map(int, [line.strip() for line in fileinput.input()][0].split()))


def parse(stream):
    sum_metadata_total = 0
    num_children = stream.pop(0)
    num_meta = stream.pop(0)

    child_vals = []
    for _ in range(num_children):
        # parse all children, keep track of metadata sums and node values of children
        stream, partial_sum_meta, node_value = parse(stream)
        sum_metadata_total += partial_sum_meta
        child_vals.append(node_value)

    metadata = [stream.pop(0) for _ in range(num_meta)]
    sum_metadata_total += sum(metadata)

    if num_children == 0:
        # if no children, node value is sum of metadata
        node_value = sum(metadata)
    else:
        # metadata >= 1 are indices to child values
        node_value = sum(child_vals[m - 1] for m in metadata if 1 <= m <= num_children)

    return stream, sum_metadata_total, node_value


_, sum_metadata, value_root = parse(x)
print(f"part 1: {sum_metadata}")
print(f"part 2: {value_root}")
