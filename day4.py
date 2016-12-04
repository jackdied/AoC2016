'''
--- Day 4: Security Through Obscurity ---

Finally, you come across an information kiosk with a list of rooms. Of course, the list is encrypted and full of decoy data, but the instructions to decode the list are barely hidden nearby. Better remove the decoy data first.

Each room consists of an encrypted name (lowercase letters separated by dashes) followed by a dash, a sector ID, and a checksum in square brackets.

A room is real (not a decoy) if the checksum is the five most common letters in the encrypted name, in order, with ties broken by alphabetization. For example:

aaaaa-bbb-z-y-x-123[abxyz] is a real room because the most common letters are a (5), b (3), and then a tie between x, y, and z, which are listed alphabetically.
a-b-c-d-e-f-g-h-987[abcde] is a real room because although the letters are all tied (1 of each), the first five are listed alphabetically.
not-a-real-room-404[oarel] is a real room.
totally-real-room-200[decoy] is not.
Of the real rooms from the list above, the sum of their sector IDs is 1514.

What is the sum of the sector IDs of the real rooms?

'''

import itertools
import re

my_input = open('day4_input.txt').read().strip()

def split_room_code(line):
    # here's some cargo culting for you, never use '.*' in your re to capture things of unknown length.
    # instead use the index of the smaller thing you want to match or split on.
    code_re = re.compile('(\d+)\[(\w+)\]$')
    m = code_re.search(line)
    assert m, ("bad input", line)
    digits, checksum = m.groups()
    letters = line[:m.start()]  # everything we didn't capture using a '.*'
    return letters, digits, checksum

# test first two lines of input
assert ('gbc-frperg-pubpbyngr-znantrzrag-', '377', 'rgbnp') == \
    split_room_code('gbc-frperg-pubpbyngr-znantrzrag-377[rgbnp]')
assert ('nij-mywlyn-wlsiayhcw-jfumncw-alumm-mbcjjcha-', '422', 'mcjwa') == \
    split_room_code('nij-mywlyn-wlsiayhcw-jfumncw-alumm-mbcjjcha-422[mcjwa]')


def top_5_letters(letters):
    letters = sorted(list(letters.replace('-', '')))
    care_letters = ''
    # the award for worst interface in the stdlib goes to itertools.groupby()
    for k, iter_of_ks in itertools.groupby(letters):
        # ugh. it is never useful to consume the results of itertoos.groupby() directly
        # so instead throw this away and do something with a comprehension of it.
        pass  # fuck me, fuck this trash.
    grouped = [(k, len(list(subiter))) for k, subiter in itertools.groupby(letters)]
    grouped.sort(key=lambda x:x[1], reverse=True)  # most popular first
    return sorted([letter for letter, count in grouped[:5]])

assert list('abc') == top_5_letters('a-b-c')
assert list('abc') == top_5_letters('cba')
assert list('abcde') == top_5_letters('gfeeddccba'), top_5_letters('gfeeddccba')

def main():
    total = 0
    for line in my_input.split('\n'):
        letters, digits, checksum = split_room_code(line)
        want_checksum = ''.join(top_5_letters(letters))
        checksum = ''.join(sorted(checksum))
        if want_checksum == checksum:
            total += int(digits)
    print("Digit total", total)

if __name__ == '__main__':
    main()
