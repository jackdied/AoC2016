

EMPTY = object()
class Peekable(object):
    def __init__(self, iterator):
        self.it = iterator
        self._peek = EMPTY

    def __iter__(self):
        return self

    def __next__(self):
        v = self.peek
        self._peek = EMPTY
        return v
    next = __next__

    @property
    def peek(self):
        if self._peek == EMPTY:
            self._peek = next(self.it)
        return self._peek


from string import ascii_lowercase as alphabet

p = Peekable(iter(alphabet))
assert p is iter(p)
assert p.peek == 'a'
assert next(p) == 'a'
assert p.peek == 'b'

p = Peekable(iter('a'))
assert p is iter(p)
assert p.peek == 'a'
assert next(p) == 'a'
try:
    next(p)
    raise AssertionError("StopIteration not raised!")
except StopIteration:
    pass

try:
    p.peek
    raise AssertionError("StopIteration not raised!")
except StopIteration:
    pass

p = Peekable(iter([]))
try:
    p.peek
    raise AssertionError("StopIteration not raised!")
except StopIteration:
    pass
try:
    next(p)
    raise AssertionError("StopIteration not raised!")
except StopIteration:
    pass
