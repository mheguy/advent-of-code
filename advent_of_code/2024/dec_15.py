from dataclasses import dataclass
from enum import Enum

from advent_of_code.shared.utils import Direction, Position, run_solution

Lines = list[str]

INSTRUCTION_MAPPING = {
    "^": Direction.UP.value.as_position,
    "v": Direction.DOWN.value.as_position,
    "<": Direction.LEFT.value.as_position,
    ">": Direction.RIGHT.value.as_position,
}


class Entity(Enum):
    EMPTY = "."
    WALL = "#"
    BOX = "O"
    ROBOT = "@"


@dataclass
class Grid:
    data: dict[Position, Entity]
    robot: Position
    max_y: int
    max_x: int

    def move_robot(self, new_position: Position) -> None:
        self.data[self.robot] = Entity.EMPTY
        self.data[new_position] = Entity.ROBOT
        self.robot = new_position

    def get_score(self) -> int:
        result = 0
        for k, v in self.data.items():
            if v == Entity.BOX:
                result += (k.y * 100) + k.x

        return result

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
        robot_position = None
        data: dict[Position, Entity] = {}

        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                match char:
                    case "#":
                        entity = Entity.WALL
                    case "O":
                        entity = Entity.BOX
                    case "@":
                        robot_position = Position(row, col)
                        entity = Entity.ROBOT
                    case ".":
                        entity = Entity.EMPTY
                    case _:
                        raise ValueError("Unexpected value")

                data[Position(col, row)] = entity

        if not robot_position:
            raise ValueError("Unable to find robot position")

        return Grid(data=data, robot=robot_position, max_y=len(lines), max_x=len(lines[0]))


def perform_movement_instruction(grid: Grid, direction: Position) -> None:
    new_position = grid.robot + direction
    content = grid.data[new_position]

    match content:
        case Entity.WALL:
            pass
        case Entity.EMPTY:
            grid.move_robot(new_position)
        case Entity.BOX:
            if try_move(grid, new_position, direction):
                grid.move_robot(new_position)
        case _:
            raise ValueError(f"Unexpected value: {content}")


def try_move(grid: Grid, position: Position, direction: Position) -> bool:
    new_position = position + direction
    content = grid.data[new_position]

    match content:
        case Entity.EMPTY:
            grid.data[new_position] = grid.data[position]
            return True
        case Entity.WALL:
            return False
        case Entity.BOX:
            if try_move(grid, new_position, direction):
                grid.data[new_position] = grid.data[position]
                grid.data[position] = Entity.EMPTY
                return True

            return False
        case _:
            raise ValueError(f"Unexpected value: {content}")


def main(lines: Lines) -> None:
    grid, instructions = parse_input(lines)

    for direction in instructions:
        perform_movement_instruction(grid, INSTRUCTION_MAPPING[direction])

    print(grid.get_score())


def parse_input(lines: Lines) -> tuple[Grid, str]:
    grid_movement_split = lines.index("")
    grid_instructions = lines[:grid_movement_split]
    movement_instructions = "".join(lines[grid_movement_split + 1 :])

    return Grid.from_lines(grid_instructions), movement_instructions


if __name__ == "__main__":
    run_solution("2024", "dec_15", main)
