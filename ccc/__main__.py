from pathlib import Path
from pprint import pprint

from loguru import logger as log

from .contest import solve
from .utils import infer_current_level, infer_quests_for_level


def load(lines: list[str]) -> dict:
    rooms = []
    for line in lines[1:]:
        x, y, ndesks = map(int, line.split())
        rooms.append((x, y, ndesks))

    return dict(rooms=rooms)


if __name__ == "__main__":
    base_path = Path("data")
    level = infer_current_level(base_path)
    quests = infer_quests_for_level(base_path, level)
    # quests = ["example"]

    for quest in quests:
        input_file = base_path / f"level{level}_{quest}.in"
        output_file = input_file.with_suffix(".out")

        if not input_file.exists():
            log.warning(f"file not found, skip: {input_file}")
            continue

        with open(input_file, "r") as fi:
            data = load(fi.read().splitlines())
            pprint(data)

            print("=== Input {}".format(quest))
            print("======================")

            result = solve(data)
            pprint(result)

            with open(output_file, "w+") as fo:
                fo.write(result)
