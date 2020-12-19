import sys
import re
from lark import Lark

rules, messages = sys.stdin.read().split('\n\n')

grammar = []

for rule in rules.split('\n'):
    if not rule:
        continue
    id, r = rule.split(':')
    r = r.strip()
    if r.startswith('"'):
        grammar.append('r_%s: %s' % (id, r))
    else:
        grammar.append('r_%s: %s' % (id, re.sub('(\d+)', r'r_\1', r)))

grammar = '\n'.join(grammar)
parser = Lark(grammar, start='r_0')

match = 0

for m in messages.split('\n'):
    m = m.strip()
    if not m:
        continue
    try:
        parser.parse(m)
        match += 1
    except:
        pass

print(match)
