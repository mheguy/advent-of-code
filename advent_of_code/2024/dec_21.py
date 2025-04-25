from collections import deque

from advent_of_code.shared.utils import Direction, Position, run_solution

Lines = list[str]


NUMERIC_KEYPAD = {
    "7": Position(0, 0),
    "8": Position(1, 0),
    "9": Position(2, 0),
    "4": Position(0, 1),
    "5": Position(1, 1),
    "6": Position(2, 1),
    "1": Position(0, 2),
    "2": Position(1, 2),
    "3": Position(2, 2),
    "0": Position(1, 3),
    "A": Position(2, 3),
}
NUMERIC_POSITIONS = {v: k for k, v in NUMERIC_KEYPAD.items()}

DIRECTIONAL_KEYPAD = {
    "^": Position(1, 0),
    "A": Position(2, 0),
    "<": Position(0, 1),
    "v": Position(1, 1),
    ">": Position(2, 1),
}
DIRECTIONAL_POSITIONS = {v: k for k, v in DIRECTIONAL_KEYPAD.items()}

MOVEMENTS = {"<": Direction.LEFT, ">": Direction.RIGHT, "^": Direction.UP, "v": Direction.DOWN}


def step(key: dict[Position, str], pos: Position, command: str) -> tuple[Position | None, str | None]:
    if command in MOVEMENTS:
        new_position = pos + MOVEMENTS[command]

        if new_position not in key:
            return (None, None)

        return new_position, None

    return pos, key[pos]


def bfs_min_length(code: str) -> int:  # noqa: C901, PLR0912
    start = (DIRECTIONAL_KEYPAD["A"], DIRECTIONAL_KEYPAD["A"], NUMERIC_KEYPAD["A"], 0)
    dq = deque()
    dq.append((start, 0))
    seen = {start}

    while dq:
        (position_keypad_1, position_keypad_2, position_keypad_3, k), dist = dq.popleft()

        if k == len(code):
            return dist

        for cmd in ["<", ">", "^", "v", "A"]:
            # Keypad 1
            new_pos_1, output_1 = step(DIRECTIONAL_POSITIONS, position_keypad_1, cmd)

            if new_pos_1 is None:
                continue

            if output_1 is None:
                newstate = (new_pos_1, position_keypad_2, position_keypad_3, k)
                if newstate not in seen:
                    seen.add(newstate)
                    dq.append((newstate, dist + 1))
                continue

            # Keypad 2
            new_pos_2, output_2 = step(DIRECTIONAL_POSITIONS, position_keypad_2, output_1)

            if new_pos_2 is None:
                continue

            if output_2 is None:
                newstate = (new_pos_1, new_pos_2, position_keypad_3, k)
                if newstate not in seen:
                    seen.add(newstate)
                    dq.append((newstate, dist + 1))

                continue

            # Keypad 3
            new_pos_3, output_3 = step(NUMERIC_POSITIONS, position_keypad_3, output_2)

            if new_pos_3 is None:
                continue

            if output_3 is None:
                newstate = (new_pos_1, new_pos_2, new_pos_3, k)
                if newstate not in seen:
                    seen.add(newstate)
                    dq.append((newstate, dist + 1))

            elif output_3 == code[k]:
                newstate = (new_pos_1, new_pos_2, new_pos_3, k + 1)
                if newstate not in seen:
                    seen.add(newstate)
                    dq.append((newstate, dist + 1))
            else:
                # else mismatch → throw away
                pass

    raise RuntimeError("No solution found!")


def main(lines: Lines) -> None:
    result = 0
    for line in lines:
        steps_taken = bfs_min_length(line)
        numeric_part_of_code = int("".join([x for x in line if x.isdigit()]))
        result += steps_taken * numeric_part_of_code

    print(result)


if __name__ == "__main__":
    run_solution("2024", "dec_21", main)
