import sys
import itertools

if __name__ == '__main__':

    values = [int(line.strip()) for line in sys.stdin.readlines()]
    for (a, b) in itertools.combinations(values, 2):
        if a + b ==  2020:
            print(a * b)
