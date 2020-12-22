import sys
import math

class Tile:

    def __init__(self, id, top, right, bottom, left):
        self.id = id
        self.edges = [top, bottom, left, right]
        self.transforms = {top, bottom, left, right, top[::-1], bottom[::-1], left[::-1], right[::-1]}

def read_tile(id, lines):
    top = lines[0]
    right = ''.join(l[-1] for l in lines)
    bottom = lines[-1]
    left = ''.join(l[0] for l in lines)
    assert len(top) == len(bottom) == len(left) == len(right)
    return Tile(id, top, right, bottom, left)

tiles = []

for tile in sys.stdin.read().split('\n\n'):
    if not tile.strip():
        continue
    lines = tile.strip().split('\n')
    assert lines[0].startswith('Tile ')
    t_id = int(lines[0].strip()[5:-1])
    tiles.append(read_tile(t_id, lines[1:]))

for t1 in tiles:
    for t2 in tiles:
        if t1 == t2:
            continue
        t1.edges = [e for e in t1.edges if e not in t2.transforms]

r = 1
for t in tiles:
    # Tiles with 2 non-paired edges must be corner tiles
    if len(t.edges) == 2:
         r *= t.id   
print(r)
