import sys
import math

class Tile:

    def __init__(self, id, top, right, bottom, left, content):
        self.id = id
        self.pairings = {
            top: ('T', None, None),
            bottom: ('B', None, None),
            left: ('L', None, None),
            right: ('R', None, None),
        }
        self.transforms = {
            top: 'T',
            bottom: 'B',
            left: 'L',
            right: 'R',
            top[::-1]: 'TI',
            bottom[::-1]: 'BI',
            left[::-1]: 'LI',
            right[::-1]: 'RI'
        }
        assert len(self.transforms) == 8
        self.content = content
        self.completed = False
        self.edge_mapping = {
            'T': 'T',
            'R': 'R',
            'B': 'B',
            'L': 'L',
        }
        self.oriented = False

    def __repr__(self):
        return 'Tile(%d)' % (self.id,)

    def orient(self, adj_edge, own_edge):
        if self.oriented:
            return
        print("Orient", self.id, adj_edge, own_edge)
        if own_edge in ['RI', 'LI']:
            self.flip_x()
            own_edge = own_edge[0]
        elif own_edge in ['BI', 'TI']:
            self.flip_y()
            own_edge = own_edge[0]

        adj_is_inverted = False
        if adj_edge.endswith('I'):
            adj_edge = adj_edge[0]
            adj_is_inverted = True

        edges = 'TRBL'
        i1 = edges.index(adj_edge)
        i2 = edges.index(own_edge)
        turns = ((i2 + 4) - i1) % 4
        if turns != 2:
            self.rotate(turns)
            if turns == 1:
                if own_edge in 'TB':
                    self.flip_x()
            if turns == 3:
                if own_edge in 'LR':
                    self.flip_y()
            if adj_edge in 'RL':
                self.flip_y()
            else:
                self.flip_x()
        if adj_is_inverted:
            if adj_edge in 'RL':
                self.flip_x()
            elif adj_edge in 'TB':
                self.flip_y()
        self.oriented = True

    def flip_y(self):
        print(self.id, "flip y")
        self.content = [l[::-1] for l in self.content]
        self.edge_mapping['L'], self.edge_mapping['R'] \
                                = self.edge_mapping['R'], self.edge_mapping['L']
        self.invert_edge('T')
        self.invert_edge('B')

    def flip_x(self):
        print(self.id, "flip x")
        self.content = self.content[::-1]
        self.edge_mapping['T'], self.edge_mapping['B'] \
                                = self.edge_mapping['B'], self.edge_mapping['T']
        self.invert_edge('L')
        self.invert_edge('R')

    def invert_edge(self, edge):
        e = self.edge_mapping[edge]
        if e.endswith('I'):
            self.edge_mapping[edge] = e[0]
        else:
            self.edge_mapping[edge] = e + 'I'

    def rotate(self, ccw_count):
        print(self.id, "rotate", ccw_count)
        for _ in range(ccw_count):
            # Note: assume square
            content = []
            for col in range(len(self.content) - 1, -1, -1):
                content.append(''.join(l[col] for l in self.content))
            self.content = content
            edges = dict(self.edge_mapping)
            self.edge_mapping['T'] = edges['R']
            self.edge_mapping['R'] = edges['B']
            self.edge_mapping['B'] = edges['L']
            self.edge_mapping['L'] = edges['T']
            self.invert_edge('L')
            self.invert_edge('R')
            print(edges, "->", self.edge_mapping)

def read_tile(id, lines):
    top = lines[0]
    right = ''.join(l[-1] for l in lines)
    bottom = lines[-1]
    left = ''.join(l[0] for l in lines)
    assert len(top) == len(bottom) == len(left) == len(right)
    assert len({top, bottom, left, right}) == 4
    return Tile(id, top, right, bottom, left, list(lines))#[l[1:-1] for l in lines[1:-1]])

tiles = []

for tile in sys.stdin.read().split('\n\n'):
    if not tile.strip():
        continue
    lines = tile.strip().split('\n')
    assert lines[0].startswith('Tile ')
    t_id = int(lines[0].strip()[5:-1])
    tiles.append(read_tile(t_id, lines[1:]))

size = int(math.sqrt(len(tiles)))
assert size**2 == len(tiles)

for t1 in tiles:
    for t2 in tiles:
        if t1 == t2:
            continue
        for e, (name, t, _) in list(t1.pairings.items()):
            if t is not None:
                assert e not in t2.transforms or t2 == t
                continue
            if e in t2.transforms:
                t2_edge = t2.transforms[e]
                t1.pairings[e] = (name, t2, t2_edge)

edge_delta = {
    'T': (0, 1),
    'R': (1, 0),
    'B': (0, -1),
    'L': (-1, 0),
}

grid = {}
min_x, min_y = 0, 0

fringe = [(0, 0, tiles[0])]
while fringe:
    x, y, tile = fringe.pop()
    min_x = min(min_x, x)
    min_y = min(min_y, y)
    print(x, y, tile, list(tile.pairings.values()))
    if tile.completed:
        #assert grid[(x, y)] == tile, (grid[(x, y)], tile)
        continue
    assert (x, y) not in grid, (x, y, grid[(x, y)], tile)
    grid[(x, y)] = tile
    tile.completed = True
    for (this_edge, other, other_edge) in tile.pairings.values():
        print(tile.id, this_edge, "is really", tile.edge_mapping[this_edge])
        if other is None or other.completed:
            continue
        other.orient(tile.edge_mapping[this_edge], other_edge)
        sx, sy = edge_delta[tile.edge_mapping[this_edge][0]]
        fringe.append((x + sx, y + sy, other))

print(grid)

grid2 = {}
for (x, y), tile in grid.items():
    grid2[(x - min_x, y - min_y)] = tile

tile_image = []
for y in range(size - 1, -1, -1):
    tile_image.append([grid2[(x, y)] for x in range(0, size)])

def build_image(tiles):
    image = []
    for line in tiles:
        lines = []
        s = ''
        for tile in line:
            s += ' ' + str(tile.id)
            if not lines:
                lines = ['   ' + str(tile.id)] + list(tile.content)
            else:
                lines[0] += '       ' + str(tile.id)
                for i, line in enumerate(tile.content):
                    # Concat content
                    lines[i + 1] += ' ' + line
        image.extend(lines)
        image.append('')
        print(s)
    return image

image = build_image(tile_image)

print('\n'.join(image))
