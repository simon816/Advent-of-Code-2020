import sys

grid = []
for line in sys.stdin.readlines():
    grid.append([c for c in line.strip()])

def get_adj(x, y, grid):
    adj = []
    if y > 0:
        adj.append(grid[y - 1][x])
        if x > 0:
            adj.append(grid[y - 1][x - 1])
        if x < len(grid[y - 1]) - 1:
            adj.append(grid[y - 1][x + 1])
    if y < len(grid) - 1:
        adj.append(grid[y + 1][x])
        if x > 0:
            adj.append(grid[y + 1][x - 1])
        if x < len(grid[y + 1]) -1:
            adj.append(grid[y + 1][x + 1])
    if x > 0:
        adj.append(grid[y][x - 1])
    if x < len(grid[y]) - 1:
        adj.append(grid[y][x + 1])
    return adj

change = True
while change:
    new = []
    change = False
    for y, row in enumerate(grid):
        new_row = []
        for x, cell in enumerate(row):
            if cell == 'L':
                adj = get_adj(x, y, grid)
                if adj.count('#') == 0:
                    new_row.append('#')
                    change = True
                else:
                    new_row.append('L')
            elif cell == '#':
                adj = get_adj(x, y, grid)
                if adj.count('#') >= 4:
                    new_row.append('L')
                    change = True
                else:
                    new_row.append('#')
            else:
                new_row.append(cell)
        new.append(new_row)
    grid = new

print(sum(r.count('#') for r in grid))
