starting = list(map(int, input().split(',')))

last_spoken = {}

turn = 1
last = None
for n in starting:
    last_spoken[n] = (turn, None)
    turn += 1
    last = n

while turn <= 2020:
    last_turn, prev_spoken = last_spoken[last]
    if prev_spoken is None:
        last = 0
    else:
        last = last_turn - prev_spoken
    if last in last_spoken:
        last_spoken_last, _ = last_spoken[last]
    else:
        last_spoken_last = None
    last_spoken[last] = (turn, last_spoken_last)
    turn += 1

print(last)
