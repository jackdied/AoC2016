'''

'''

import itertools as it

lines = list(open('day6_input.txt'))

from collections import Counter

def main():
    lets = [Counter() for c in range(8)]
    for line in lines:
        for i, c in enumerate(line.strip()):
            lets[i][c] += 1
    final = ''
    for cnt in lets:
        final += cnt.most_common()[-1][0]

    print final
if __name__ == '__main__':
    main()
