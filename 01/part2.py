import sys
import itertools

if __name__ == '__main__':

    values = [int(line.strip()) for line in sys.stdin.readlines()]
    for (a, b, c) in itertools.combinations(values, 3):
        if a + b + c ==  2020:
            print(a * b * c)
