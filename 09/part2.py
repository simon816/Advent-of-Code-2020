import sys
import itertools

numbers = [int(n) for n in sys.stdin.readlines()]

preamble, rest = numbers[:25], numbers[25:]

while rest:
    n = rest.pop(0)
    matches = False
    for pair in itertools.combinations(preamble, 2):
        if sum(pair) == n:
            matches = True
            break
    if not matches:
        break
    preamble.pop(0)
    preamble.append(n)

invalid = n

curr = [numbers.pop(0), numbers.pop(0)]

while sum(curr) != invalid:
    n = numbers.pop(0)
    while sum(curr) + n > invalid:
        curr.pop(0)
    curr.append(n)

print(min(curr) + max(curr))
