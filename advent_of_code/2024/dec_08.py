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

    def __mul__(self, other: int) -> "Position":
        return Position(self.x * other, self.y * other)


@dataclass(frozen=True)
class Tower:
    pos: Position
    frequency: str


class Grid:
    def __init__(self, lines: Lines):
        self.x_min = 0
        self.y_min = 0
        self.x_max = len(lines[0]) - 1
        self.y_max = len(lines) - 1
        self.largest_axis = max(self.x_max, self.y_max)

    def __contains__(self, pos: Position) -> bool:
        return pos.x >= self.x_min and pos.x <= self.x_max and pos.y >= self.y_min and pos.y <= self.y_max


def main(lines: Lines) -> None:
    print(get_result(lines))


def get_result(lines: Lines) -> tuple[int, int]:
    grid = Grid(lines)
    towers = get_towers(lines)
    frequencies = {t.frequency for t in towers}

    p1_antinodes: list[Position] = []
    p2_antinodes: list[Position] = []
    for frequency in frequencies:
        towers_with_frequency = [t for t in towers if t.frequency == frequency]
        for first, second in itertools.permutations(towers_with_frequency, 2):
            p2_antinodes.extend([first.pos, second.pos])
            offset = Position(first.pos.x - second.pos.x, first.pos.y - second.pos.y)

            antinode = first.pos + offset

            if antinode not in grid:
                continue

            p1_antinodes.append(antinode)

            counter = 1
            while antinode in grid:
                p2_antinodes.append(antinode)

                counter += 1
                antinode = first.pos + offset * counter

    return len(set(p1_antinodes)), len(set(p2_antinodes))


def get_towers(lines: Lines) -> list[Tower]:
    towers: list[Tower] = []
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char != ".":
                towers.append(Tower(Position(col, row), char))

    return towers


if __name__ == "__main__":
    run_solution("2024", "dec_08", main)
