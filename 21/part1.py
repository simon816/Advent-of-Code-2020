from collections import defaultdict
import sys

allergens = {}

all_ingredients = defaultdict(lambda: 0)

for food in sys.stdin.readlines():
    ing, al = food.strip()[:-1].split(' (contains ')
    ing = set(ing.split(' '))
    for i in ing:
        all_ingredients[i] += 1
    for al in al.split(', '):
        if al not in allergens:
            allergens[al] = set(ing)
        else:
            allergens[al] &= ing

while sum(map(len, allergens.values())) != len(allergens):
    singles = [ing for ing in allergens.values() if len(ing) == 1]
    for ing in allergens.values():
        for s in singles:
            if s != ing:
                ing -= s

no_allergens = set(all_ingredients.keys()) - set(next(iter(ing)) for ing in allergens.values())
print(sum(all_ingredients[i] for i in no_allergens))
