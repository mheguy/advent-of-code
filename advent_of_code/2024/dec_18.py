import sys
from collections import defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
from typing import ClassVar

from advent_of_code.shared.utils import Direction, Position, run_solution

Lines = list[str]

is_sample = True


class NoSolutionError(Exception):
    pass


@dataclass(frozen=True)
class EntityInfo:
    symbol: str
    allows_traversal: bool


class Entity(Enum):
    EMPTY = EntityInfo(".", True)
    WALL = EntityInfo("#", False)


@dataclass
class Grid:
    data: dict[Position, Entity]
    max_y: int
    max_x: int
    cost_map: dict[Position, int] = field(default_factory=lambda: defaultdict(lambda: sys.maxsize), init=False)

    def __contains__(self, position: Position) -> bool:
        return position in self.data

    def is_valid_position(self, position: Position) -> bool:
        if entity := self.data.get(position):
            return entity.value.allows_traversal

        return False

    def debug_print(self) -> None:
        print("-")
        for row in range(self.max_y):
            line = ""
            for col in range(self.max_x):
                line += self.data[Position(col, row)].value.symbol

            print(line)

        print("-")

    @staticmethod
    def from_lines(lines: Lines) -> "Grid":
        data: dict[Position, Entity] = {}
        for text in lines:
            col = int(text.split(",")[0])
            row = int(text.split(",")[1])
            data[Position(col, row)] = Entity.WALL

        max_y = max(data, key=lambda x: x.y).y
        max_x = max(data, key=lambda x: x.x).x

        for x in range(max_x + 1):
            for y in range(max_y + 1):
                pos = Position(x, y)
                if pos not in data:
                    data[pos] = Entity.EMPTY

        return Grid(data=data, max_y=max_y, max_x=max_x)


@dataclass
class Walker:
    pos: Position
    facing: Direction
    score: int
    visited_positions: set[Position]
    step_cost: int = 1
    rotation_cost: int = 0

    CLOCKWISE_TURN_MAP: ClassVar[dict[Direction, Direction]] = {
        Direction.UP: Direction.RIGHT,
        Direction.RIGHT: Direction.DOWN,
        Direction.DOWN: Direction.LEFT,
        Direction.LEFT: Direction.UP,
    }

    COUNTER_CLOCKWISE_TURN_MAP: ClassVar[dict[Direction, Direction]] = {
        Direction.UP: Direction.LEFT,
        Direction.LEFT: Direction.DOWN,
        Direction.DOWN: Direction.RIGHT,
        Direction.RIGHT: Direction.UP,
    }

    def take_step(self, grid: Grid) -> bool:
        target_position = self.pos + self.facing

        if target_position in self.visited_positions:
            return False

        if not grid.is_valid_position(target_position):
            return False

        self.score += self.step_cost
        self.pos = target_position

        if self.score >= grid.cost_map[self.pos]:
            return False

        grid.cost_map[self.pos] = self.score
        self.visited_positions.add(target_position)

        return True

    def split(self) -> "list[Walker]":
        return [
            Walker(
                self.pos,
                self.facing,
                self.score,
                self.visited_positions,
            ),
            Walker(
                self.pos,
                self.CLOCKWISE_TURN_MAP[self.facing],
                self.score + self.rotation_cost,
                self.visited_positions.copy(),
            ),
            Walker(
                self.pos,
                self.COUNTER_CLOCKWISE_TURN_MAP[self.facing],
                self.score + self.rotation_cost,
                self.visited_positions.copy(),
            ),
        ]


def find_shortest_path_around_objects(start_position: Position, end_position: Position, grid: Grid) -> Walker:
    initial_walkers = [
        Walker(start_position, Direction.UP, 0, {start_position}),
        Walker(start_position, Direction.DOWN, 0, {start_position}),
        Walker(start_position, Direction.LEFT, 0, {start_position}),
        Walker(start_position, Direction.RIGHT, 0, {start_position}),
    ]

    koth: Walker | None = None
    queue = deque(initial_walkers)

    while queue:
        walker = queue.popleft()

        if not walker.take_step(grid):
            continue

        if walker.pos == end_position and (koth is None or walker.score < koth.score):
            koth = walker

        queue.extend(walker.split())

    if koth is None:
        raise NoSolutionError("No walker reached the end.")

    return koth


def main(lines: Lines) -> None:
    global is_sample  # noqa: PLW0603

    if is_sample:
        p1_length = 12
        is_sample = False
    else:
        p1_length = 1024

    grid = Grid.from_lines(lines[:p1_length])
    start_position = Position(0, 0)
    end_position = Position(grid.max_x, grid.max_y)

    walker = find_shortest_path_around_objects(start_position, end_position, grid)
    print(f"p1 result: {walker.score}")

    for text in lines[p1_length:]:
        x, y = map(int, text.split(","))
        grid.data[Position(x, y)] = Entity.WALL
        grid.cost_map.clear()

        try:
            find_shortest_path_around_objects(start_position, end_position, grid)
        except NoSolutionError:
            break
    else:
        raise ValueError("Never failed")

    print(f"p2 result: {text}")


if __name__ == "__main__":
    run_solution("2024", "dec_18", main)
