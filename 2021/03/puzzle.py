import fileinput
from collections import Counter

x = [line.strip() for line in fileinput.input()]

gamma = ""
epsilon = ""
for i in range(len(x[0])):
    c = Counter([num[i] for num in x])
    gamma += c.most_common()[0][0]
    epsilon += c.most_common()[-1][0]

print(f"part 1: {int(''.join(gamma), 2) * int(''.join(epsilon), 2)}")

candidates_oxy = x.copy()
candidates_co2 = x.copy()
for i in range(len(x[0])):
    counter_oxy = Counter([num[i] for num in candidates_oxy])
    keep_oxy = "1" if counter_oxy["1"] >= counter_oxy["0"] else "0"
    candidates_oxy = [xx for xx in candidates_oxy if xx[i] == keep_oxy]

    counter_co2 = Counter([num[i] for num in candidates_co2])
    keep_co2 = "0" if counter_co2["0"] <= counter_co2["1"] else "1"
    candidates_co2 = [xx for xx in candidates_co2 if xx[i] == keep_co2]

    if len(candidates_oxy) == 1:
        oxy = int(candidates_oxy[0], 2)

    if len(candidates_co2) == 1:
        co2 = int(candidates_co2[0], 2)

print(f"part 2: {oxy*co2}")
