
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

def parse_bot_lines(lines):
    move_re = re.compile('bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)')
    for line in lines:
        m = move_re.match(line)
        if not m:
            continue

        bot_from, word_low, num_low, word_high, num_high = m.groups()
        bot_from = int(bot_from)
        num_low, num_high = int(num_low), int(num_high)
        # a little hacky, if the destination is an output make it negative
        # (minus one more because there is both output zero and bot zero)
        if word_low == 'output':
            num_low = -num_low - 1
        if word_high == 'output':
            num_high = -num_high - 1
        yield (bot_from, num_low, num_high)
    return

def parse_value_lines(lines):
    val_re = re.compile('value (\d+) goes to bot (\d+)')
    for line in lines:
        m = val_re.match(line)
        if m:
            (val, bot_to) = map(int, m.groups())
            yield (bot_to, val)
    return

def main():
    lines = my_input.split('\n')
    output_bins = defaultdict(list)  # {bin_number: [chip1, chip2, ..]}
    bot_holding = defaultdict(list)  # {bot_number: [chip1, chip2]}
    bot_destination = {}  # {bot_number: (dest_num_low, dest_num_high)}

    value_lines = [line for line in lines if line.startswith('value')]
    bot_lines = [line for line in lines if line.startswith('bot')]

    for bot_num, low_dest, high_dest in parse_bot_lines(bot_lines):
        bot_destination[bot_num] = (low_dest, high_dest)

    # execute a list of instructions that puts one value into one bot/output
    give_list = list(parse_value_lines(lines))  # [(destination, chip_value), ..]
    give_list.reverse()
    while give_list:
        bot_to, val = give_list.pop()
        if bot_to < 0:  # actually an ouptut bin
            output_bins[-bot_to-1].append(val)
            continue
        bot_holding[bot_to].append(val)
        assert len(bot_holding[bot_to]) < 3, "the problem is underspecified"

        print((bot_to, val), bot_holding[bot_to])
        if len(bot_holding[bot_to]) == 2:  # full, triggers a give away
            low_val, high_val = sorted(bot_holding[bot_to])
            if low_val == 17 and high_val == 61:
                print("FOUND", bot_to, low_val, high_val)
            bot_holding[bot_to] = []
            low_dest, high_dest = bot_destination[bot_to]
            give_list.append((high_dest, high_val))
            give_list.append((low_dest, low_val))

    for output_num in [0, 1, 2]:
        print("Outputs in %d, %r" % (output_num, output_bins[output_num]))
            
if __name__== '__main__':
    main()
    
