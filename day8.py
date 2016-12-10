import itertools as it
from collections import *
import re

'''

'''

WIDTH = 50
HEIGHT = 6
ALLPOS = [(x, y) for x in range(WIDTH) for y in range(HEIGHT)]
lines = open('day8_input.txt').readlines()


def make_rect(screen, width, height):
    rect = set((x, y) for x in range(width) for y in range(height))
    return rect | screen

def make_rotrow(screen, row, count):
    def rotrow_mutator(x, y):
        if y == row:
            x = (x + count) % WIDTH
        return (x, y)
    return set(it.starmap(rotrow_mutator, screen))

def make_rotcol(screen, col, count):
    def rotcol_mutator(x, y):
        if x == col:
            y = (y + count) % HEIGHT
        return (x, y)
    return set(it.starmap(rotcol_mutator, screen))

def exec_line(screen, line):
    _rect = (make_rect, re.compile('rect (\d+)x(\d+)'))
    _rotrow = (make_rotrow, re.compile('rotate row y=(\d+) by (\d+)'))
    _rotcol = (make_rotcol, re.compile('rotate column x=(\d+) by (\d+)'))
    parsers = [_rect, _rotrow, _rotcol]
    for func, parse in parsers:
        if parse.match(line):
            args = map(int, parse.match(line).groups())
            return func(screen, *args)

def pprint_screen(screen):
    for y in range(HEIGHT):
        line = ''
        for x in range(WIDTH):
            if (x, y) in screen:
                line += 'X'
            else:
                line += ' '
        print(line)

def main():
    screen = set()
    for line in lines:
        screen = exec_line(screen, line)
    print("CNT", len(screen))
    pprint_screen(screen)

if __name__ == '__main__':
    main()
