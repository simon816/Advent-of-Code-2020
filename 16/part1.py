import sys

data = sys.stdin.read().strip()

sections = data.split('\n\n')

rules = sections[0].split('\n')
nearby = sections[2].split('\n')

assert nearby.pop(0) == 'nearby tickets:'
nearby = [set(int(n) for n in s.split(',')) for s in nearby]
ranges = [[tuple(map(int, s.strip().split('-'))) \
           for s in r.split(':')[1].split('or')] for r in rules]
rangesets = []
for rangeset in ranges:
    rangesets.extend(rangeset)

invalid = 0

for t in nearby:
    for n in t:
        is_valid = False
        for (lower, upper) in rangesets:
            if n >= lower and n <= upper:
                is_valid = True
                break
        if not is_valid:
            invalid += n

print(invalid)
