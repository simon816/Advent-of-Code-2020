import sys
import itertools

if __name__ == '__main__':

    valid = 0
    for line in sys.stdin.readlines():
        policy, pw = line.split(':')
        pw = pw.strip()
        range, letter = policy.split(' ')
        min, max = map(int, range.split('-'))
        count = pw.count(letter)
        if count >= min and count <= max:
            valid += 1
    print(valid)
