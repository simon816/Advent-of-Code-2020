import sys

count = 0
x = 0
for line in sys.stdin.readlines():
    line = line.strip()
    if not line:
        continue
    if x == 0:
        x = 3
        continue
    if line[x % len(line)] == '#':
        count += 1
    x += 3
print(count)
