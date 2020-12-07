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

def count(bag):
    total = 0
    for (color, qty) in bags[bag].items():
        total += qty * (count(color) + 1)
    return total

print(count('shiny gold'))
