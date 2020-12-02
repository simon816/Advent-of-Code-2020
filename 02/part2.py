import sys
import itertools

if __name__ == '__main__':

    valid = 0
    for line in sys.stdin.readlines():
        policy, pw = line.split(':')
        pw = pw.strip()
        positions, letter = policy.split(' ')
        p1, p2 = map(int, positions.split('-'))
        match = 0
        if pw[p1 - 1] == letter:
            match += 1
        if pw[p2 - 1] == letter:
            match += 1
        if match == 1:
            valid += 1
    print(valid)
