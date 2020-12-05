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

max_sid = 0

for l in sys.stdin.readlines():
    l = l.strip()
    rowsel = l[:7]
    colsel = l[7:]
    row = search(rowsel, 'F')
    col = search(colsel, 'L')
    sid = row * 8 + col
    if sid > max_sid:
        max_sid = sid

print(max_sid)
