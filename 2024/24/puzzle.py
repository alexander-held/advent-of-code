import fileinput
import random
import re
from itertools import combinations

import matplotlib.pyplot as plt
import networkx as nx

x = "".join([line for line in fileinput.input()])

wires = {}  # wire: val
for m in re.findall(r"(\w+): ([01])", x):
    wires[m[0]] = bool(int(m[1]))

gates = {}  # out: in_1, op, in_2
graph = nx.DiGraph()
for m in re.findall(r"(\w+) (\w+) (\w+) -> (\w+)", x):
    for node in [m[0], m[2], m[3]]:
        graph.add_node(node, label=node)
    op_key = m[1] + m[0] + m[2] + m[3]
    graph.add_node(op_key, label={"AND": "&", "OR": "|", "XOR": "^"}[m[1]])
    graph.add_edges_from(((m[0], op_key), (m[2], op_key), (op_key, m[3])))
    gates[m[3]] = (m[0], m[1], m[2])


def circuit(wires, gates):
    missing_last = set()
    while (missing := set(gates.keys()) - set(wires.keys())) != missing_last:
        missing_last = missing
        for mis in missing:
            inp = gates[mis]
            if inp[0] in wires.keys() and inp[2] in wires.keys():
                if inp[1] == "AND":
                    wires[mis] = wires[inp[0]] & wires[inp[2]]
                elif inp[1] == "OR":
                    wires[mis] = wires[inp[0]] | wires[inp[2]]
                elif inp[1] == "XOR":
                    wires[mis] = wires[inp[0]] ^ wires[inp[2]]
    return [
        sum(
            wires[wire] * 2**i
            for i, wire in enumerate(sorted([w for w in wires if w[0] == c]))
        )
        for c in "xyz"
    ]


_, _, val_z = circuit(wires.copy(), gates)


# start part 2 by manual inspection of graph.pdf
# normal outputs z should always be formed via XOR, including carry from previous bit
# zNN = (xNN XOR yNN) XOR [carry]
# z11 output of AND -> should be XOR, swap the following
#   - dvh AND hnn -> z11
#   - hnn XOR dvh -> rpv
# z31 output of AND -> should be XOR, swap the following
#   - x31 AND y31 -> z31
#   - fgs XOR ctw -> dmh
# z38 output of OR -> should be XOR, swap the following
#   - bvk OR trm -> z38
#   - hhv XOR pqr -> dvq

rc = [
    (random.random(), random.random(), random.random()) for _ in range(len(wires) // 2)
]
nc = []  # node colors (same colors for same numbers)
labels = {}
for node in graph:
    labels[node] = graph.nodes[node]["label"]
    if node[0].upper() == node[0]:
        nc.append({"&": "firebrick", "|": "khaki", "^": "skyblue"}[labels[node]])
    elif node[0] in "xyz":
        nc.append(rc[int(node[1:]) - 1])
    else:
        nc.append((0.8, 0.8, 0.8))

fig, ax = plt.subplots(figsize=(45, 90), constrained_layout=True)
nx.draw_networkx(
    graph,
    ax=ax,
    pos=nx.drawing.nx_agraph.graphviz_layout(graph, prog="dot"),
    labels=labels,
    node_shape="s",
    node_color=nc,
    font_size=8,
)
fig.savefig("graph.pdf")


def wires_to_swap(wires, gates):
    # swap everything known from manual inspection
    TO_SWAP = [("z11", "rpv"), ("z31", "dmh"), ("z38", "dvq")]
    for swap in TO_SWAP:
        gates[swap[0]], gates[swap[1]] = gates[swap[1]], gates[swap[0]]

    for swap in combinations((g for g in gates if g[0] != "z"), 2):
        gates_cp = gates.copy()
        gates_cp[swap[0]], gates_cp[swap[1]] = gates_cp[swap[1]], gates_cp[swap[0]]
        val_x, val_y, val_z = circuit(wires.copy(), gates_cp)
        if val_x + val_y == val_z:  # works for original numbers, try a few more
            for _ in range(10):
                wires_cp = wires.copy()
                for wire in wires_cp:
                    wires_cp[wire] = random.getrandbits(1)  # randomize input
                val_x, val_y, val_z = circuit(wires_cp, gates_cp)
                if val_x + val_y != val_z:
                    break  # invalid circuit
            else:
                return ",".join(sorted(wire for sw in TO_SWAP + [swap] for wire in sw))


print(f"part 1: {val_z}")
print(f"part 2: {wires_to_swap(wires, gates)}")
