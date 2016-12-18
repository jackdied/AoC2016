import itertools as it
from collections import *
import re
from hashlib import md5

'''


'''
tile = '.'
trap = '^'

seed = '^.^^^.^..^....^^....^^^^.^^.^...^^.^.^^.^^.^^..^.^...^.^..^.^^.^..^.....^^^.^.^^^..^^...^^^...^...^.'


def make_row(prev):
    squares = []
    prev = '.' + prev + '.'
    for l, c, r in zip(prev, prev[1:], prev[2:]):
        if ((l == c == trap and r == tile) or
            (c == r == trap and l == tile) or
            (l == trap and c == r == tile) or
            (r == trap and l == c == tile)):
            squares.append(trap)
        else:
            squares.append(tile)
        #print((l, c, r), squares)
    return ''.join(squares)


assert make_row('.') == '.'
assert make_row('..') == '..'
assert make_row('..^^.') == '.^^^^', make_row('..^^.')
assert make_row('.^^^^') == '^^..^'

def main():
    rows = [seed]
    while len(rows) < 400000:
        rows.append(make_row(rows[-1]))
    print("COUNT", sum(row.count('.') for row in rows))
    return


if __name__ == '__main__':
    main()
