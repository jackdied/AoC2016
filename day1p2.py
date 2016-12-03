import day1

'''
--- Part Two ---

Then, you notice the instructions continue on the back of the Recruiting Document. Easter Bunny HQ is actually at the first location you visit twice.

For example, if your instructions are R8, R4, R4, R8, the first location you visit twice is 4 blocks away, due East.

How many blocks away is the first location you visit twice?
'''

def expand_instructions(instructions):
    step_by_step = []
    for instr in instructions:
        do_turn, do_steps = instr[0], int(instr[1:])
        step_by_step.append(do_turn+'1')
        step_by_step.extend(['X1'] * (do_steps-1))
    return step_by_step

assert ['R1', 'X1'] == expand_instructions(['R2'])

def main():
    instructions = [instr.strip() for instr in day1.my_input.split(',')]
    instructions = expand_instructions(instructions)

    here = ((0, 0), 'N')
    visited = set([here[0]])
    for instr in instructions:
        here = day1.move(here, instr)
        assert here[0] not in visited, here[0]
        visited.add(here[0])

if __name__ == '__main__':
    main()

