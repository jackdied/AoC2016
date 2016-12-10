
'''
--- Day 10: Balance Bots ---

You come upon a factory in which many robots are zooming around handing small microchips to each other.

Upon closer examination, you notice that each bot only proceeds when it has two microchips, and once it does, it gives each one to a different bot or puts it in a marked "output" bin. Sometimes, bots take microchips from "input" bins, too.

Inspecting one of the microchips, it seems like they each contain a single number; the bots must use some logic to decide what to do with each chip. You access the local control computer and download the bots' instructions (your puzzle input).

Some of the instructions specify that a specific-valued microchip should be given to a specific bot; the rest of the instructions indicate what a given bot should do with its lower-value or higher-value chip.

For example, consider the following instructions:

value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
Initially, bot 1 starts with a value-3 chip, and bot 2 starts with a value-2 chip and a value-5 chip.
Because bot 2 has two microchips, it gives its lower one (2) to bot 1 and its higher one (5) to bot 0.
Then, bot 1 has two microchips; it puts the value-2 chip in output 1 and gives the value-3 chip to bot 0.
Finally, bot 0 has two microchips; it puts the 3 in output 2 and the 5 in output 0.
In the end, output bin 0 contains a value-5 microchip, output bin 1 contains a value-2 microchip, and output bin 2 contains a value-3 microchip. In this configuration, bot number 2 is responsible for comparing value-5 microchips with value-2 microchips.

Based on your instructions, what is the number of the bot that is responsible for comparing value-61 microchips with value-17 microchips?
'''

my_input = open('day10_input.txt').read()

from collections import defaultdict
import re

def make_bot(low_dest, high_dest):
    def move_bot():
        pass
    return move_bot

def main():
    lines = my_input.split('\n')
    bots = defaultdict(list)  # {bot_number: [chip1, chip2]}
    output_bins = defaultdict(list)  # {bin_number: [chip1, chip2, ..]}
    bot_instructions = {}
    move_re = re.compile('bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)')
    for line in lines:
        m = move_re.match(line)
        if not m:
            continue
        
        bot_from, *args = m.groups()
        bot_from = int(bot_from)
        assert bot_from not in bot_instructions
        def exec_bot(bot_from=bot_from, args=args):
            word_low, num_low, word_high, num_high = args
            num_low, num_high = int(num_low), int(num_high)
            run_next = []
            (low, high) = bots[bot_from]
            if low == 17 and high == 61:
                print("FOND", bot_from, low, high)
            bots[bot_from] = []
            if word_low == 'bot':
                run_next.append((num_low, low))
            else:
                run_next.append((-num_low, low))
            if word_high == 'bot':
                run_next.append((num_high, high))
            else:
                run_next.append((-num_high, high))
            return run_next
        exec_bot.__name__ == 'exec_bot_%d' % bot_from
        bot_instructions[bot_from] = exec_bot

    val_re = re.compile('value (\d+) goes to bot (\d+)')
    give_list = []
    for line in lines:
        m = val_re.match(line)
        if m:
            (val, bot_to) = map(int, m.groups())
            give_list.append((bot_to, val))

    give_list.reverse()
    while give_list:
        bot_to, val = give_list.pop()
        if bot_to < 0:  # actually an ouptut bin
            output_bins[-bot_to].append(val)
            continue
        bots[bot_to].append(val)
        print((bot_to, val), bots[bot_to])
        if len(bots[bot_to]) == 2:
            run_next = bot_instructions[bot_to]()
            give_list.extend(run_next)

if __name__== '__main__':
    main()
    
