import sys

program = []
change_indexes = []
for line in sys.stdin.readlines():
    op, data = line.strip().split(' ')
    data = int(data)
    program.append((op, data))
    if op == 'nop' or op == 'jmp':
        change_indexes.append(len(program) - 1)

while True:
    patched = list(program)
    idx = change_indexes.pop(0)
    op, data = patched[idx]
    if op == 'nop':
        patched[idx] = ('jmp', data)
    else:
        patched[idx] = ('nop', data)
    looped = False
    term = False
    acc = 0
    visited = set()
    ip = 0
    while True:
        if ip in visited:
            looped = True
            break
        if ip == len(patched):
            term = True
            break
        visited.add(ip)
        op, data = patched[ip]
        if op == 'jmp':
            ip += data
            continue
        if op == 'nop':
            pass
        elif op == 'acc':
            acc += data
        ip += 1
    if term:
        break
    assert looped
    
print(acc)
