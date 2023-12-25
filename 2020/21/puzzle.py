import fileinput

x = [line for line in fileinput.input()]

ingredients_list = []
allergens = []
for line in x:
    ing, al = line.split("(")
    ingredients_list.append(tuple(ing.split()))
    allergens.append(tuple(al.strip("contains").strip().strip(")").split(", ")))

unique_allergens = set([al for al_sub in allergens for al in al_sub])

ings_matched = set()  # ingredients uniquely matched to allergen
match_dict = {}
NUM_ALLERGENS = len(unique_allergens)
while len(match_dict) < NUM_ALLERGENS:
    allergens_matched = []
    for al in unique_allergens:
        ings_matching = set()  # find all ingredients that could contain this allergen
        for i in range(len(x)):  # loop over full list
            if al in allergens[i]:
                ings_to_add = set(ingredients_list[i]).difference(ings_matched)
                if len(ings_matching) == 0:
                    ings_matching.update(ings_to_add)
                else:
                    ings_matching = ings_matching.intersection(ings_to_add)
        if len(ings_matching) == 1:
            allergens_matched.append(al)
            ings_matched = ings_matched.union(ings_matching)
            match_dict.update({al: ings_matching.pop()})

    for al in allergens_matched:
        unique_allergens.remove(al)  # remove allergens that are uniquely matched


unique_ingredients = set([ing for ing_sub in ingredients_list for ing in ing_sub])
dangerous_ingredients = match_dict.values()
safe_ingredients = unique_ingredients.difference(dangerous_ingredients)

# count how often safe ingredients appear in any ingredient list
count = 0
for ing in ingredients_list:
    count += sum([safe_ing in ing for safe_ing in safe_ingredients])

print(f"part 1: {count}")

# dangerous ingredients sorted alphabetically by associated allergen
sol = ",".join([v for _, v in sorted(match_dict.items(), key=lambda item: item[0])])
print(f"part 2: {sol}")
