import day3
import mock

'''
--- Part Two ---

Now that you've helpfully marked up their design documents, it occurs to you that triangles are specified in groups of three vertically. Each set of three numbers in a column specifies a triangle. Rows are unrelated.

For example, given the following specification, numbers with the same hundreds digit would be part of the same triangle:

101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603
In your puzzle input, and instead reading by columns, how many of the listed triangles are possible?

'''

def main():
    new_triples = []
    cols = zip(*day3.triples)
    for col in cols:
        col = list(col)
        while col:
            trip = (col.pop(0), col.pop(0), col.pop(0))
            new_triples.append(trip)
    with mock.patch.object(day3, 'triples', new_triples):
        day3.main()

if __name__ == '__main__':
    main()
