import sys

program = []
for line in sys.stdin.readlines():
    op, data = line.strip().split(' ')
    data = int(data)
    program.append((op, data))

acc = 0
visited = set()
ip = 0
while ip not in visited:
    visited.add(ip)
    op, data = program[ip]
    if op == 'jmp':
        ip += data
        continue
    if op == 'nop':
        pass
    elif op == 'acc':
        acc += data
    ip += 1

print(acc)
