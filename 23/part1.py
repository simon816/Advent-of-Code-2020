cups = [int(n) for n in input()]


curr_idx = 0
for _ in range(100):
    curr = cups[curr_idx]
    print("Curr", curr, "[", curr_idx, "]")
    sel = []
    for n in range(3):
        i = (curr_idx + n + 1) % len(cups)
        sel.append(cups[i])
        cups[i] = None
    print("Sel", sel)
    cups = [n for n in cups if n is not None]
    dest = curr - 1
    while dest not in cups:
        dest -= 1
        if dest < min(cups):
            dest = max(cups)
    print("Dest", dest)
    dest_idx = cups.index(dest) + 1
    cups = cups[:dest_idx] + sel + cups[dest_idx:]
    print(cups)
    curr_idx = (cups.index(curr) + 1) % len(cups)

one = cups.index(1)
print(''.join(str(n) for n in cups[one + 1:] + cups[:one]))
