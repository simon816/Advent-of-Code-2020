import sys
from collections import Counter

coords = []
for line in sys.stdin.readlines():
    mod = None
    steps = []
    for c in line.strip():
        if c in 'ns':
            mod = c
            continue
        if mod is not None:
            dir = mod + c
            mod = None
        else:
            dir = c
        steps.append(dir)
    x, y = 0, 0
    for dir in steps:
        if dir == 'e':
            x += 1
        elif dir == 'w':
            x -= 1
        elif dir == 'ne':
            y += 1
            x += 0.5
        elif dir == 'nw':
            y += 1
            x -= 0.5
        elif dir == 'se':
            y -= 1
            x += 0.5
        elif dir == 'sw':
            y -= 1
            x -= 0.5
    coords.append((x, y))

black = 0
for flips in Counter(coords).values():
    if flips % 2 != 0:
        black += 1
print(black)
