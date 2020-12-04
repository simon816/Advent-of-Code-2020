import sys

data = sys.stdin.read()

valid = 0

for passport in data.split('\n\n'):
    need = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])
    pairs = passport.replace('\n', ' ').split(' ')
    for p in pairs:
        if not p:
            continue
        k, v = p.split(':')
        if k in need:
            need.remove(k)
    if not len(need):
        valid += 1

print(valid)
