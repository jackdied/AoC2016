import day2
import mock

'''
--- Part Two ---

You finally arrive at the bathroom (it's a several minute walk from the lobby so visitors can behold the many fancy conference rooms and water coolers on this floor) and go to punch in the code. Much to your bladder's dismay, the keypad is not at all like you imagined it. Instead, you are confronted with the result of hundreds of man-hours of bathroom-keypad-design meetings:

    1
  2 3 4
5 6 7 8 9
  A B C
    D
You still start at "5" and stop when you're at an edge, but given the same instructions as above, the outcome is very different:

You start at "5" and don't move at all (up and left are both edges), ending at 5.
Continuing from "5", you move right twice and down three times (through "6", "7", "B", "D", "D"), ending at D.
Then, from "D", you move five more times (through "D", "B", "C", "C", "B"), ending at B.
Finally, after five more moves, you end at 3.
So, given the actual keypad layout, the code would be 5DB3.

Using the same instructions in your puzzle input, what is the correct bathroom code?
'''

_new_buttons = [['', '', '1'],
                ['', '2', '3', '4'],
                ['5', '6', '7', '8', '9'],
                ['', 'A', 'B', 'C'],
                ['', '', 'D']]
new_buttons = {}
for _y, _row in enumerate(_new_buttons):
    for _x, _val in enumerate(_row):
        if _val:
            new_buttons[(_x, _y)] = _val

assert '1' == new_buttons[(2, 0)]
assert '5' == new_buttons[(0, 2)]

def main():
    # don't be a jerk, only replace the button layout temporarily
    with mock.patch.object(day2, 'buttons', new_buttons):
        day2.main()

if __name__ == '__main__':
    main()
