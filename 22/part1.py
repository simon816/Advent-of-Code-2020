import sys

p1, p2 = [s.strip().split('\n') for s in sys.stdin.read().split('\n\n')]
assert p1.pop(0) == 'Player 1:'
assert p2.pop(0) == 'Player 2:'
p1 = [int(n) for n in p1]
p2 = [int(n) for n in p2]

while p1 and p2:
    a = p1.pop(0)
    b = p2.pop(0)
    if a > b:
        p1.append(a)
        p1.append(b)
    else:
        assert a < b
        p2.append(b)
        p2.append(a)

winner = p1 if p1 else p2

score = sum(i * n for i, n in enumerate(winner[::-1], 1))
print(score)
