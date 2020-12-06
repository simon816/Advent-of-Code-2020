import sys

input = sys.stdin.read()
groups = input.split('\n\n')
print(sum(len(set(g.replace('\n', ''))) for g in groups))
