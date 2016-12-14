import itertools as it
from collections import *
import re

'''
--- Day 12: Leonardo's Monorail ---

You finally reach the top floor of this building: a garden with a slanted glass ceiling. Looks like there are no more stars to be had.

While sitting on a nearby bench amidst some tiger lilies, you manage to decrypt some of the files you extracted from the servers downstairs.

According to these documents, Easter Bunny HQ isn't just this building - it's a collection of buildings in the nearby area. They're all connected by a local monorail, and there's another building not far from here! Unfortunately, being night, the monorail is currently not operating.

You remotely connect to the monorail control systems and discover that the boot sequence expects a password. The password-checking logic (your puzzle input) is easy to extract, but the code it uses is strange: it's assembunny code designed for the new computer you just assembled. You'll have to execute the code and get the password.

The assembunny code you've extracted operates on four registers (a, b, c, and d) that start at 0 and can hold any integer. However, it seems to make use of only a few instructions:

cpy x y copies x (either an integer or the value of a register) into register y.
inc x increases the value of register x by one.
dec x decreases the value of register x by one.
jnz x y jumps to an instruction y away (positive means forward; negative means backward), but only if x is not zero.
The jnz instruction moves relative to itself: an offset of -1 would continue at the previous instruction, while an offset of 2 would skip over the next instruction.

For example:

cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
The above code would set register a to 41, increase its value by 2, decrease its value by 1, and then skip the last dec a (because a is not zero, so the jnz a 2 skips it), leaving register a at 42. When you move past the last instruction, the program halts.

After executing the assembunny code in your puzzle input, what value is left in register a?

'''

class Puter(object):
    def __init__(self, code=[]):
        self.prog = {} # {1: (pfunc, *args)}
        self.curr = 0  # Instruction Pointer
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.cpu_used = 0
        self.load_program(code)
        
    def cpy(self, val_or_reg, dest_reg):
        if val_or_reg in 'abcd':
            src = getattr(self, val_or_reg)
        else:
            src = int(val_or_reg)
        assert dest_reg in 'abcd'
        setattr(self, dest_reg, src)
        self.curr += 1
        
    def inc(self, reg):
        assert reg in 'abcd'
        v = getattr(self, reg)
        setattr(self, reg, v + 1)
        self.curr += 1

    def dec(self, reg):
        assert reg in 'abcd'
        v = getattr(self, reg)
        setattr(self, reg, v - 1)
        self.curr += 1

    def jnz(self, val_or_reg, skip_cnt):
        if val_or_reg in 'abcd':
            v = getattr(self, val_or_reg)
        else:
            v = int(val_or_reg)
        if v:
            self.curr += int(skip_cnt)
        else:
            self.curr += 1

    def run(self):
        while True:
            try:
                self.step()
                if self.cpu_used % 1000000 == 0:
                    print(self)
            except StopIteration as e:
                print("STHAAAAP", e)
                break

    def step(self):
        self.cpu_used += 1
        if self.curr not in self.prog:
            raise StopIteration("program ended")
        func, *args = self.prog[self.curr]
        func(*args)
        #print(self.cpu_used, self.curr, func, *args)
        
    def load_program(self, code):
        curr = 0
        for line in code:
            fname, *args = line.split()
            assert fname in {'cpy', 'inc', 'dec', 'jnz'}
            func = getattr(self, fname)
            self.prog[curr] = (func, *args)
            curr += 1

    def __repr__(self):
        return '<%s:%d reg=%r ic=%d inst=%r>' % (self.__class__.__name__,
                                                 id(self), [self.a, self.b, self.c, self.d],
                                                 self.curr,
                                                 self.prog.get(self.curr, 'OUT OF BOUNDS'))
test_code = '''cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a'''.split('\n')

test = Puter(code=test_code)
test.run()
print("REGA", test.a, test.cpu_used)
            
def main():
    code = open('day12_input.txt').readlines()
    # day 1
    prog = Puter(code=code)
    prog.run()
    return
    # day 2
    prog = Puter(code=code)
    prog.c = 1
    prog.run()
    
    print("DONE!", prog.a, prog.cpu_used)

if __name__ == '__main__':
    main()
