import sys
from collections import defaultdict

tiles = defaultdict(lambda: False)

# Ensure we have a perimeter of white tiles
def ensure(x, y):
    if (x, y) not in tiles:
        tiles[(x, y)] = False
    # use this function to auto-vivify neighbours
    get_adj_count(x, y)

def get_adj_count(x, y):
    c = 0
    if tiles[(x + 1, y)]:
        c += 1
    if tiles[(x - 1, y)]:
        c += 1
    if tiles[(x + 0.5, y + 1)]:
        c += 1
    if tiles[(x - 0.5, y + 1)]:
        c += 1
    if tiles[(x + 0.5, y - 1)]:
        c += 1
    if tiles[(x - 0.5, y - 1)]:
        c += 1
    return c

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
    tiles[(x, y)] = not tiles[(x, y)]
    ensure(x, y)

for rounds in range(100):

    changes = []

    for (x, y), t in list(tiles.items()):
        adj = get_adj_count(x, y)
        if t and adj == 0 or adj > 2:
            changes.append((x, y, False))
        elif not t and adj == 2:
            changes.append((x, y, True))

    for (x, y, state) in changes:
        tiles[(x, y)] = state

print(len([t for t in tiles.values() if t]))
