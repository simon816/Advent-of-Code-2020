import sys

grid = []
for line in sys.stdin.readlines():
    grid.append([c for c in line.strip()])

def get_occ_seat_count(x, y, grid):
    adj = []
    count = 0
    scan_x = x
    while scan_x > 0:
        if grid[y][scan_x - 1] in 'L#':
            count += grid[y][scan_x - 1].count('#')
            break
        scan_x -= 1
    scan_x = x
    while scan_x < len(grid[y]) - 1:
        if grid[y][scan_x + 1] in 'L#':
            count += grid[y][scan_x + 1].count('#')
            break
        scan_x += 1
    scan_y = y
    while scan_y > 0:
        if grid[scan_y - 1][x] in 'L#':
            count += grid[scan_y - 1][x].count('#')
            break
        scan_y -= 1
    scan_y = y
    while scan_y < len(grid) - 1:
        if grid[scan_y + 1][x] in 'L#':
            count += grid[scan_y + 1][x].count('#')
            break
        scan_y += 1
    scan_x = x
    scan_y = y
    while scan_x > 0 and scan_y > 0:
        if grid[scan_y - 1][scan_x - 1] in 'L#':
            count += grid[scan_y - 1][scan_x - 1].count('#')
            break
        scan_x -= 1
        scan_y -= 1
    scan_x = x
    scan_y = y
    while scan_x < len(grid[y]) - 1 and scan_y < len(grid) - 1:
        if grid[scan_y + 1][scan_x + 1] in 'L#':
            count += grid[scan_y + 1][scan_x + 1].count('#')
            break
        scan_x += 1
        scan_y += 1
    scan_x = x
    scan_y = y
    while scan_x < len(grid[y]) - 1 and scan_y > 0:
        if grid[scan_y - 1][scan_x + 1] in 'L#':
            count += grid[scan_y - 1][scan_x + 1].count('#')
            break
        scan_x += 1
        scan_y -= 1
    scan_x = x
    scan_y = y
    while scan_x > 0 and scan_y < len(grid) - 1:
        if grid[scan_y + 1][scan_x - 1] in 'L#':
            count += grid[scan_y + 1][scan_x - 1].count('#')
            break
        scan_x -= 1
        scan_y += 1
    return count

change = True
while change:
    new = []
    change = False
    for y, row in enumerate(grid):
        new_row = []
        for x, cell in enumerate(row):
            count = get_occ_seat_count(x, y, grid)
            if cell == 'L':
                if count == 0:
                    new_row.append('#')
                    change = True
                else:
                    new_row.append('L')
            elif cell == '#':
                if count >= 5:
                    new_row.append('L')
                    change = True
                else:
                    new_row.append('#')
            else:
                new_row.append(cell)
        new.append(new_row)
    grid = new

print(sum(r.count('#') for r in grid))
