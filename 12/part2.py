import sys

w_x, w_y = 10, 1
s_x, s_y = 0, 0

for insn in sys.stdin.readlines():
    insn = insn.strip()
    op, val = insn[0], insn[1:]
    val = int(val)
    if op == 'N':
        w_y += val
    elif op == 'S':
        w_y -= val
    elif op == 'E':
        w_x += val
    elif op == 'W':
        w_x -= val
    elif op in 'LR':
        if val == 270:
            op = 'L' if op == 'R' else 'R'
            val = 90
        if val == 180:
            w_x = -w_x
            w_y = -w_y
        else:
            o_x, o_y = w_x, w_y
            if op == 'L':
                w_y = o_x
                w_x = -o_y
            else:
                w_y = -o_x
                w_x = o_y
    elif op == 'F':
        s_x += w_x * val
        s_y += w_y * val

print(abs(s_x) + abs(s_y))
