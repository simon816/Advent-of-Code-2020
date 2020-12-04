import sys

data = sys.stdin.read()

valid = 0

for passport in data.split('\n\n'):
    need = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])
    pairs = passport.replace('\n', ' ').split(' ')
    bad = False
    for p in pairs:
        if not p:
            continue
        k, v = p.split(':')
        if k in need:
            need.remove(k)
        if k == 'byr':
            try:
                v = int(v)
                bad = v < 1920 or v > 2002
            except:
                bad = True
        if k == 'iyr':
            try:
                v = int(v)
                bad = v < 2010 or v > 2020
            except:
                bad = True
        if k == 'eyr':
            try:
                v = int(v)
                bad = v < 2020 or v > 2030
            except:
                bad = True
        if k == 'hgt':
            try:
                n = int(v[:-2])
            except:
                bad = True
            if not bad and v.endswith('cm'):
                bad = n < 150 or n > 193
            elif not bad and v.endswith('in'):
                bad = n < 59 or n > 76
            else:
                bad = True
        if k == 'hcl':
            if not v.startswith('#'):
                bad = True
            else:
                try:
                    int(v[1:], 16)
                except:
                    bad = True
        if k == 'ecl':
            bad = v not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
        if k == 'pid':
            bad = len(v) != 9
            try:
                int(v)
            except:
                bad = True
        if bad:
            print(k, v)
            break
    if not len(need) and not bad:
        valid += 1

print(valid)
