import sys

def search(sel, low):
    mi = 0
    ma = (2 ** len(sel)) - 1
    step = 2 ** (len(sel) - 1)
    for c in sel:
        if c == low:
            ma -= step
        else:
            mi += step
        step //= 2
    assert mi == ma
    return mi

all = set()

for l in sys.stdin.readlines():
    l = l.strip()
    rowsel = l[:7]
    colsel = l[7:]
    row = search(rowsel, 'F')
    col = search(colsel, 'L')
    all.add(row * 8 + col)

for n in range(128 * 8):
    if n not in all and n + 1 in all and n - 1 in all:
        print(n)
