import sys
import re

def tokenize(s):
    curr_num = None
    for c in s:
        if c.isdigit():
            if curr_num is None:
                curr_num = int(c)
            else:
                curr_num *= 10
                curr_num += int(c)
        else:
            if curr_num is not None:
                yield curr_num
                curr_num = None
            if c.isspace():
                continue
            if c in '()+*':
                yield c
            else:
                assert False, c

la = []

def push_back(t):
    la.append(t)

def next_token(stream):
    if la:
        return la.pop(0)
    return next(stream)

def eval_expr(tokens):
    value = parse_term(tokens)
    while True:
        try:
            op = next_token(tokens)
        except StopIteration:
            break
        if op not in '*+':
            push_back(op)
            break
        right = parse_term(tokens)
        if op == '+':
            value += right
        else:
            value *= right
    return value

def parse_term(tokens):
    t = next_token(tokens)
    if type(t) == int:
        return t
    if t == '(':
        v = eval_expr(tokens)
        t = next_token(tokens)
        assert t == ')', t
        return v
    assert False, t

def eval_line(e):
    return eval_expr(tokenize(e))

print(sum(eval_line(e) for e in sys.stdin.readlines()))
