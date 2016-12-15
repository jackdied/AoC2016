import itertools as it
from collections import *
import re

'''
Disc #1 has 7 positions; at time=0, it is at position 0.
Disc #2 has 13 positions; at time=0, it is at position 0.
Disc #3 has 3 positions; at time=0, it is at position 2.
Disc #4 has 5 positions; at time=0, it is at position 2.
Disc #5 has 17 positions; at time=0, it is at position 0.
Disc #6 has 19 positions; at time=0, it is at position 7.
'''

def make_disc(stops):
        return deque([1]+[0]*(stops-1), stops)

def initial():
    discs = list(map(make_disc, [7, 13, 3, 5, 17, 19]))  # Part 1
    discs = list(map(make_disc, [7, 13, 3, 5, 17, 19, 11]))  # Part 2
    for _ in range(2):
        discs[2].rotate()
    for _ in range(2):
        discs[3].rotate()
    for _ in range(7):
        discs[5].rotate()
    assert discs[0][0]
    assert discs[2][2]
    assert discs[3][2]
    assert discs[5][7]
    for i, d in enumerate(discs):
        print(i, d)
    return discs

def _initial():
    discs = list(map(make_disc, [5, 2]))
    for _ in range(4):
        discs[0].rotate()
    for _ in range(1):
        discs[1].rotate()
    for i, d in enumerate(discs):
        print(i, d)
    return discs

def main():
    discs = initial()
    tim = 0
    def pp():
        for i, d in enumerate(discs):
            print('  ', i, d)
    def advance():
        for d in discs:d.rotate(1)
    tim += 1
    advance()
    pp()
    while not all(disc[-i] for i, disc in enumerate(discs)):
            advance()
            tim += 1
    print("WIN!", tim-1) # 176737 too high! so is 176737
    pp()

if __name__ == '__main__':
    main()
