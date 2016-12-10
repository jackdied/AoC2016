import itertools as it
from collections import *
import re

'''

'''

WIDTH = 50
HEIGHT = 6
lines = open('day8_input.txt').readlines()

def rect(screen, width, height):
    ''' turn on pixels in the rectangle defined by a & b '''
    new_screen = set(screen)
    for x in range(0, width):
        for y in range(0, height):
            new_screen.add((x, y))
    return new_screen

def rotrow(screen, row, cnt):
    new_screen = set()

    # copy unchanged
    for y in range(HEIGHT):
        if y == row:
            continue
        for x in range(WIDTH):
            if (x, y) in screen:
                new_screen.add((x, y))

    for x in range(WIDTH):
        rotx = (x + cnt) % WIDTH
        if (x, row) in screen:
            new_screen.add((rotx, row))
    return new_screen

def rotcol(screen, row, cnt):
    new_screen = set()

    # copy unchanged
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if x == row:
                continue
            if (x, y) in screen:
                new_screen.add((x, y))

    for y in range(HEIGHT):
        roty = (y + cnt) % HEIGHT
        if (row, y) in screen:
            new_screen.add((row, roty))
    return new_screen

def exec_line(screen, line):
    _rect = (rect, re.compile('rect (\d+)x(\d+)'))
    _rotrow = (rotrow, re.compile('rotate row y=(\d+) by (\d+)'))
    _rotcol = (rotcol, re.compile('rotate column x=(\d+) by (\d+)'))
    parsers = [_rect, _rotrow, _rotcol]
    for func, parse in parsers:
        if parse.match(line):
            args = map(int, parse.match(line).groups())
            return func(screen, *args)

def main():
    screen = set()
    for line in lines:
        screen = exec_line(screen, line)
    print("CNT", len(screen))
    for y in range(HEIGHT):
        line = ''
        for x in range(WIDTH):
            if (x, y) in screen:
                line += 'X'
            else:
                line += ' '
        print(line)

if __name__ == '__main__':
    main()
