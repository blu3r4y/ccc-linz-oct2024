Room = dict[complex, int]


def solve(data: dict) -> str:
    rooms = data["rooms"]

    output = []

    for x, y, _ in rooms:
        r = Room(x, y)
        r.fill_room_with_tables()
        output.append(r.print_room())

    return "\n\n".join(map(str, output))


class Room:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.matrix = self._init_matrix()

    def _init_matrix(self):
        matrix = {}
        for iy in range(self.y):
            for ix in range(self.x):
                matrix[complex(ix, iy)] = 0
        return matrix

    def fill_room_with_tables(self):
        table = 1
        for iy in range(self.y):
            for ix in range(0, self.x, 3):
                self.matrix[complex(ix, iy)] = table
                self.matrix[complex(ix + 1, iy)] = table
                self.matrix[complex(ix + 2, iy)] = table
                table += 1
        return self.matrix

    def print_room(self) -> str:
        lines = []
        for iy in range(self.y):
            line = []
            for ix in range(self.x):
                line.append(self.matrix[complex(ix, iy)])
            lines.append(" ".join(map(str, line)))
        return "\n".join(lines)
