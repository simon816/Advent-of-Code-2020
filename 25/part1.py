
card = int(input())
door = int(input())

c_loop = None

value = 1
i = 1
while c_loop is None:
    value = value * 7
    value = value % 20201227
    if value == card:
        c_loop = i
    i += 1

value = 1
for _ in range(c_loop):
    value = value * door
    value = value % 20201227

print(value)
