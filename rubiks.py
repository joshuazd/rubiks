
class Rubiks_Side():
    """ One side of a Rubik's cube """

    def __init__(self, color):
        self._face = []
        for i in range(3):
            self._face.append([color, color, color])

    def __repr__(self):
        return '\n'.join(' '.join(i) for i in self._face)

    def rotate(self):
        # self._face = rotate(rotate(rotate(self._face)))
        self._face = [list(i) for i in rotate(rotate(rotate(self._face)))]

    def get_row(self, rowNum):
        return self._face[rowNum]

    def set_row(self, rowNum, row):
        self._face[rowNum] = row

    def get_col(self, colNum):
        return [self._face[0][colNum], self._face[1][colNum], self._face[2][colNum]]

    def set_col(self, colNum, col):
        for i in range(len(col)):
            self._face[i][colNum] = col[i]


def rotate(l):
    return list(zip(*l))[::-1]


class Rubiks_Cube():
    """ A Rubik's cube """

    def __init__(self):
        self._sides = [Rubiks_Side('r'),
                       Rubiks_Side('o'),
                       Rubiks_Side('g'),
                       Rubiks_Side('b'),
                       Rubiks_Side('w'),
                       Rubiks_Side('y')]

    def __repr__(self):
        def split_repr(side):
            return side.__repr__().split('\n')
        repr = []
        blank = split_repr(Rubiks_Side(' '))
        red = split_repr(self._sides[0])
        # orange = split_repr(self._sides[1])[::-1]
        orange = [' '.join(i) for i in rotate(rotate(self._sides[1]._face))]
        green = [' '.join(i) for i in rotate(rotate(rotate(self._sides[2]._face)))]
        blue = [' '.join(i) for i in rotate(self._sides[3]._face)]
        white = split_repr(self._sides[4])
        yellow = [' '.join(i[::-1]) for i in self._sides[5]._face]
        repr.extend([blank[i] + ' ' + yellow[i] for i in range(len(blank))])
        repr.extend([blank[i] + ' ' + orange[i] for i in range(len(blank))])
        repr.extend([green[i] + ' ' + white[i] + ' ' + blue[i] for i in range(len(green))])
        repr.extend([blank[i] + ' ' + red[i] for i in range(len(blank))])

        return '\n'.join(repr)

    def rotate(self, side=0, direction='cw'):
        def move_slice(source_slice, dest):
            d_side = self._sides[dest['side']]
            temp = []

            if dest['slice'][0] is 'r':
                temp = d_side.get_row(int(dest['slice'][1]))[::dest['reverse']]
                d_side.set_row(int(dest['slice'][1]), source_slice)
            else:
                temp = d_side.get_col(int(dest['slice'][1]))[::dest['reverse']]
                d_side.set_col(int(dest['slice'][1]), source_slice)

            return temp

        face = side
        # pick the 'face' to rotate if rotating a middle section
        if side >= 6:
            face = (face - 6) * 2

        # ignoring the faces parallel to the rotating section
        ignore = [face, face - 1 if face % 2 else face + 1]
        ignore.sort()
        sides_to_rotate = list(range(6))
        sides_to_rotate = sides_to_rotate[0:ignore[0]] + sides_to_rotate[ignore[1]+1:]
        sides_to_rotate = [{'side': i} for i in sides_to_rotate]

        rows_cols = []
        reverse = []
        # for each of the 3 orthogonal rotations, determine whether we need to reverse
        # a row/column when it is moved, and whether it is a row or a column that should
        # be moved
        if face in (0, 1):
            reverse = [-1, 1, 1, -1]
            rows_cols = ['c', 'c', 'r', 'r']
        elif face in (2, 3):
            reverse = [1, -1, -1, 1]
            rows_cols = ['c', 'c', 'c', 'c']
        elif face in (4, 5):
            reverse = [1, 1, 1, 1]
            rows_cols = ['r', 'r', 'r', 'r']

        reverse = [{'reverse': i} for i in reverse]

        # determine which row/column is moved
        if side in (0, 3):
            rows_cols = [{'slice': j + ('0' if i % 2 else '2')} for i, j in enumerate(rows_cols)]
        elif side in (1, 2):
            rows_cols = [{'slice': j + ('2' if i % 2 else '0')} for i, j in enumerate(rows_cols)]
        elif side == 4:
            rows_cols = [{'slice': i + '0'} for i in rows_cols]
        elif side == 5:
            rows_cols = [{'slice': i + '2'} for i in rows_cols]
        elif side in (6, 7, 8):
            rows_cols = [{'slice': i + '1'} for i in rows_cols]

        sides_to_rotate = list(zip(sides_to_rotate, rows_cols, reverse))
        for index, i in enumerate(sides_to_rotate):
            sides_to_rotate[index] = {key: item for j in i for key, item in j.items()}

        source = sides_to_rotate[0]
        s_side = self._sides[source['side']]
        if source['slice'][0] is 'r':
            temp = s_side.get_row(int(source['slice'][1]))[::source['reverse']]
        else:
            temp = s_side.get_col(int(source['slice'][1]))[::source['reverse']]

        temp = move_slice(temp, sides_to_rotate[2])
        temp = move_slice(temp, sides_to_rotate[1])
        temp = move_slice(temp, sides_to_rotate[3])
        move_slice(temp, sides_to_rotate[0])

        if side < 6:
            self._sides[side].rotate()


a = Rubiks_Cube()
print(a)
print()
a.rotate(4)
print(a)
print()
a.rotate(0)
print(a)
print()
a.rotate(3)
print(a)
