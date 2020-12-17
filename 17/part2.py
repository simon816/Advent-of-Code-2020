import sys

active_set = set()

min_point = [0, 0, 0, 0]
max_point = [0, 0, 0, 0]

def set_cell(x, y, z, w, val):
    if val:
        active_set.add((x, y, z, w))
        if x < min_point[0]:
            min_point[0] = x
        if y < min_point[1]:
            min_point[1] = y
        if z < min_point[2]:
            min_point[2] = z
        if w < min_point[3]:
            min_point[3] = w
        if x > max_point[0]:
            max_point[0] = x
        if y > max_point[1]:
            max_point[1] = y
        if z > max_point[2]:
            max_point[2] = z
        if w > max_point[3]:
            max_point[3] = w
    elif (x, y, z, w) in active_set:
        active_set.remove((x, y, z, w))

def get_cell(x, y, z, w):
    return (x, y, z, w) in active_set 

def get_active_neighbours(x, y, z, w):
    active = 0
    for x1 in range(x - 1, x + 2):
        for y1 in range(y - 1, y + 2):
            for z1 in range(z - 1, z + 2):
                for w1 in range(w - 1, w + 2):
                    if (x1, y1, z1, w1) == (x, y, z, w):
                        continue
                    if (x1, y1, z1, w1) in active_set:
                        active += 1
    return active

z = 0
w = 0
for y, line in enumerate(sys.stdin.readlines()):
    for x, cell in enumerate(line.strip()):
        set_cell(x, y, z, w, cell == '#')

for _ in range(6):
    staged = []
    for x in range(min_point[0] - 1, max_point[0] + 2):
        for y in range(min_point[1] - 1, max_point[1] + 2):
            for z in range(min_point[2] - 1, max_point[2] + 2):
                for w in range(min_point[3] - 1, max_point[3] + 2):
                    n = get_active_neighbours(x, y, z, w)
                    active = get_cell(x, y, z, w)
                    if active and n != 2 and n != 3:
                        staged.append((x, y, z, w, False))
                    if not active and n == 3:
                        staged.append((x, y, z, w, True))
    for args in staged:
        set_cell(*args)
    staged = []

print(len(active_set))
