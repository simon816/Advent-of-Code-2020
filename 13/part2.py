import sys

sys.stdin.readline()
input = sys.stdin.readline().strip().split(',')
busses = []
offs = []
for i, b in enumerate(input):
    if b != 'x':
        v = int(b)
        busses.append(v)
        offs.append(i)

stride = busses.pop(0)
offs.pop(0)

x = 0
while busses:
    curr = busses.pop(0)
    off = offs.pop(0)
    while (x + off) % curr != 0:
        x += stride
    stride *= curr
print(x)
