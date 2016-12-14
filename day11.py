import itertools as it
from collections import *
import re
from string import ascii_lowercase as alphabet
from peekable import Peekable

'''
I tried several things to speed this up but only two worked (I removed some caching that was a meh 10% speedup)
1) normalize_floors() -- If there are three matching chip-generator pairs on a level moving one is the same
   as moving any of the others. So after each move re-assign letters to the whole puzzle top-to-bottom-left-to-right.
   This massively reduces the number of total possible states.
2) score and sort untried moves on the stack. A good scoring function is required and you can't be sure
   you are right, but a 10x speedup (30 seconds down to 3) when we are right.

I didn't try any heuristics in moving. Like a rubik's cube or Tower of Hanoi there must be
repeatable ways to swap items/clear floors/whatever. You could just compile a series of winning moves from those, probably.
'''


# Part1
my_input = '''The first floor contains a thulium generator, a thulium-compatible microchip, a plutonium generator, and a strontium generator.
The second floor contains a plutonium-compatible microchip and a strontium-compatible microchip.
The third floor contains a promethium generator, a promethium-compatible microchip, a ruthenium generator, and a ruthenium-compatible microchip.
The fourth floor contains nothing relevant.'''

# Part2
my_input = '''The first floor contains a thulium generator, a thulium-compatible microchip, a plutonium generator, and a strontium generator.  An elerium generator. An elerium-compatible microchip. A dilithium generator.A dilithium-compatible microchip.
The second floor contains a plutonium-compatible microchip and a strontium-compatible microchip.
The third floor contains a promethium generator, a promethium-compatible microchip, a ruthenium generator, and a ruthenium-compatible microchip.
The fourth floor contains nothing relevant.'''

sample_input = '''The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.'''

# figure out the words used for things (plutonium, derpanium, etc)
pair_re = re.compile('(\w+)(?:-compatible)? (generator|microchip)')
kinds = set(adj for adj, noun in pair_re.findall(my_input))
# Let's use 'ABC..' for chips and 'abc..' for generators
kind_to_letter = dict(zip(kinds, alphabet))


# eat the input and make it like ['a', 'C', 'b', ..] instead of ['plutonium', ..]
floors = []
for line in my_input.split('\n'):
    floor = []
    for adj, noun in pair_re.findall(line):
        letter = kind_to_letter[adj]
        if noun == 'microchip':
            letter = letter.upper()
        else:
            letter = letter.lower()
        floor.append(letter)
    floors.append(tuple(sorted(floor)))

print("INITIAL", floors)

def valid_floor(floor):
    # if there is a microchip that doesn't have a matching generator
    unshielded_micros = any(x for x in floor if x.lower() not in floor)
    if not unshielded_micros:
        return True  # nothing to fry!
    any_gens = any(x for x in floor if x >= 'a')  # ASCII sorting, lowercase is greater
    if any_gens:
        # chip isn't safe/matched and there are some generators
        return False
    return True

def valid_state(floors):
    return all(valid_floor(floor) for floor in floors)

assert valid_state(floors)  # it better be!

def next_moves(state):
    curr, floors = state
    # four floors, zero can only go up, four can only go down
    avail_dirs = {0: [1], 1: [-1, 1], 2: [1, -1], 3: [-1]}
    for move_dir in avail_dirs[curr]:
        here = floors[curr]
        for move_obs in sorted(it.chain(it.combinations(here, 1), # 1 item from here
                                        it.combinations(here, 2))): # 2 items from here
            yield (move_obs, move_dir)
    return

def normalize_floors(floors):
    ''' we don't care about the name of a pair of matching items on a floor ..
        moving microchip-A or microchip-B doesn't matter, just that we are breaking up a pair.
        So just rename everything. Two pairs and a single on the first floor? AaBbC every time.
    '''
    trans = {}
    alpha_it = iter(alphabet)
    for floor in floors:
        for c in sorted(floor):
            if c not in trans:
                rename = next(alpha_it)
                trans[c.lower()] = rename.lower()
                trans[c.upper()] = rename.upper()

    new_floors = []
    for floor in floors:
        new_floor = []
        for c in floor:
            new_floor.append(trans[c])
        #assert tuple(new_floor) == tuple(sorted(new_floor)), (new_floor)
        new_floors.append(tuple(sorted(new_floor)))
    return new_floors

assert normalize_floors([['Z', 'z']]) == [('A', 'a')], normalize_floors([['Z', 'z']])
assert normalize_floors([['Z', 'z'], ['a', 'b']]) == [('A', 'a'), ('b', 'c')]

def apply_move(state, move_obs, move_dir):
    curr, floors = state
    assert move_dir != 0
    src = list(floors[curr])
    dest = list(floors[curr+move_dir])
    for ob in move_obs:
        src.remove(ob)
        dest.append(ob)

    new_floors = list(floors)
    new_floors[curr] = src
    new_floors[curr+move_dir] = sorted(dest)
    floors = normalize_floors(new_floors)
    return (curr+move_dir, floors)

def winning_state(state):
    if not state[0] and not state[1] and not state[2]:
        print("FTW", state)
        return True
    return False

def freeze_state(curr, floors):
    return (curr, tuple(floors))

def main(floor_num, start_floors):
    # ground floor is 0
    state = (floor_num, start_floors)
    stack = deque([(state, 0)])
    seen = set()  # state-of-the-world that we've alread tried

    print("TOP STIZACK", stack)
    i = 0
    while stack:
        i += 1
        state, count = stack.popleft()
        curr = state[0]
        assert type(state[1][0]) == tuple, state[1]

        for move_obs, move_dir in next_moves(state):
            new_curr, new_floors = apply_move(state, move_obs, move_dir)

            # always check the happy path first.
            # you'll be wrong and waste CPU, but it feels good to try.
            if winning_state(new_floors):
                print("WINZING", new_floors, count+1)
                return

            # skip if moving move_obs results in invalid floors
            if (not valid_floor(set(new_floors[curr]) - set(move_obs)) or
                not valid_floor(set(new_floors[new_curr]) | set(move_obs))):
                seen.add(freeze_state(new_curr, new_floors))
                continue
            
            # skip if we've already added it to the stack
            fstate = freeze_state(new_curr, new_floors)
            if fstate in seen:
                continue
            seen.add(fstate)

            # this is something we want to explore
            stack.append(((new_curr, new_floors), count+1))

        def score(item):
            ''' a good scoring function likes more items towards the goal than the start '''
            (c, f), h = item
            return 4 * len(f[0]) + 3 * len(f[1]) + 2 * len(f[2]) + 1 * len(f[3])
        if i % 100 == 0:
            print(i, len(stack), stack[0][:-1])
            # uncomment to sort by scoring and *really* speed things up
            #stack = deque(sorted(stack, key=score))
    raise Exception("nopefuck")



if __name__ == '__main__':
    floors = normalize_floors(floors)
    main(0, floors)
