import sys

active_set = set()

min_point = [0, 0, 0]
max_point = [0, 0, 0]

def set_cell(x, y, z, val):
    if val:
        active_set.add((x, y, z))
        if x < min_point[0]:
            min_point[0] = x
        if y < min_point[1]:
            min_point[1] = y
        if z < min_point[2]:
            min_point[2] = z
        if x > max_point[0]:
            max_point[0] = x
        if y > max_point[1]:
            max_point[1] = y
        if z > max_point[2]:
            max_point[2] = z
    elif (x, y, z) in active_set:
        active_set.remove((x, y, z))

def get_cell(x, y, z):
    return (x, y, z) in active_set 

def get_active_neighbours(x, y, z):
    active = 0
    for x1 in range(x - 1, x + 2):
        for y1 in range(y - 1, y + 2):
            for z1 in range(z - 1, z + 2):
                if (x1, y1, z1) == (x, y, z):
                    continue
                if (x1, y1, z1) in active_set:
                    active += 1
    return active

z = 0
for y, line in enumerate(sys.stdin.readlines()):
    for x, cell in enumerate(line.strip()):
        set_cell(x, y, z, cell == '#')

for _ in range(6):
    staged = []
    for x in range(min_point[0] - 1, max_point[0] + 2):
        for y in range(min_point[1] - 1, max_point[1] + 2):
            for z in range(min_point[2] - 1, max_point[2] + 2):
                n = get_active_neighbours(x, y, z)
                active = get_cell(x, y, z)
                if active and n != 2 and n != 3:
                    staged.append((x, y, z, False))
                if not active and n == 3:
                    staged.append((x, y, z, True))
    for args in staged:
        set_cell(*args)
    staged = []

print(len(active_set))
