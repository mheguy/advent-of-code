import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum

from advent_of_code.shared.utils import Direction, Position, run_solution

Lines = list[str]

CLOCKWISE_TURN_MAP: dict[Direction, Direction] = {
    Direction.UP: Direction.RIGHT,
    Direction.RIGHT: Direction.DOWN,
    Direction.DOWN: Direction.LEFT,
    Direction.LEFT: Direction.UP,
}

COUNTER_CLOCKWISE_TURN_MAP: dict[Direction, Direction] = {
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
    BEST = "O"


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
    visited_positions: set[Position]

    def take_step(self) -> None:
        self.pos = self.pos + self.direction
        self.score += STEP_COST

    def split(self) -> "list[Walker]":
        return [
            Walker(self.score, self.pos, self.direction, self.visited_positions),
            Walker(
                self.score + ROTATION_COST,
                self.pos,
                CLOCKWISE_TURN_MAP[self.direction],
                self.visited_positions.copy(),
            ),
            Walker(
                self.score + ROTATION_COST,
                self.pos,
                COUNTER_CLOCKWISE_TURN_MAP[self.direction],
                self.visited_positions.copy(),
            ),
        ]


def main(lines: Lines) -> None:
    grid = Grid.from_lines(lines)

    initial_walkers = [
        Walker(ROTATION_COST * 0, grid.start, Direction.RIGHT, {grid.start}),
        Walker(ROTATION_COST * 1, grid.start, Direction.DOWN, {grid.start}),
        Walker(ROTATION_COST * 2, grid.start, Direction.LEFT, {grid.start}),
        Walker(ROTATION_COST * 1, grid.start, Direction.UP, {grid.start}),
    ]

    koth_score = sys.maxsize
    queue = deque(initial_walkers)
    cost_map = defaultdict(lambda: sys.maxsize)
    positions_on_best_paths = set()

    while queue:
        walker = queue.popleft()

        walker.take_step()

        if grid.data[walker.pos] == Entity.WALL:
            continue

        if walker.score > cost_map[walker.pos] + ROTATION_COST:
            continue

        cost_map[walker.pos] = walker.score
        walker.visited_positions.add(walker.pos)

        if walker.pos == grid.end:
            if walker.score < koth_score:
                koth_score = walker.score
                positions_on_best_paths.clear()
            elif walker.score > koth_score:
                continue

            positions_on_best_paths.update(walker.visited_positions)
            continue

        queue.extend(walker.split())

    print(koth_score)
    print(len(positions_on_best_paths))


if __name__ == "__main__":
    run_solution("2024", "dec_16", main)
