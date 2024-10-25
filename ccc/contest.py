Room = dict[complex, int]


def solve(data: dict) -> str:
    rooms = data["rooms"]

    output = []
    for x, y, ndesks in rooms:
        r = Room(x, y)
        nplaced = r.fill_room()
        assert (
            nplaced == ndesks
        ), f"should have placed {ndesks} desks, but placed {nplaced}"
        output.append(r.room_matrix_str(True))

    return "\n\n".join(map(str, output))


EMPTY = 0
EMPTY_CHAR = "."
TABLE_CHAR = "X"


class Room:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.matrix: dict[complex, int] = {}  # self._init_matrix()
        self.ntables = 0  # number of placed tables

    def fill_room(self):
        nr = 1
        for iy in range(self.y):
            for ix in range(self.x):
                if self.place_table(ix, iy, nr):
                    nr += 1
                if self.place_table(ix, iy, nr, vertical=True):
                    nr += 1
        return nr - 1  # number of placed tables

    def place_table(
        self,
        x: int,
        y: int,
        number: int,
        vertical: bool = False,
        length: int = 3,
    ) -> bool:
        if not (0 <= x < self.x and 0 <= y < self.y):
            return False  # start position out of bounds

        coords = set()
        if not vertical:
            if x + length > self.x:
                return False  # table would overflow
            coords = {complex(ix, y) for ix in range(x, x + length)}
        else:
            if y + length > self.y:
                return False  # table would overflow
            coords = {complex(x, iy) for iy in range(y, y + length)}

        if not all(self.matrix.get(xy, EMPTY) == EMPTY for xy in coords):
            return False  # table overlaps with existing tables

        outline = set()
        if not vertical:
            outline |= {complex(ix, y - 1) for ix in range(x - 1, x + length + 1)}
            outline |= {complex(x - 1, y), complex(x + length, y)}
            outline |= {complex(ix, y + 1) for ix in range(x - 1, x + length + 1)}
            outline -= coords
        else:
            outline |= {complex(x - 1, iy) for iy in range(y - 1, y + length + 1)}
            outline |= {complex(x, y - 1), complex(x, y + length)}
            outline |= {complex(x + 1, iy) for iy in range(y - 1, y + length + 1)}
            outline -= coords

        if not all(self.matrix.get(xy, EMPTY) == EMPTY for xy in outline):
            return False  # table would touch another table

        # place table
        for xy in coords:
            self.matrix[xy] = number
        return True

    def room_matrix_str(self, anonymize: bool = False) -> str:
        mat = self.room_matrix(anonymize=anonymize)
        space = " " if not anonymize else ""
        return "\n".join(space.join(map(str, line)) for line in mat)

    def room_matrix(self, anonymize: bool = False) -> list[list[int | str]]:
        matrix = self.anonymized_matrix() if anonymize else self.matrix
        default = EMPTY_CHAR if anonymize else EMPTY
        result = []

        for iy in range(self.y):
            line = []
            for ix in range(self.x):
                line.append(matrix.get(complex(ix, iy), default))
            result.append(line)
        return result

    def anonymized_matrix(self) -> dict[complex, str]:
        result = {}
        for xy, nr in self.matrix.items():
            result[xy] = EMPTY_CHAR if nr == EMPTY else TABLE_CHAR
        return result
