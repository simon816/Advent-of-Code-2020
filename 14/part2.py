import sys
import itertools

mask = 'X' * 36

mem = {}

def float_addr(a):
    float_vals = itertools.product([0, 1], repeat=mask.count('X'))
    for float_option in float_vals:
        f_iter = iter(float_option)
        new_addr = a
        for i, m in enumerate(mask):
            if m == '0':
                continue
            shift = 35 - i
            bit_val = 1
            b = 1 << shift
            if m == 'X':
                bit_val = next(f_iter)
            if bit_val:
                new_addr |= b
            else:
                if new_addr & b != 0:
                    new_addr -= b
        yield new_addr

for line in sys.stdin.readlines():
    l = line.strip()
    k, v = l.split(' = ')
    if k == 'mask':
        mask = v
        continue
    addr = int(k[k.index('[') + 1:k.index(']')])
    val = int(v)
    for addr in float_addr(addr):
        mem[addr] = val

print(sum(mem.values()))
