import sys

min_dep = int(sys.stdin.readline())
busses = sys.stdin.readline().strip().split(',')
busses = [int(b) for b in busses if b != 'x']
dm = [(divmod(min_dep, b), b) for b in busses]
exact = [d[1] for d in dm if d[0][1] == 0]
if exact:
    bus = exact[0]
    wait = 0
else:
    next_time = [((d[0][0] + 1) * d[1], d[1]) for d in dm]
    next = min(next_time, key=lambda d: d[0])
    time, bus = next
    wait = time - min_dep

print(wait * bus)
