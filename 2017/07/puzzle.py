import fileinput
import re
from collections import Counter

x = "".join([line for line in fileinput.input()])


graph = dict()
for node, weight, above in re.findall(r"(\w+) \((\d+)\)(?: -> )?([\w, ]*)", x):
    above = [] if above == "" else above.split(", ")
    graph[node] = (above, int(weight))


def find_root(graph, prog=None):
    prog = prog or next(k for k, v in graph.items() if v[0] == [])  # start at leaf
    below = next((k for k, v in graph.items() if prog in v[0]), None)
    if below:  # recurse while possible
        return find_root(graph, prog=below)
    return below or prog  # root of tree


def weights_above(graph, prog):  # weights of node and all nodes above
    weights = graph[prog][1]
    for above in graph[prog][0]:
        weights += weights_above(graph, above)
    return weights


def find_imbalanced(graph, prog):  # return imbalanced program and offset
    weights = dict((above, weights_above(graph, above)) for above in graph[prog][0])
    ctr = Counter(weights.values())
    if len(ctr.most_common()) > 1:  # imbalance exists
        # find branch causing imbalance
        prog_imb = next(k for k, v in weights.items() if v == ctr.most_common()[1][0])
        offset = ctr.most_common()[1][0] - ctr.most_common()[0][0]
        return prog_imb, offset  # program causing imbalance and discrepancy
    return None, 0  # no imbalance found


# start at root and check weights of all daughters, iterate until balance is found
imbalance = (find_root(graph), 0)  # program and numerical imbalance
while True:
    next_imbalance = find_imbalanced(graph, imbalance[0])
    if next_imbalance[0] is None:
        break  # next level is balanced, so current level needs to be fixed
    imbalance = next_imbalance

print(f"part 1: {find_root(graph)}")
print(f"part 2: {graph[imbalance[0]][1] - imbalance[1]}")
