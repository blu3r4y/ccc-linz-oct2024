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
        output.append(r.room_matrix_str())

    return "\n\n".join(map(str, output))


EMPTY = 0


class Room:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.matrix = {}  # self._init_matrix()
        self.ntables = 0  # number of placed tables

    def _init_matrix(self):
        matrix = {}
        for iy in range(self.y):
            for ix in range(self.x):
                matrix[complex(ix, iy)] = 0
        return matrix

    def fill_room(self):
        nr = 1
        for iy in range(self.y):
            for ix in range(self.x):
                if self.place_table(ix, iy, nr):
                    nr += 1
                if self.place_table(ix, iy, nr, vertical=True):
                    nr += 1
        return nr - 1  # number of placed tables

    # def fill_room(self):
    #     table = 1
    #     for iy in range(self.y):
    #         for ix in range(0, self.x, 3):
    #             self.matrix[complex(ix, iy)] = table
    #             self.matrix[complex(ix + 1, iy)] = table
    #             self.matrix[complex(ix + 2, iy)] = table
    #             table += 1
    #     self.ntables = table - 1
    #     return self.matrix

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

        coords = []
        if not vertical:
            if x + length > self.x:
                return False  # table does not fit
            coords = [complex(ix, y) for ix in range(x, x + length)]
        else:
            if y + length > self.y:
                return False  # table does not fit
            coords = [complex(x, iy) for iy in range(y, y + length)]

        if not all(self.matrix.get(xy, EMPTY) == EMPTY for xy in coords):
            return False  # table overlaps with existing tables

        # place table
        for xy in coords:
            self.matrix[xy] = number
        return True

    def room_matrix_str(self) -> str:
        mat = self.room_matrix()
        return "\n".join(" ".join(map(str, line)) for line in mat)

    def room_matrix(self) -> list[list[int]]:
        matrix = []
        for iy in range(self.y):
            line = []
            for ix in range(self.x):
                line.append(self.matrix.get(complex(ix, iy), EMPTY))
            matrix.append(line)
        return matrix
