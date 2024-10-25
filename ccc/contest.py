from collections import namedtuple
from typing import Iterable

EMPTY = 0
TABLE = 1
EMPTY_CHAR = "."
TABLE_CHAR = "X"


def solve(data: dict) -> str:
    output = []
    for x, y, ndesks in data["rooms"]:
        r = Room(x, y)
        nplaced = r.fill_room(ndesks)
        if nplaced != ndesks:
            print(f"should have placed {ndesks} desks, but placed {nplaced}")
        output.append(r.room_matrix_str(True))

    return "\n\n".join(map(str, output))


State = namedtuple("State", ["matrix", "pos"])


class Room:
    def __init__(self, x: int, y: int, length: int = 2):
        self.x = x
        self.y = y
        self.length = length
        self.matrix: dict[complex, int] = {}

    def fill_room(self, num_tables: int):
        target_score = self.x * self.y - self.length * num_tables
        return self._fill_room(target_score)

    def _fill_room(self, target_score: int):
        start = State(self.matrix, complex(0, 0))
        states = [start]

        best_score = self.num_free_spaces(start.matrix)
        best_state = start

        print(f"({target_score})", end=" ", flush=True)

        i = 0
        while states and i < 100_000:
            state = states.pop()
            if self.is_terminal(state):
                score = self.num_free_spaces(state.matrix)
                if score < best_score:
                    best_score = score
                    best_state = state
                    print(best_score, end=" - ", flush=True)
                if best_score == target_score:
                    print("done.")
                    break
            states.extend(self.successors(state))
            i += 1

        self.matrix = best_state.matrix
        return self.num_tables(best_state.matrix)

    def is_terminal(self, state: State) -> bool:
        return state.pos is None or state.pos == complex(self.x - 1, self.y - 1)

    def successors(self, state: State) -> Iterable[State]:
        matrix, pos = state

        # advance the position
        npos = self.advance_position(pos)
        if npos is None:
            return None

        # place table
        if (mat := self.place_table(matrix, pos)) is not None:
            yield State(mat, npos)
        if (mat := self.place_table(matrix, pos, vertical=True)) is not None:
            yield State(mat, npos)

        # place no table
        yield State(matrix, npos)

    def advance_position(self, pos: complex) -> complex:
        npos = complex(int(pos.real) + 1, int(pos.imag))
        if npos.real >= self.x:
            npos = complex(0, pos.imag + 1)
        if npos.imag >= self.y:
            return None
        return npos

    def num_free_spaces(self, matrix: dict[complex, int]) -> int:
        space = self.x * self.y
        nplaced = sum(1 for nr in matrix.values() if nr == TABLE)
        return space - nplaced

    def num_tables(self, matrix: dict[complex, int]) -> int:
        # assumes that tables are placed correctly
        nplaced = sum(1 for nr in matrix.values() if nr == TABLE)
        return nplaced // self.length

    def place_table(
        self,
        matrix: dict[complex, int],
        xy: complex,
        vertical: bool = False,
    ) -> dict[complex, int] | None:
        x, y = int(xy.real), int(xy.imag)
        if not (0 <= x < self.x and 0 <= y < self.y):
            return None  # start position out of bounds

        coords = set()
        if not vertical:
            if x + self.length > self.x:
                return None  # table would overflow
            coords = {complex(ix, y) for ix in range(x, x + self.length)}
        else:
            if y + self.length > self.y:
                return None  # table would overflow
            coords = {complex(x, iy) for iy in range(y, y + self.length)}

        if not all(matrix.get(xy, EMPTY) == EMPTY for xy in coords):
            return None  # table overlaps with existing tables

        outline = set()
        if not vertical:
            outline |= {complex(ix, y - 1) for ix in range(x - 1, x + self.length + 1)}
            outline |= {complex(x - 1, y), complex(x + self.length, y)}
            outline |= {complex(ix, y + 1) for ix in range(x - 1, x + self.length + 1)}
        else:
            outline |= {complex(x - 1, iy) for iy in range(y - 1, y + self.length + 1)}
            outline |= {complex(x, y - 1), complex(x, y + self.length)}
            outline |= {complex(x + 1, iy) for iy in range(y - 1, y + self.length + 1)}

        if any(matrix.get(xy, EMPTY) != EMPTY for xy in outline):
            return None  # table would touch another table

        # place table on copy of matrix
        matrix = dict(matrix)
        for xy in coords:
            matrix[xy] = TABLE
        return matrix

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
