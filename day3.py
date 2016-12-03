'''

--- Day 3: Squares With Three Sides ---

Now that you can think clearly, you move deeper into the labyrinth of hallways and office furniture that makes up this part of Easter Bunny HQ. This must be a graphic design department; the walls are covered in specifications for triangles.

Or are they?

The design document gives the side lengths of each triangle it describes, but... 5 10 25? Some of these aren't triangles. You can't help but mark the impossible ones.

In a valid triangle, the sum of any two sides must be larger than the remaining side. For example, the "triangle" given above is impossible, because 5 + 10 is not larger than 25.

In your puzzle input, how many of the listed triangles are possible?

'''


def valid_triangle(sides):
    sides = sorted(sides)
    side1, side2, side3 = sides
    return side1 + side2 > side3

assert True == valid_triangle([3, 4, 5])  # pythagorizzle
assert False == valid_triangle([1, 1, 3])

my_input = open('day3_input.txt').read()  # very wordy, keep it in a file
lines = my_input.split('\n')
triples = [map(int, line.split()) for line in lines if line]

def main():
    print(sum(valid_triangle(triple) for triple in triples))

if __name__ == '__main__':
    main()
