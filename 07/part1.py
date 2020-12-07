from collections import defaultdict
import re
import sys

bags = defaultdict(dict)
parenting = defaultdict(list)

for rule in sys.stdin.readlines():
    bag, contents = rule.strip().split(' bags contain ')
    for content in contents.split(', '):
        if content != 'no other bags.':
            m = re.match('(\d+) (.*) bags?', content)
            qty = int(m.group(1))
            color = m.group(2)
            bags[bag][color] = qty
            parenting[color].append(bag)
        else:
            bags[bag] = {}

def find_roots(needle, bag):
    if not len(parenting[bag]):
        return [bag]
    parents = []
    if bag in bags and bag != needle:
        parents.append(bag)
    for p in parenting[bag]:
        parents.extend(find_roots(needle, p))
    return parents

print(len(set(find_roots('shiny gold', 'shiny gold'))))
    
