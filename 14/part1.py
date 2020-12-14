import sys

mask = 'X' * 36

mem = {}

def apply_mask(v):
    for i, m in enumerate(mask):
        shift = 35 - i
        b = 1 << shift
        if m == '0':
            if v & b != 0:
                v -= b
        elif m == '1':
            v |= b
    return v

for line in sys.stdin.readlines():
    l = line.strip()
    k, v = l.split(' = ')
    if k == 'mask':
        mask = v
        continue
    addr = int(k[k.index('[') + 1:k.index(']')])
    val = int(v)
    mem[addr] = apply_mask(val)

print(sum(mem.values()))
