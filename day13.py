import itertools as it
from collections import *
import re

'''
--- Day 13: A Maze of Twisty Little Cubicles ---

You arrive at the first floor of this new building to discover a much less welcoming environment than the shiny atrium of the last one. Instead, you are in a maze of twisty little cubicles, all alike.

Every location in this area is addressed by a pair of non-negative integers (x,y). Each such coordinate is either a wall or an open space. You can't move diagonally. The cube maze starts at 0,0 and seems to extend infinitely toward positive x and y; negative values are invalid, as they represent a location outside the building. You are in a small waiting area at 1,1.

While it seems chaotic, a nearby morale-boosting poster explains, the layout is actually quite logical. You can determine whether a given x,y coordinate will be a wall or an open space using a simple system:

Find x*x + 3*x + 2*x*y + y + y*y.
Add the office designer's favorite number (your puzzle input).
Find the binary representation of that sum; count the number of bits that are 1.
If the number of bits that are 1 is even, it's an open space.
If the number of bits that are 1 is odd, it's a wall.
For example, if the office designer's favorite number were 10, drawing walls as # and open spaces as ., the corner of the building containing 0,0 would look like this:

  0123456789
0 .#.####.##
1 ..#..#...#
2 #....##...
3 ###.#.###.
4 .##..#..#.
5 ..##....#.
6 #...##.###
Now, suppose you wanted to reach 7,4. The shortest route you could take is marked as O:

  0123456789
0 .#.####.##
1 .O#..#...#
2 #OOO.##...
3 ###O#.###.
4 .##OO#OO#.
5 ..##OOO.#.
6 #...##.###
Thus, reaching 7,4 would take a minimum of 11 steps (starting from your current location, 1,1).

What is the fewest number of steps required for you to reach 31,39?


--- Part Two ---

How many locations (distinct x,y coordinates, including your starting location) can you reach in at most 50 steps?
'''

my_input = 1362

def iswall(x, y, seed=my_input):
    n = seed + x*x + 3*x + 2*x*y + y + y*y
    ns = bin(n)[2:]
    ones = ns.count('1')
    if ones % 2 == 0:
        return False
    else:
        return True

test_answer = '''.#.####.##
..#..#...#
#....##...
###.#.###.
.##..#..#.
..##....#.
#...##.###'''

test_d = {}
for y, row in enumerate(test_answer.split('\n')):
    for x, c in enumerate(row):
        if c == '#':
            assert iswall(x, y, 10), (x, y, 10)
        elif c == '.':
            assert not iswall(x, y, 10), (x, y, 10)
        else:
            assert False, c

def neighs(pos):
    x, y = pos
    if x > 0:
        yield x - 1, y
    if y > 0:
        yield x, y - 1
    yield x+1, y
    yield x, y+1

def pprint_maze(maze, curr):
    for x in range(20):
        line = ''
        for y in range(20):
            if (x, y) == curr:
                line += 'X'
            else:
                line += '.#'[iswall(x, y)]
        print(line)

class LazyMaze(dict):
    def __missing__(self, pos):
        v = iswall(*pos)
        self[pos] = v
        return v
        
def main(start=(1,1), goal=(31, 39), maxcost=None):
    maze = LazyMaze()
    best = {}
    stack = [(start, 0)]
    seen = set()  # for Part2
    while stack:
        pos, cost = stack.pop()
        if maxcost is not None and cost > maxcost:  # for Part2
            continue
        seen.add(pos)  # for Part2
        if pos in best:
            if best[pos] <= cost:  # someone already visited here in fewer moves
                continue
            best[pos] = cost
            if pos == goal:
                print("WIN!", cost)
                continue
        for newpos in list(neighs(pos)):
            if not maze[newpos] and ((newpos not in best) or best[newpos] > cost):
                # we can get to newpos for cost+1
                # we don't want anyone that can get there in cost+2 or more to visit
                # so set the best value to cost+2 to keep out longer paths than ours
                best[newpos] = cost+2
                stack.append((newpos, cost+1))
    print("LEN SEEN", len(seen))
    pprint_maze(maze, goal)
    return

if __name__ == '__main__':
    main()
    main(maxcost=50)


