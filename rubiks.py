
class Rubiks_Side():
    """ One side of a Rubik's cube """

    def __init__(self, color):
        self._face = []
        for i in range(3):
            self._face.append([color, color, color])

    def __repr__(self):
        return '\n'.join(' '.join(i) for i in self._face)

    def row(self, row):
        return self._face[row]

    def col(self, col):
        return [self._face[0][col], self._face[1][col], self._face[2][col]]


class Rubiks_Cube():
    """ A Rubik's cube """

    def __init__(self):
        self._sides = [Rubiks_Side('r'),
                       Rubiks_Side('o'),
                       Rubiks_Side('g'),
                       Rubiks_Side('b'),
                       Rubiks_Side('w'),
                       Rubiks_Side('y')]

    def rotate(self, side=0, direction='cw'):
        face = side
        # pick the 'face' to rotate if rotating a middle section
        if side >= 6:
            face = (face - 6) * 2

        # ignoring the faces parallel to the rotating section
        ignore = [face, face - 1 if face % 2 else face + 1]
        ignore.sort()
        sides_to_rotate = list(range(6))
        sides_to_rotate = sides_to_rotate[0:ignore[0]] + sides_to_rotate[ignore[1]+1:]
        sides_to_rotate = [[i] for i in sides_to_rotate]

        rows_cols = []
        reverse = []
        # for each of the 3 orthogonal rotations, determine whether we need to reverse
        # a row/column when it is moved, and whether it is a row or a column that should
        # be moved
        if face in (0, 1):
            reverse = [True, False, False, True]
            rows_cols = ['c', 'c', 'r', 'r']
        elif face in (2, 3):
            reverse = [False, True, False, True]
            rows_cols = ['c', 'c', 'c', 'c']
        elif face in (4, 5):
            reverse = [False, False, False, False]
            rows_cols = ['r', 'r', 'r', 'r']

        # determine which row/column is moved
        if side in (0, 3):
            rows_cols = [j + ('0' if i % 2 else '2') for i, j in enumerate(rows_cols)]
        elif side in (1, 2):
            rows_cols = [j + ('2' if i % 2 else '0') for i, j in enumerate(rows_cols)]
        elif side == 4:
            rows_cols = [i + '0' for i in rows_cols]
        elif side == 5:
            rows_cols = [i + '2' for i in rows_cols]
        elif side in (6, 7, 8):
            rows_cols = [i + '1' for i in rows_cols]

        sides_to_rotate = list(zip(sides_to_rotate, rows_cols, reverse))


a = Rubiks_Cube()
a.rotate()
a.rotate(1)
