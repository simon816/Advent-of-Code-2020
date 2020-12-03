import sys

lines = list(sys.stdin.readlines())

result = 1

for (h, v) in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
    count = 0
    x = 0
    line_num = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if x == 0:
            x = h
            line_num += 1
            continue
        if line_num % v != 0:
            line_num += 1
            continue
        line_num += 1
        if line[x % len(line)] == '#':
            count += 1
        x += h
    result *= count

print(result)
