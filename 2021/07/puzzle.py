import fileinput
import statistics

x = [int(pos) for pos in [line.strip() for line in fileinput.input()][0].split(",")]

cost = lambda opt_pos: int(sum(abs(crab-opt_pos) for crab in x))
print(f"part 1: {cost(statistics.median(x))}")

cost = lambda pos: int(sum([abs(crab-pos)*(abs(crab-pos)+1)/2 for crab in x]))
print(f"part 2: {min([cost(pos) for pos in range(min(x), max(x))])}")
