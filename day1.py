'''

--- Day 1: No Time for a Taxicab ---

Santa's sleigh uses a very high-precision clock to guide its movements, and the clock's oscillator is regulated by stars. Unfortunately, the stars have been stolen... by the Easter Bunny. To save Christmas, Santa needs you to retrieve all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You're airdropped near Easter Bunny Headquarters in a city somewhere. "Near", unfortunately, is as close as you can get - the instructions on the Easter Bunny Recruiting Document the Elves intercepted start here, and nobody had time to work them out further.

The Document indicates that you should start at the given coordinates (where you just landed) and face North. Then, follow the provided sequence: either turn left (L) or right (R) 90 degrees, then walk forward the given number of blocks, ending at a new intersection.

There's no time to follow such ridiculous instructions on foot, though, so you take a moment and work out the destination. Given that you can only walk on the street grid of the city, how far is the shortest path to the destination?

For example:

Following R2, L3 leaves you 2 blocks East and 3 blocks North, or 5 blocks away.
R2, R2, R2 leaves you 2 blocks due South of your starting position, which is 2 blocks away.
R5, L5, R5, R3 leaves you 12 blocks away.
How many blocks away is Easter Bunny HQ?

'''

my_input = 'L3, R2, L5, R1, L1, L2, L2, R1, R5, R1, L1, L2, R2, R4, L4, L3, L3, R5, L1, R3, L5, L2, R4, L5, R4, R2, L2, L1, R1, L3, L3, R2, R1, L4, L1, L1, R4, R5, R1, L2, L1, R188, R4, L3, R54, L4, R4, R74, R2, L4, R185, R1, R3, R5, L2, L3, R1, L1, L3, R3, R2, L3, L4, R1, L3, L5, L2, R2, L1, R2, R1, L4, R5, R4, L5, L5, L4, R5, R4, L5, L3, R4, R1, L5, L4, L3, R5, L5, L2, L4, R4, R4, R2, L1, L3, L2, R5, R4, L5, R1, R2, R5, L2, R4, R5, L2, L3, R3, L4, R3, L2, R1, R4, L5, R1, L5, L3, R4, L2, L2, L5, L5, R5, R2, L5, R1, L3, L2, L2, R3, L3, L4, R2, R3, L1, R2, L5, L3, R4, L4, R4, R3, L3, R1, L3, R5, L5, R1, R5, R3, L1'

def turn(start_cardinal, leftright):
    assert leftright in ('L', 'R')
    if leftright == 'L':
        return {'N': 'W', 'W': 'S', 'S': 'E', 'E': 'N'}[start_cardinal]
    else:
        return {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}[start_cardinal]

def step(start_pos, start_cardinal, step_count):
    inc = {'N': (0, 1), 'E': (1, 0), 'S': (0, -1), 'W': (-1, 0)}
    x, y = start_pos
    dx, dy = inc[start_cardinal]
    for _ in range(step_count):
        x += dx
        y += dy
    return x, y

def move(start, instruction):
    (x, y), cardinal = start
    do_turn, do_steps = instruction[0], int(instruction[1:])
    cardinal = turn(cardinal, do_turn)
    return step((x, y), cardinal, do_steps), cardinal

_zero = ((0, 0), 'N')

assert move(_zero, 'R1') == ((1, 0), 'E'), move(_zero, 'R1')
assert move(_zero, 'L2') == ((-2, 0), 'W'), move(_zero, 'L2')

def main():
    instructions = [instr.strip() for instr in my_input.split(',')]
    here = ((0, 0), 'N')
    for instr in instructions:
        here = move(here, instr)
        print here
    print here

if __name__ == '__main__':
    main()
