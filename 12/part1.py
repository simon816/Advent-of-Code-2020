import sys
import itertools

shift = {
    'N': (0, 1),
    'E': (1, 0),
    'S': (0, -1),
    'W': (-1, 0),
}
dirs = iter(itertools.cycle('NESW'))
x, y = 0, 0
while next(dirs) != 'E':
    pass
h = 'E'

for insn in sys.stdin.readlines():
    insn = insn.strip()
    op, val = insn[0], insn[1:]
    val = int(val)
    if op == 'N':
        y += val
    elif op == 'S':
        y -= val
    elif op == 'E':
        x += val
    elif op == 'W':
        x -= val
    elif op in 'LR':
        assert val in [90, 180, 270]
        mag = val // 90
        if op == 'L':
            mag = 4 - mag
        for _ in range(mag):
            h = next(dirs)
    elif op == 'F':
        sx, sy = shift[h]
        x += sx * val
        y += sy * val

print(abs(x) + abs(y))
