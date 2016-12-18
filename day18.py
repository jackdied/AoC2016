import itertools as it
from collections import *
import re
from hashlib import md5
import functools

'''
I added a variety of make_row() implementations after the original simple one.
Some of them are just as simple (and faster!), most of them are more complicated
with mixed results.

'''
tile = '.'
trap = '^'

seed = '^.^^^.^..^....^^....^^^^.^^.^...^^.^.^^.^^.^^..^.^...^.^..^.^^.^..^.....^^^.^.^^^..^^...^^^...^...^.'

#
# Original make_row (23 seconds)
#
def orig_make_row(prev):
    squares = []
    prev = '.' + prev
    for l, c, r in zip(prev, prev[1:] + '.', prev[2:]+'.'):
        if ((l == c == trap and r == tile) or
            (c == r == trap and l == tile) or
            (l == trap and c == r == tile) or
            (r == trap and l == c == tile)):
            squares.append(trap)
        else:
            squares.append(tile)
    return ''.join(squares)

#
# Original but with the tile/trap logic refactored (28 seconds)
#
# Slower because of the extra bazillion function call overheads

def calc_tile(triple):
    l, c, r = triple
    if ((l == c == trap and r == tile) or
        (c == r == trap and l == tile) or
        (l == trap and c == r == tile) or
        (r == trap and l == c == tile)):
        return trap
    return tile

def refactored_make_row(prev):
    prev = '.' + prev + '.'
    return ''.join(calc_tile(triple) for triple in zip(prev, prev[1:], prev[2:]))

#
# Lookup Table make_row (11 seconds)
#

trans = {triple: calc_tile(triple) for triple in it.product('.^', '.^', '.^')}

def lookup_make_row(prev):
    prev = '.' + prev + '.'
    return ''.join(trans[triple] for triple in zip(prev, prev[1:], prev[2:]))

#
# Lookup Table with strings (19 seconds)
#
# as above, but use length 3 strings instead of tuples
# slower because we execute lots more bytecodes per character

trans.update({''.join(triple): trans[triple] for triple in trans.keys()})

def string_lookup_make_row(prev):
    prev = '.' + prev + '.'
    return ''.join(trans[prev[i:i+3]] for i in range(len(prev)-2))

#
# Lookup Table with peek ahead (14 seconds)
#
# We know the current (left, center, right) so we make a tiny lookup dict
# that returns the next triple based on the current one and the next char
# (left, center, right) becomes (center, right, new_char)
#
# This ends up being slower because of all the temporaries.

trans_peek = {}
for triple, v in trans.items():
    chars = ''.join(triple)
    next_triples = {c:chars[1:]+c for c in '.^'}
    trans_peek[chars] = (v, next_triples)

def fancy_lookup_make_row(prev):
    chars = iter(prev+'.')
    curr = '.' + next(chars) + next(chars)
    out = []
    try:
        while True:
            v, lookup = trans_peek[curr]
            out.append(v)
            curr = lookup[next(chars)]
    except StopIteration:
        pass
    return ''.join(out)


#
# cache translated subsets of strings (6 secs)
# Shitty complicated, but faster

import functools
@functools.lru_cache(None)
def make_8(row):
    # translate all the middle triples (don't try to translate 1st and last chars)
    retval = ''.join(trans[triple] for triple in zip(row, row[1:], row[2:]))
    assert len(retval) == len(row) - 2
    return retval

def cachable_make_row(prev):
    orig = prev
    prev = '.' + prev + '.'
    eight = 8  # tunable, but it turns out 8 is the optimal number
    prev += '.' * (eight - len(prev) % eight)
    inds = list(range(1, len(prev)+eight, eight))
    prev += '.' # IDK
    return ''.join(make_8(prev[i-1:j+1]) for i,j in zip(inds, inds[1:]))[:len(orig)]


make_row = orig_make_row
make_row = string_lookup_make_row
make_row = lookup_make_row

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
