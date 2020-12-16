import sys

data = sys.stdin.read().strip()

sections = data.split('\n\n')

rules = sections[0].split('\n')
ticket = sections[1].split('\n')
nearby = sections[2].split('\n')

assert ticket.pop(0) == 'your ticket:'
ticket = [int(n) for n in ticket[0].split(',')]

assert nearby.pop(0) == 'nearby tickets:'
nearby = [[int(n) for n in s.split(',')] for s in nearby]
rules = [[(r.split(':')[0], *map(int, s.strip().split('-'))) \
           for s in r.split(':')[1].split('or')] for r in rules]
rulesets = []
for ruleset in rules:
    rulesets.extend(ruleset)

all_rules = [r[0] for r in rulesets]

column_options = [set(all_rules) for _ in ticket]

for t in nearby:
    for col, n in enumerate(t):
        could_be = set()
        is_valid = False
        for (rule, lower, upper) in rulesets:
            if n >= lower and n <= upper and rule in column_options[col]:
                is_valid = True
                could_be.add(rule)
        if not is_valid:
            break
        column_options[col] &= could_be

while sum(len(opts) for opts in column_options) != len(column_options):
    for col, opts in enumerate(list(column_options)):
        if len(opts) == 1:
            for oth, others in enumerate(column_options):
                if oth != col:
                    others -= opts


answer = 1

for col, val in enumerate(ticket):
    label = next(iter(column_options[col]))
    if label.startswith('departure'):
        answer *= val

print(answer)
