import fileinput

x = [line.strip() for line in fileinput.input()]

rules = {}
for rule in x:
    container, contents = rule.split("contain")
    container = container.replace(" bags", "").strip()
    contents = [c.strip().replace(" bags", "").replace(" bag", "").replace(".", "") for c in contents.split(",")]
    colors = [c[2:] if c != "no other" else None for c in contents]
    num_bags = [int(c[0]) if c != "no other" else None for c in contents]
    r = {}
    for c, n in zip(colors, num_bags):
        r.update({c: n})
    rules.update({container: r})

def outer_exists(c):
    outer_list = []
    for outer, inner in zip(rules.keys(), rules.values()):
        if c in inner.keys():
            outer_list.append(outer)
    return outer_list

bags = ["shiny gold"]
all_containers = []
while True:
    containers = []
    for s in bags:
        containers += outer_exists(s)
    all_containers += containers
    bags = containers
    if containers == []:
        break

print("unique bags:", len(set(all_containers)))

# part 2
def inner_exists(bag_dict):
    inner = {}
    for color_outer, number_outer in bag_dict.items():
        for color_inner, number_inner in rules[color_outer].items():
            if color_inner is None:
                continue
            if color_inner in inner.keys():
                inner[color_inner] += number_outer*number_inner  # bag color already exists
            else:
                inner.update({color_inner: number_outer*number_inner})
    return inner

bags = {"shiny gold": 1}
bag_counter = 0
while True:
    inner_bags = inner_exists(bags)
    if inner_bags == {}:
        break
    bag_counter += sum([v for v in inner_bags.values()])
    bags = inner_bags

print("total number of bags:", bag_counter)
