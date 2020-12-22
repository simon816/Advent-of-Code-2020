import sys

def play(p1, p2):
    seen = set()
    while p1 and p2:
        sig = (tuple(p1), tuple(p2))
        if sig in seen:
            return 1
        seen.add(sig)
        a = p1.pop(0)
        b = p2.pop(0)
        if len(p1) >= a and len(p2) >= b:
            winner = play(p1[:a], p2[:b])
        else:
            winner = 1 if a > b else 2
        if winner == 1:
            p1.append(a)
            p1.append(b)
        else:
            p2.append(b)
            p2.append(a)
    return 1 if p1 else 2

p1, p2 = [s.strip().split('\n') for s in sys.stdin.read().split('\n\n')]
assert p1.pop(0) == 'Player 1:'
assert p2.pop(0) == 'Player 2:'
p1 = [int(n) for n in p1]
p2 = [int(n) for n in p2]

winner = p1 if play(p1, p2) == 1 else p2
        
score = sum(i * n for i, n in enumerate(winner[::-1], 1))
print(score)
