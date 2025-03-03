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
    for machine in machines:
        result_1 += process_machine(machine)

    print(result_1)


def get_machines(lines: Lines) -> list[tuple[Position, Position, Position]]:
    machines: list[tuple[Position, Position, Position]] = []
    for group in itertools.batched(lines, 4):
        button_a = extract_position(group[0])
        button_b = extract_position(group[1])

        prize_location = extract_position(group[2])

        machines.append((button_a, button_b, prize_location))

    return machines


def process_machine(machine: tuple[Position, Position, Position]) -> int:
    button_a, button_b, prize_location = machine

    # Let's work on X
    max_number_of_a_pushes = prize_location.x // button_a.x

    successful_x_combinations: list[tuple[int, int]] = []
    for a_pushes in range(max_number_of_a_pushes, 0, -1):
        remainder = prize_location.x - (a_pushes * button_a.x)

        if remainder % button_b.x == 0:
            successful_x_combinations.append((a_pushes, remainder // button_b.x))

    if not successful_x_combinations:
        return 0

    # For Y, we could do the same thing and then check the sets of successful combinations for intersection
    # But it's probably faster to simply check each successful x combination to see if it works
    for successful_x_combination in successful_x_combinations:
        a_pushes, b_pushes = successful_x_combination
        total_y = (a_pushes * button_a.y) + (b_pushes * button_b.y)

        if total_y == prize_location.y:
            return (a_pushes * A_PUSH_COST) + (b_pushes * B_PUSH_COST)

    return 0


def extract_position(text: str) -> Position:
    if match := button_extract_pattern.match(text):
        return Position(int(match.group(1)), int(match.group(2)))

    raise ValueError(f"Unable to extract from {text}")


if __name__ == "__main__":
    run_solution("2024", "dec_13", main)
