import day4

'''
--- Part Two ---

With all the decoy data out of the way, it's time to decrypt this list and get moving.

The room names are encrypted by a state-of-the-art shift cipher, which is nearly unbreakable without the right software. However, the information kiosk designers at Easter Bunny HQ were not expecting to deal with a master cryptographer like yourself.

To decrypt a room name, rotate each letter forward through the alphabet a number of times equal to the room's sector ID. A becomes B, B becomes C, Z becomes A, and so on. Dashes become spaces.

For example, the real name for qzmt-zixmtkozy-ivhz-343 is very encrypted name.

What is the sector ID of the room where North Pole objects are stored?

'''

from string import ascii_lowercase as alphabet

def rot1(letter):
    ''' rotate 1 letter 1 position '''
    ind = (alphabet.index(letter) + 1) % len(alphabet)
    return alphabet[ind]

assert 'b' == rot1('a')
assert 'a' == rot1('z')

def rotN(letter, n=1):
    if letter not in alphabet:  # hackish, is a space
        assert letter == '-', "bad assumptions make you a bad person"
        return letter
    for _ in range(n):
        letter = rot1(letter)
    return letter

assert 'c' == rotN('a', 2)
assert 'b' == rotN('z', 2)


def main():
    total = 0
    for line in day4.my_input.split('\n'):
        letters, digits, checksum = day4.split_room_code(line)
        want_checksum = ''.join(day4.top_5_letters(letters))
        checksum = ''.join(sorted(checksum))
        if want_checksum != checksum:
            # the question implies the right answer will have a valid checksum?
            continue
        
        rot_count = int(digits)
        plain_text = ''.join(rotN(letter, rot_count) for letter in letters)
        print(plain_text, digits)


# calling rot1 rotN times is super expensive -- decoding the input takes 7 seconds.
# so let's do it smarterly
def rotN(letter, n=1):
    if letter not in alphabet:  # hackish, as above
        return letter
    ind = (alphabet.index(letter) + n) % len(alphabet)
    return alphabet[ind]


if __name__ == '__main__':
    main()
