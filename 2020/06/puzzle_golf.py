for f in [set.union,set.intersection]:print(sum([len(f(*map(set,g.split()))) for g in open("i").read().split("\n\n")]))
