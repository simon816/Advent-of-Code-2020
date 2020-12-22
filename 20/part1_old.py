import sys
import math

class Tile:

    def __init__(self, id, top, right, bottom, left, available='TRBL'):
        self.id = id
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left
        self.available = frozenset(available)

    def __repr__(self):
        return 'Tile(%s, T=%s, R=%s, B=%s, L=%s)' % (
            self.id, self.top, self.right, self.bottom, self.left)

    def try_fit(self, tile):
        options = []
        if 'T' in self.available:
            if tile.bottom == self.top:
                options.append(('T', tile))
            if tile.bottom[::-1] == self.top:
                options.append(( 'T', tile.flip_y))
            if tile.left == self.top:
                options.append(( 'T', tile.rotate_ccw))
            if tile.left[::-1] == self.top:
                options.append(( 'T', tile.rotate_ccw.flip_y))
            if tile.right == self.top:
                options.append(( 'T', tile.rotate_cw.flip_y))
            if tile.right[::-1] == self.top:
                options.append(( 'T', tile.rotate_cw))
            if tile.top == self.top:
                options.append(( 'T', tile.flip_x))
            if tile.top[::-1] == self.top:
                options.append(( 'T', tile.flip_x.flip_y))
        if 'R' in self.available:
            if tile.left == self.right:
                options.append(( 'R', tile))
            if tile.left[::-1] == self.right:
                options.append(( 'R', tile.flip_x))
            if tile.bottom == self.right:
                options.append(( 'R', tile.rotate_cw))
            if tile.bottom[::-1] == self.right:
                options.append(( 'R', tile.rotate_cw.flip_x))
            if tile.top == self.right:
                options.append(( 'R', tile.rotate_ccw.flip_x))
            if tile.top[::-1] == self.right:
                options.append(( 'R', tile.rotate_ccw))
            if tile.right == self.right:
                options.append(( 'R', tile.flip_y))
            if tile.right[::-1] == self.right:
                options.append(( 'R', tile.flip_y.flip_x))
        if 'B' in self.available:
            if tile.top == self.bottom:
                options.append(( 'B', tile))
            if tile.top[::-1] == self.bottom:
                options.append(( 'B', tile.flip_y))
            if tile.right == self.bottom:
                options.append(( 'B', tile.rotate_ccw))
            if tile.right[::-1] == self.bottom:
                options.append(( 'B', tile.rotate_ccw.flip_y))
            if tile.left == self.bottom:
                options.append(( 'B', tile.rotate_cw.flip_y))
            if tile.left[::-1] == self.bottom:
                options.append(( 'B', tile.rotate_cw))
            if tile.bottom == self.bottom:
                options.append(( 'B', tile.flip_x))
            if tile.bottom[::-1] == self.bottom:
                options.append(( 'B', tile.flip_x.flip_y))
        if 'L' in self.available:
            if tile.right == self.left:
                options.append(( 'L', tile))
            if tile.right[::-1] == self.left:
                options.append(( 'L', tile.flip_x))
            if tile.bottom == self.left:
                options.append(( 'L', tile.rotate_ccw.flip_x))
            if tile.bottom[::-1] == self.left:
                options.append(( 'L', tile.rotate_ccw))
            if tile.top == self.left:
                options.append(( 'L', tile.rotate_cw))
            if tile.top[::-1] == self.left:
                options.append(( 'L', tile.rotate_cw.flip_x))
            if tile.left == self.left:
                options.append(( 'L', tile.flip_y))
            if tile.left[::-1] == self.left:
                options.append(( 'L', tile.flip_y.flip_x))
        return options

    @property
    def rotate_cw(self):
        assert len(self.available) == 4
        return Tile(self.id, self.left[::-1], self.top, self.right[::-1], self.bottom)

    @property
    def rotate_ccw(self):
        assert len(self.available) == 4
        return Tile(self.id, self.right, self.bottom[::-1], self.left, self.top[::-1])

    @property
    def flip_y(self):
        assert len(self.available) == 4
        return Tile(self.id, self.top[::-1], self.left, self.bottom[::-1], self.right)

    @property
    def flip_x(self):
        assert len(self.available) == 4
        return Tile(self.id, self.bottom, self.right[::-1], self.top, self.left[::-1])

    def can_fit_above(self, tile):
        if 'T' not in self.available:
            return False
        return self.top == tile.bottom

    def can_fit_below(self, tile):
        if 'B' not in self.available:
            return False
        return self.bottom == tile.top

    def can_fit_left(self, tile):
        if 'L' not in self.available:
            return False
        return self.left == tile.right

    def can_fit_right(self, tile):
        if 'R' not in self.available:
            return False
        return self.right == tile.left

    def occupy(self, edge):
        available = self.available - set(edge)
        return Tile(self.id, self.top, self.right, self.bottom, self.left, available)

class Image:

    def __init__(self, size):
        self.grid = {}
        self.min_x = 0
        self.max_x = 0
        self.min_y = 0
        self.max_y = 0
        self.size = size

    def add_tile(self, tile):
        if not self.grid:
            self.grid[(0, 0)] = tile
            return True, None, None
        options = []
        for (x, y), other in self.grid.items():
            face_opts = other.try_fit(tile)
            for (face, new_tile) in face_opts:
                if face == 'T':
                    new_x, new_y = x, y - 1
                elif face == 'B':
                    new_x, new_y = x, y + 1
                elif face == 'L':
                    new_x, new_y = x - 1, y
                elif face == 'R':
                    new_x, new_y = x + 1, y
                if self.can_fit(new_x, new_y, new_tile):
                    #print(len(self.grid), new_tile.id, "could fit", new_x, new_y)
                    options.append((new_x, new_y, new_tile))
        if options:
            x, y, tile = options[0]
            others = options[1:]
            if others:
                state = dict(self.grid)
            self.insert(x, y, tile)
            if others:
                return True, state, others
            return True, None, None
        return False, None, None

    def replay(self, grid, option):
        self.grid = dict(grid)
        x, y, tile = option
        xs = [c[0] for c in grid.keys()]
        ys = [c[1] for c in grid.keys()]
        self.min_x, self.max_x = min(xs), max(xs)
        self.min_y, self.max_y = min(ys), max(ys)
        self.insert(x, y, tile)

    def can_fit(self, x, y, tile):
        g = self.grid
        # Fail if already taken
        if (x, y) in g:
            return False
        min_x = min(self.min_x, x)
        min_y = min(self.min_y, y)
        max_x = max(self.max_x, x)
        max_y = max(self.max_y, y)
        if max_x - min_x > self.size:
            return False
        if max_y - min_y > self.size:
            return False
        # Fail if tile above cannot match
        if (x, y - 1) in g and not g[(x, y - 1)].can_fit_below(tile):
            return False
        # Fail if tile below cannot match
        if (x, y + 1) in g and not g[(x, y + 1)].can_fit_above(tile):
            return False
        # Fail if tile to the left cannot match
        if (x - 1, y) in g and not g[(x - 1, y)].can_fit_right(tile):
            return False
        # Fail if tile to the right cannot match
        if (x + 1, y) in g and not g[(x + 1, y)].can_fit_left(tile):
            return False
        return True

    def insert(self, x, y, tile):
        #print("Insert", x, y)
        assert self.can_fit(x, y, tile), (x, y, tile)
        self.min_x = min(self.min_x, x)
        self.min_y = min(self.min_y, y)
        self.max_x = max(self.max_x, x)
        self.max_y = max(self.max_y, y)
        g = self.grid
        if (x, y - 1) in g:
            g[(x, y - 1)] = g[(x, y - 1)].occupy('B')
            tile = tile.occupy('T')
        if (x, y + 1) in g:
            g[(x, y + 1)] = g[(x, y + 1)].occupy('T')
            tile = tile.occupy('B')
        if (x - 1, y) in g:
            g[(x - 1, y)] = g[(x - 1, y)].occupy('R')
            tile = tile.occupy('L')
        if (x + 1, y) in g:
            g[(x + 1, y)] = g[(x + 1, y)].occupy('L')
            tile = tile.occupy('R')
        g[(x, y)] = tile

def read_tile(id, lines):
    top = lines[0]
    right = ''.join(l[-1] for l in lines)
    bottom = lines[-1]
    left = ''.join(l[0] for l in lines)
    assert len(top) == len(bottom) == len(left) == len(right)
    return Tile(id, top, bottom, left, right)

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
image = Image(size)

states = []

while len(tiles):
    new_tiles = []
    progress = False
    for tile in tiles:
        added, state, others = image.add_tile(tile)
        if not added:
            new_tiles.append(tile)
        else:
            progress = True
            if state:
                #print("Branch", len(states), len(others))
                states.append((state, others, tiles))
    if progress or not new_tiles:
        tiles = new_tiles
        continue
    if not states:
        print(image.grid)
        print(tiles)
    state, others, tiles = states.pop()
    assert len(others)
    print("Backtracking", len(states), len(others))
    option, others = others[0], others[1:]
    if len(others):
        states.append((state, others, tiles))
    image.replay(state, option)

xs = [c[0] for c in image.grid.keys()]
ys = [c[1] for c in image.grid.keys()]

min_x, max_x = min(xs), max(xs)
min_y, max_y = min(ys), max(ys)

a = (min_x, min_y)
b = (min_x, max_y)
c = (max_x, min_y)
d = (max_x, max_y)

g = image.grid
print('\n'.join('%s: %s' % (k, v) for k, v in g.items()))
print(g[a], g[b], g[c], g[d])
