import sys

numbers = sorted([int(n) for n in sys.stdin.readlines()])

curr = 0

diffs = []
while numbers:
    n = numbers.pop(0)
    diff = n - curr
    assert diff <= 3
    diffs.append(diff)
    curr = n
print(diffs.count(1) * (diffs.count(3) + 1))
