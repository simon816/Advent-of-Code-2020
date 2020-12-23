class Node:

    def __init__(self, value):
        self.val = value
        self.next = None

starting = [int(n) for n in input()]

val_to_node = {}

root = Node(starting[0])
val_to_node[starting[0]] = root
node = root
for n in starting[1:]:
    node.next = Node(n)
    node = node.next
    val_to_node[n] = node
for n in range(max(starting) + 1, 1000000 + 1):
    node.next = Node(n)
    node = node.next
    val_to_node[n] = node
# complete the cycle
node.next = root

min_val = min(starting)
max_val = 1000000

curr = root
for _ in range(10000000):
    sel = []
    sel_val = set()
    c = curr
    for _ in range(3):
        sel.append(c.next)
        sel_val.add(c.next.val)
        c = c.next
    curr.next = c.next
    dest = curr.val - 1
    while dest in sel_val or dest < min_val:
        dest -= 1
        if dest < min_val:
            dest = max_val
    dest_node = val_to_node[dest]
    end = dest_node.next
    dest_node.next = sel[0]
    sel[-1].next = end
    curr = curr.next

one = val_to_node[1]
print(one.next.val * one.next.next.val)
