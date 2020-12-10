import sys

from collections import defaultdict, namedtuple

numbers = [0] + sorted([int(n) for n in sys.stdin.readlines()])

target = numbers[-1] # largest

DP = namedtuple('DP', 'n f')

options = {}
for i, n in enumerate(numbers):
    valid = []
    for offset in range(1, min(4, len(numbers) - i)):
        next_n = numbers[i + offset]
        if next_n - n <= 3:
            valid.append(DP(next_n, None))
        else:
            break
    options[n] = valid

reverse = defaultdict(list)

for k, s in options.items():
    for v in s:
        reverse[v.n].append(k)

ways = { target: 1 }

def solve_for(ptr):
    for n in reverse[ptr]:
        unresolved = options[n]
        new = []
        for u in unresolved:
            if u.f is None and u.n == ptr:
                u = u._replace(f=ways[ptr])
            new.append(u)
        if all(u.f is not None for u in new):
            assert n not in ways
            ways[n] = sum(u.f for u in new)
        options[n] = new
        if n in ways:
            solve_for(n)

solve_for(target)

print(ways[0])

