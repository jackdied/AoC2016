import itertools as it
from collections import *
import re

lines = list(open('day7_input.txt'))

def has_aba(txt):
    for a, b, c, in zip(txt, txt[1:], txt[2:]):
        if a == c and a != b:
            yield a+b+c
    return

assert list(has_aba('aba')) == ['aba']
assert list(has_aba('abaxyx')) == ['aba', 'xyx']


def is_tls(line):
    abas = []
    hyper = ''
    oline = line
    while line:
        pre = mid = pos = ''
        m = re.match('(\w*)\[(\w*)\](.*)', line)
        if m:
            pre, mid, post = m.groups()
            line = post
        else:
            pre = line
            line = ''
        abas.extend(has_aba(pre))
        hyper += ' ' + mid

    for aba in abas:
        a, b, c = aba
        if b+a+b in hyper:
            return True
    return False

def main():
    good = 0
    for line in lines:
        if is_tls(line):
            good += 1
    print(good, len(lines))

if __name__ == '__main__':
    main()
