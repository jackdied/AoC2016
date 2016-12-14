from collections import *
import itertools as it
import re
from hashlib import md5
'''
It contains three of the same character in a row, like 777. Only consider the first such triplet in a hash.
One of the next 1000 hashes in the stream contains that same character five times in a row, like 77777.
'''

my_input = 'zpqevtbw'

'''
So, using our example salt of abc, index 22728 produces the 64th key.
'''

def gensums(i=0, seed=my_input, count=100000):
    while count:
        blob = md5((seed + str(i)).encode('utf8')).hexdigest()
        yield i, blob
        i += 1
        count -= 1

def superhash(blob, repeat=2016,_cache={}):
    for _ in range(repeat):
        origblob = blob
        blob = _cache.get(blob, None)
        if blob is None:
            blob = md5(origblob.encode('utf8')).hexdigest()
            _cache[origblob] = blob
    return blob

assert superhash('577571be4de9dcce85a041ba0410f29f') == 'a107ff634856bb300138cac6568c0f24'


#def superhash(blob): return blob  # Part 1, comment line for Part 2

def main(seed=my_input, want=64):
    que = deque([], 1000)
    sums = gensums(0, seed)
    def newhash():
        i, blob = next(sums)
        return i, superhash(blob)
    while len(que) != 1000:
        que.append(newhash())
    while want:
        i, examine = que.popleft()
        que.append(newhash())
        m = re.search(r'([abcdef0123456789])\1\1', examine)
        if not m:
            continue
        letter = m.group(1)
        fiver = letter * 5
        for _, v in que:
            if fiver in v:
                want -= 1
                print("FOUND", i, want)

        
def _main():
    keys = list(it.islice(eatmatching(0, my_input), 150))
    for i, (beg, match) in enumerate(sorted(keys)[:70]):
        print(i, (beg, match))
    return

if __name__ == '__main__':
    main()
