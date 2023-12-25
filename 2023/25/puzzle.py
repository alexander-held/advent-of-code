import fileinput
from math import prod

import networkx as nx


x = [line.strip().split(": ") for line in fileinput.input()]

graph = nx.Graph()
graph.add_edges_from(((left, r) for left, right in x for r in right.split(" ")))

min_cut = nx.minimum_edge_cut(graph)  # edges to cut
assert len(min_cut) == 3
graph.remove_edges_from(min_cut)
print(f"part 1: {prod([len(k) for k in nx.connected_components(graph)])}")
