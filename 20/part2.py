import re
import sys
import math

opposite = {
    'T': 'B',
    'L': 'R',
    'B': 'T',
    'R': 'L',
}

class Tile:

    def __init__(self, id, lines):
        self.id = id
        self.lines = lines
        self.recompute_edges()
        self.completed = False

    def __repr__(self):
        return 'Tile(%d)' % (self.id,)

    @property
    def content(self):
        return [l[1:-1] for l in self.lines[1:-1]]

    def recompute_edges(self):
        top = self.lines[0]
        right = ''.join(l[-1] for l in self.lines)
        bottom = self.lines[-1]
        left = ''.join(l[0] for l in self.lines)
        assert len(top) == len(bottom) == len(left) == len(right)
        self.edges = {
            top: 'T',
            bottom: 'B',
            left: 'L',
            right: 'R',
        }
        assert len(self.edges) == 4
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

    def orient(self, from_face, paired_face):
        if opposite[from_face] == paired_face:
            return
        if opposite[from_face] + 'I' == paired_face:
            if from_face in 'LR':
                self.flip_x()
            else:
                self.flip_y()
            return
        if from_face + 'I' == paired_face:
            self.flip_x()
            self.flip_y()
            return
        if from_face == paired_face:
            if paired_face in 'TB':
                self.flip_x()
            else:
                self.flip_y()
            return
        if from_face == 'L' and paired_face == 'BI':
            self.rotate_ccw(1)
            return
        if from_face == 'L' and paired_face == 'B':
            self.rotate_ccw(1)
            self.flip_x()
            return
        if from_face == 'L' and paired_face == 'T':
            self.rotate_cw(1)
            return
        if from_face == 'L' and paired_face == 'TI':
            self.rotate_cw(1)
            self.flip_x()
            return
        if from_face == 'R' and paired_face == 'B':
            self.rotate_cw(1)
            return
        if from_face == 'R' and paired_face == 'BI':
            self.rotate_cw(1)
            self.flip_x()
            return
        if from_face == 'R' and paired_face == 'TI':
            self.rotate_ccw(1)
            return
        if from_face == 'B' and paired_face == 'R':
            self.rotate_ccw(1)
            return
        if from_face == 'B' and paired_face == 'RI':
            self.rotate_ccw(1)
            self.flip_y()
            return
        if from_face == 'B' and paired_face == 'LI':
            self.rotate_cw(1)
            return
        if from_face == 'B' and paired_face == 'L':
            self.rotate_cw(1)
            self.flip_y()
            return
        if from_face == 'T' and paired_face == 'L':
            self.rotate_ccw(1)
            return
        if from_face == 'T' and paired_face == 'RI':
            self.rotate_cw(1)
            return
        assert False, (from_face, paired_face)

    def flip_y(self):
        #print(self.id, "flip y")
        self.lines = [l[::-1] for l in self.lines]
        self.recompute_edges()
 
    def flip_x(self):
        #print(self.id, "flip x")
        self.lines = self.lines[::-1]
        self.recompute_edges()

    def rotate_cw(self, num):
        #print(self.id, "rotate cw", num)
        for _ in range(num):
            # Note: assumes square
            lines = []
            for col in range(0, len(self.lines)):
                lines.append(''.join(l[col] for l in self.lines[::-1]))
            self.lines = lines
        self.recompute_edges()

    def rotate_ccw(self, num):
        #print(self.id, "rotate ccw", num)
        for _ in range(num):
            # Note: assumes square
            lines = []
            for col in range(len(self.lines) - 1, -1, -1):
                lines.append(''.join(l[col] for l in self.lines))
            self.lines = lines
        self.recompute_edges()


tiles = []

for tile in sys.stdin.read().split('\n\n'):
    if not tile.strip():
        continue
    lines = tile.strip().split('\n')
    assert lines[0].startswith('Tile ')
    t_id = int(lines[0].strip()[5:-1])
    tiles.append(Tile(t_id, lines[1:]))

size = int(math.sqrt(len(tiles)))
assert size**2 == len(tiles)

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
    x, y, tile = fringe.pop(0)
    min_x = min(min_x, x)
    min_y = min(min_y, y)
    if tile.completed:
        #assert grid[(x, y)] == tile, (grid[(x, y)], tile)
        continue
    #print(x, y, tile)
    assert (x, y) not in grid, (x, y, grid[(x, y)], tile)
    grid[(x, y)] = tile
    for other in tiles:
        if other == tile:
            continue
        for e, face in tile.edges.items():
            if e in other.transforms:
                tr = other.transforms[e]
                other.orient(face, tr)
                sx, sy = edge_delta[face]
                fringe.append((x + sx, y + sy, other))
    tile.completed = True

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
        for tile in line:
            if not lines:
                lines = list(tile.content)
            else:
                for i, line in enumerate(tile.content):
                    # Concat content
                    lines[i] += line
        image.extend(lines)
    return image

def flip_y(image):
    return [l[::-1] for l in image]

def flip_x(image):
    return image[::-1]

def rotate(image):
    # Note: assumes square
    new_image = []
    for col in range(len(image) - 1, -1, -1):
        new_image.append(''.join(l[col] for l in image))
    return new_image

def mask(line, start, mask):
    new = line[:start]
    for i, m in enumerate(mask):
        c = line[start + i]
        if m == '#':
            c = 'O'
        new += c
    new += line[start + len(mask):]
    return new

def find(image):
    image = list(image)
    possible_l1 = set()
    possible_l2 = set()
    possible_l3 = set()
    found = False
    for l, line in enumerate(image):
        for start in range(len(line)):
            if re.match('..................#.', line[start:]) is not None:
                possible_l1.add((l, start))
            if re.match('#....##....##....###', line[start:]) is not None:
                possible_l2.add((l, start))
            if re.match('.#..#..#..#..#..#...', line[start:]) is not None:
                possible_l3.add((l, start))
    for (l, s) in possible_l1:
        if (l + 1, s) in possible_l2 and (l + 2, s) in possible_l3:
            found = True
            image[l] = mask(image[l], s, '..................#.')
            image[l + 1] = mask(image[l + 1], s, '#....##....##....###')
            image[l + 2] = mask(image[l + 2], s, '.#..#..#..#..#..#...')
    if found:
        print(''.join(image).count('#'))
        exit()

image = build_image(tile_image)
for r in range(4):
    find(image)
    find(flip_x(image))
    find(flip_y(image))
    image = rotate(image)
