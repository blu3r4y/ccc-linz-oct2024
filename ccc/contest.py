def solve(data: dict) -> str:
    rooms = data["rooms"]

    ndesks = []

    for x, y in rooms:
        ndesks.append((x // 3) * y)

    return "\n".join(map(str, ndesks))
