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

print(n)
