import sys
import operator
from functools import reduce

groups = sys.stdin.read().strip().split('\n\n')

print(sum(len(list(reduce(operator.and_, map(set, g.split('\n'))))) for g in groups))
