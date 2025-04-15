from dataclasses import dataclass

from advent_of_code.shared.utils import Direction, Position, run_solution

Lines = list[str]

TIME_SAVING_CUTOFF = 100

P1_POSSIBLE_CHEAT_MOVES = (
    Position(-2, 0),
    Position(2, 0),
    Position(0, 2),
    Position(0, -2),
    Position(1, 1),
    Position(1, -1),
    Position(-1, 1),
    Position(-1, -1),
)


@dataclass
class PositionInfo:
    moves_to_end: int
    next_position: Position | None


@dataclass
class Grid:
    data: dict[Position, PositionInfo]
    start: Position
    end: Position

    def __contains__(self, other: Position) -> bool:
        return other in self.data

    @staticmethod
    def from_lines(lines: Lines) -> "Grid":
        start = None
        end = None

        positions: set[Position] = set()

        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                match char:
                    case "S":
                        start = Position(col, row)
                        positions.add(start)
                    case "E":
                        end = Position(col, row)
                        positions.add(end)
                    case ".":
                        positions.add(Position(col, row))
                    case _:
                        continue

        if not start or not end:
            raise ValueError("Start or End missing.")

        current_position = end
        next_position = None
        steps_from_end = 0

        data: dict[Position, PositionInfo] = {end: PositionInfo(steps_from_end, next_position)}
        while True:
            steps_from_end += 1
            previous_position = get_previous_position(current_position, next_position, positions)
            data[previous_position] = PositionInfo(steps_from_end, current_position)
            next_position = current_position
            current_position = previous_position

            if current_position == start:
                break

        return Grid(data=data, start=start, end=end)


def get_p2_cheat_moves() -> dict[Position, int]:
    move_radius = 20

    moves: dict[Position, int] = {}
    for left in range(move_radius + 1):
        for right in range(move_radius - left + 1):
            cost = left + right
            for move in [
                Position(left, right),
                Position(left, -right),
                Position(-left, right),
                Position(-left, -right),
            ]:
                moves[move] = cost

    return moves


def get_previous_position(
    current_position: Position, next_position: Position | None, positions: set[Position]
) -> Position:
    for direction in Direction:
        new_position = current_position + direction
        if new_position != next_position and new_position in positions:
            return new_position

    raise ValueError("Unable to find next position")


def main(lines: Lines) -> None:
    grid = Grid.from_lines(lines)
    p2_cheat_moves = get_p2_cheat_moves()

    p1_result = 0
    p2_result = 0

    current_position = grid.start
    while current_position:
        current_position_info = grid.data[current_position]

        for cheat_move, cheat_cost in p2_cheat_moves.items():
            cheat_position = current_position + cheat_move
            if cheat_position in grid:
                time_reduction = (
                    current_position_info.moves_to_end - grid.data[cheat_position].moves_to_end - cheat_cost
                )

                if time_reduction < TIME_SAVING_CUTOFF:
                    continue

                p2_result += 1

                if cheat_move in P1_POSSIBLE_CHEAT_MOVES:
                    p1_result += 1

        current_position = current_position_info.next_position

    print(p1_result)
    print(p2_result)


if __name__ == "__main__":
    run_solution("2024", "dec_20", main)
