import fileinput
import functools

x = [line.strip() for line in fileinput.input()]

timestamp = int(x[0])
busses = [int(xi) for xi in x[1].split(",") if xi != "x"]

next_busses = [(timestamp//bus + 1)*bus for bus in busses]
earliest_bus_time = min(next_busses)
next_bus_idx = next_busses.index(earliest_bus_time)
print(f"part 1: {busses[next_bus_idx]*(earliest_bus_time-timestamp)}")


# part 2
departure_time_offset = [int(i) for i, xi in enumerate(x[1].split(",")) if xi != "x"]
period = busses[0]  # starting period for scan: first bus
first_coincidence = 0  # starting point for each scan

for idx_max in range(2, len(busses)+1):  # iteratively find solution for busses
    t = first_coincidence
    while True:
        departure_times = [d + t for d in departure_time_offset[:idx_max]]
        bus_departs = [dep_t % b == 0 for dep_t, b in zip(departure_times, busses[:idx_max])]
        if all(bus_departs):
            first_coincidence = t
            print(f"first coincidence of first {idx_max} busses: {first_coincidence}")
            break
        t += period

    # next period: least common multiple of busses so far
    period = functools.reduce((lambda x, y: x*y), busses[:idx_max])

print(f"part 2: {t}")
