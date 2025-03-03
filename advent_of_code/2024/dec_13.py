import itertools
import re

from advent_of_code.shared.utils import Position, run_solution

Lines = list[str]

A_PUSH_COST = 3
B_PUSH_COST = 1

button_extract_pattern = re.compile(r"(?:Button [AB]|Prize): X[+=](\d+), Y[+=](\d+)")


def main(lines: Lines) -> None:
    machines = get_machines(lines)

    result_1 = 0
    result_2 = 0
    for machine in machines:
        result_1 += process_machine(machine)
        result_2 += process_machine(machine, 10000000000000)

    print(result_1, result_2)


def get_machines(lines: Lines) -> list[tuple[Position, Position, Position]]:
    machines: list[tuple[Position, Position, Position]] = []
    for group in itertools.batched(lines, 4):
        button_a = extract_position(group[0])
        button_b = extract_position(group[1])

        prize_location = extract_position(group[2])

        machines.append((button_a, button_b, prize_location))

    return machines


def process_machine(machine: tuple[Position, Position, Position], prize_location_offset: int = 0) -> int:
    button_a, button_b, prize_location = machine
    prize_location = Position(prize_location.x + prize_location_offset, prize_location.y + prize_location_offset)

    det = button_a.x * button_b.y - button_a.y * button_b.x

    if det == 0:
        return 0

    a_numerator = prize_location.x * button_b.y - prize_location.y * button_b.x
    b_numerator = button_a.x * prize_location.y - button_a.y * prize_location.x

    if a_numerator % det != 0 or b_numerator % det != 0:
        return 0

    a_pushes = a_numerator // det
    b_pushes = b_numerator // det

    if a_pushes < 0 or b_pushes < 0:
        return 0

    if (
        button_a.x * a_pushes + button_b.x * b_pushes == prize_location.x
        and button_a.y * a_pushes + button_b.y * b_pushes == prize_location.y
    ):
        return (a_pushes * A_PUSH_COST) + (b_pushes * B_PUSH_COST)

    return 0


def extract_position(text: str) -> Position:
    if match := button_extract_pattern.match(text):
        return Position(int(match.group(1)), int(match.group(2)))

    raise ValueError(f"Unable to extract from {text}")


if __name__ == "__main__":
    run_solution("2024", "dec_13", main)
