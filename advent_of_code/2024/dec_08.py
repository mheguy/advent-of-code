import itertools
from dataclasses import dataclass

from advent_of_code.shared.utils import run_solution

Lines = list[str]


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, other: "Position") -> "Position":
        return Position(self.x + other.x, self.y + other.y)


@dataclass(frozen=True)
class Tower:
    pos: Position
    frequency: str


def main(lines: Lines) -> None:
    results = get_result(lines)
    print(results)


def get_result(lines: Lines) -> int:
    towers = get_towers(lines)
    frequencies = {t.frequency for t in towers}

    antinodes: list[Position] = []
    for frequency in frequencies:
        towers_with_frequency = [t for t in towers if t.frequency == frequency]
        for first, second in itertools.permutations(towers_with_frequency, 2):
            offset = Position(first.pos.x - second.pos.x, first.pos.y - second.pos.y)

            antinodes.append(first.pos + offset)

    # Remove antinodes that are outside of grid
    x_min = 0
    y_min = 0
    x_max = len(lines[0]) - 1
    y_max = len(lines) - 1
    antinodes = [a for a in antinodes if a.x >= x_min and a.x <= x_max and a.y >= y_min and a.y <= y_max]

    return len(set(antinodes))


def get_towers(lines: Lines) -> list[Tower]:
    towers: list[Tower] = []
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char != ".":
                towers.append(Tower(Position(col, row), char))

    return towers


if __name__ == "__main__":
    run_solution("2024", "dec_08", main)
