import re
from dataclasses import dataclass
from enum import Enum

from advent_of_code.shared.utils import Position, run_solution

Lines = list[str]

MOVE_COUNT = 100
robot_pattern = re.compile(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)")


class Quadrant(Enum):
    INVALID = "INVALID"
    NW = "NW"
    NE = "NE"
    SW = "SW"
    SE = "SE"


@dataclass
class Robot:
    position: Position
    velocity: Position


def main(lines: Lines) -> None:
    grid_info = {"width": 101, "height": 103}
    # grid_info = {"width": 11, "height": 7} # For debugging with the example

    robots: list[Robot] = []
    for line in lines:
        if match := robot_pattern.match(line):
            robots.append(  # noqa: PERF401
                Robot(
                    Position(int(match.group(1)), int(match.group(2))),
                    Position(int(match.group(3)), int(match.group(4))),
                )
            )

    moved_robots = [move_robot(robot, MOVE_COUNT, grid_info) for robot in robots]

    # Map robots into quadrants
    quadrants = {q: 0 for q in Quadrant}
    for robot in moved_robots:
        quadrants[get_quadrant(robot.position, grid_info)] += 1

    del quadrants[Quadrant.INVALID]

    result = 1
    for quad in quadrants.values():
        result *= quad

    print(result)


def move_robot(robot: Robot, time: int, grid_info: dict[str, int]) -> Robot:
    end_position = robot.position + (robot.velocity * time)

    x_pos = trim_positional_value(end_position.x, grid_info["width"])
    y_pos = trim_positional_value(end_position.y, grid_info["height"])

    return Robot(Position(x_pos, y_pos), robot.velocity)


def trim_positional_value(position: int, exclusive_limit: int) -> int:
    remainder = position % exclusive_limit

    if position >= 0:
        return remainder

    return (remainder + exclusive_limit) % exclusive_limit


def get_quadrant(pos: Position, grid_info: dict[str, int]) -> Quadrant:
    mid_x = grid_info["width"] // 2
    mid_y = grid_info["height"] // 2

    if pos.x == mid_x or pos.y == mid_y:
        return Quadrant.INVALID

    quadrant = ""

    if pos.y > mid_y:
        quadrant += "S"
    else:
        quadrant += "N"

    if pos.x > mid_x:
        quadrant += "E"
    else:
        quadrant += "W"

    return Quadrant(quadrant)


if __name__ == "__main__":
    run_solution("2024", "dec_14", main)
