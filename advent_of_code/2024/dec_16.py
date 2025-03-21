import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum

from advent_of_code.shared.utils import Direction, Position, run_solution

Lines = list[str]

CLOCKWISE_MAP: dict[Direction, Direction] = {
    Direction.UP: Direction.RIGHT,
    Direction.RIGHT: Direction.DOWN,
    Direction.DOWN: Direction.LEFT,
    Direction.LEFT: Direction.UP,
}

COUNTER_CLOCKWISE_MAP: dict[Direction, Direction] = {
    Direction.UP: Direction.LEFT,
    Direction.LEFT: Direction.DOWN,
    Direction.DOWN: Direction.RIGHT,
    Direction.RIGHT: Direction.UP,
}

ROTATION_COST = 1000
STEP_COST = 1


class Entity(Enum):
    EMPTY = "."
    WALL = "#"
    START = "S"
    END = "E"


@dataclass
class Grid:
    data: dict[Position, Entity]
    max_y: int
    max_x: int
    start: Position
    end: Position
    visited_positions: set[Position] = field(default_factory=set, init=False)

    def __contains__(self, position: Position) -> bool:
        return position in self.data

    def debug_print(self) -> None:
        print("-")
        for row in range(self.max_y):
            line = ""
            for col in range(self.max_x):
                line += self.data[Position(col, row)].value

            print(line)

        print("-")

    @staticmethod
    def from_lines(lines: Lines) -> "Grid":
        start_position = None
        end_position = None
        data: dict[Position, Entity] = {}

        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                match char:
                    case ".":
                        entity = Entity.EMPTY
                    case "#":
                        entity = Entity.WALL
                    case "S":
                        start_position = Position(col, row)
                        entity = Entity.START
                    case "E":
                        end_position = Position(col, row)
                        entity = Entity.END
                    case _:
                        raise ValueError("Unexpected value")

                data[Position(col, row)] = entity

        if not start_position or not end_position:
            raise ValueError("Unable to find start/end position")

        return Grid(data=data, start=start_position, end=end_position, max_y=len(lines), max_x=len(lines[0]))


@dataclass
class Walker:
    score: int
    pos: Position
    direction: Direction

    def take_step(self) -> None:
        self.pos = self.pos + self.direction
        self.score += STEP_COST

    def split(self) -> "list[Walker]":
        return [
            Walker(self.score, self.pos, self.direction),
            Walker(self.score + ROTATION_COST, self.pos, CLOCKWISE_MAP[self.direction]),
            Walker(self.score + ROTATION_COST, self.pos, COUNTER_CLOCKWISE_MAP[self.direction]),
        ]


def main(lines: Lines) -> None:
    grid = Grid.from_lines(lines)

    initial_walkers = [
        Walker(0, grid.start, Direction.RIGHT),
        Walker(ROTATION_COST, grid.start, Direction.DOWN),
        Walker(ROTATION_COST * 2, grid.start, Direction.LEFT),
        Walker(ROTATION_COST, grid.start, Direction.UP),
    ]

    koth_score = sys.maxsize

    queue = deque(initial_walkers)

    cost_map = defaultdict(lambda: sys.maxsize)

    while queue:
        walker = queue.popleft()

        walker.take_step()

        if walker.pos not in grid:
            continue

        if grid.data[walker.pos] == Entity.WALL:
            continue

        if cost_map[walker.pos] < walker.score:
            continue

        cost_map[walker.pos] = walker.score

        if walker.score >= koth_score:
            continue

        if walker.pos == grid.end:
            koth_score = walker.score

            continue

        queue.extend(walker.split())

    print(koth_score)


if __name__ == "__main__":
    run_solution("2024", "dec_16", main)
