import importlib.resources as pkg_resources
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING

import advent_of_code

if TYPE_CHECKING:
    from collections.abc import Callable

INPUT_FOLDER = "input"


@dataclass(frozen=True, slots=True)
class Position:
    x: int
    y: int

    def __str__(self) -> str:
        return f"{self.x}, {self.y}"

    def __add__(self, other: "Position | Direction | DirectionInfo") -> "Position":
        match other:
            case Direction():
                other = other.value.as_position
            case DirectionInfo():
                other = other.as_position
            case _:
                pass

        return Position(self.x + other.x, self.y + other.y)

    def __mul__(self, other: int) -> "Position":
        return Position(self.x * other, self.y * other)


@dataclass(frozen=True, slots=True)
class DirectionInfo:
    as_position: Position
    axis: str


class Direction(Enum):
    UP = DirectionInfo(Position(0, -1), "y")
    RIGHT = DirectionInfo(Position(1, 0), "x")
    DOWN = DirectionInfo(Position(0, 1), "y")
    LEFT = DirectionInfo(Position(-1, 0), "x")


def run_solution(year: str, date: str, func: "Callable[[list[str]], None]") -> None:
    filename = f"{date}.txt"
    partial_path = f"input/{year}/"

    print("Running sample...")

    try:
        sample_data = get_input_file_lines(f"{partial_path}/sample/{filename}")
    except FileNotFoundError:
        print(f"ERROR: No sample file found for year ({year}) and date ({date}). Exiting.")
        sys.exit(1)

    if not sample_data:
        print("ERROR: Sample data is empty. Check the file. Exiting.")
        sys.exit(1)

    func(sample_data)

    print("Sample completed.")
    print("Running real...")

    try:
        real_data = get_input_file_lines(f"{partial_path}/real/{filename}")
    except FileNotFoundError:
        print("ERROR: File with real data missing. Create the missing file with the data.")

        init_file = advent_of_code.__file__
        package_path = Path(init_file).parent
        full_path = package_path / f"{partial_path}/real/{filename}"
        print("Location:", full_path)

        sys.exit(1)

    if not real_data:
        print("ERROR: Real data is empty. Check the file. Exiting.")
        sys.exit(1)

    func(real_data)

    print("Real completed.")


def get_input_file_lines(file_path: str) -> list[str]:
    file = pkg_resources.open_text(advent_of_code, file_path)

    input_text = file.read()
    lines = input_text.split("\n")

    return trim_final_empty_lines(lines)


def trim_final_empty_lines(lines: list[str]) -> list[str]:
    if not lines[-1]:
        return trim_final_empty_lines(lines[:-1])

    return lines
